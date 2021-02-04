# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 18:14:19 2020

@author: agarwal.270a
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import detrend
import tensorflow as tf
from tensorflow.keras import layers
from tensorflow import keras
import pickle
import glob
import pandas as pd
from tensorflow.keras.activations import relu
import datetime

from utils import make_data_pipe, Rpeak2HR, sliding_window_fragmentation

tf.keras.backend.set_floatx('float32')
lrelu_pt2=lambda x: relu(x, alpha=0.2)

#tf.keras.backend.clear_session()
#TODO: Added to run only on CPU when needed
#tf.config.set_visible_devices([], 'GPU') 
#%% Loading Data

def get_train_data(path,val_files=[],test_files=[],
                   win_len=8,step=1,Fs_pks=100):
    '''
    Use all files in the folder 'path' except the val_files and test_files
    '''
    def get_clean_ppg_and_ecg(files):
        list_clean_ppg=[];list_arr_pks=[]
        for i in range(len(files)):
            df=pd.read_csv(files[i],header=None)
            arr=df.values
            if 'clean' in files[i]:
                arr[:,41:45]=(detrend(arr[:,41:45].reshape(-1),0,'constant')
                                ).reshape((-1,4))
                list_clean_ppg+=[np.concatenate([arr[:,29:30],arr[:,41:45]],
                                    axis=-1),arr[:,30:31],arr[:,39:40],arr[:,40:41]]
                list_arr_pks+=[arr[:,45:49].reshape(-1)]    
        return list_clean_ppg,list_arr_pks
    files=glob.glob(path+'*.csv')
    #files=[fil for fil in files if 'WZ' in fil] #get wenxiao's data
    #separate val and test files
    s3=set(files);s4=set(val_files+test_files)
    files_2=list(s3.difference(s4))
    #files_2=[files_2[0]]
    #files_2=[fil for fil in files if not((val_names[0] in fil))]
    list_clean_ppg,list_arr_pks=get_clean_ppg_and_ecg(files_2)
    
    dsample_factr=4
    Fs_pks=int(Fs_pks/dsample_factr)
    win_len=win_len*Fs_pks
    
    list_r_pk_locs=[np.arange(len(arr_pks))[arr_pks.astype(bool)] for 
                    arr_pks in list_arr_pks]
    
    #get nearest dsampled idx
    #TODO: Started using round instead of floor
    list_r_pk_locs_dsampled=[np.round(r_pk_locs/dsample_factr).astype(int) for 
                             r_pk_locs in list_r_pk_locs]
    #print([np.max(r_pks) for r_pks in list_r_pk_locs_dsampled])
    #print([len(ppg) for ppg in list_clean_ppg[::4]])
    
    list_arr_pks_dsampled=[]
    for j in range(len(list_arr_pks)):
        arr_pks_dsampled=np.zeros([int(len(list_arr_pks[j])/dsample_factr),1])
        #check & correct for rare rounding up issue in the last element
        if list_r_pk_locs_dsampled[j][-1]==len(arr_pks_dsampled):
            list_r_pk_locs_dsampled[j][-1]-=1
        arr_pks_dsampled[list_r_pk_locs_dsampled[j]]=1
        list_arr_pks_dsampled.append(arr_pks_dsampled)
    #print([len(ppg) for ppg in list_arr_pks_dsampled])


    list_HR=[4*[Rpeak2HR(arr_pks,win_len,step,Fs_pks)] 
             for arr_pks in list_arr_pks_dsampled]
    list_HR=sum(list_HR,[])
    #list_HR=[HR[::dsample_factr] for HR in list_HR]
    
    return list_clean_ppg,list_HR

def get_test_data(file_path,win_len,step,Fs_pks):
    df=pd.read_csv(file_path,header=None)
    arr=df.values
    test_in=[np.concatenate([arr[:,29:30],arr[:,41:45]],axis=-1),arr[:,30:31],
                            arr[:,39:40],arr[:,40:41]]
    
    arr_pks=arr[:,45:49].reshape(-1)
    
    dsample_factr=4
    Fs_pks=int(Fs_pks/dsample_factr)
    win_len=win_len*Fs_pks
    
    r_pk_locs=np.arange(len(arr_pks))[arr_pks.astype(bool)]
    
    #get nearest dsampled idx
    #TODO: Started using round instead of floor
    r_pk_locs_dsampled=np.round(r_pk_locs/dsample_factr).astype(int)
    #print([np.max(r_pks) for r_pks in list_r_pk_locs_dsampled])
    #print([len(ppg) for ppg in list_clean_ppg[::4]])
    arr_pks_dsampled=np.zeros([len(test_in[0]),1])
        #check & correct for rare rounding up issue in the last element
    if r_pk_locs_dsampled[-1]==len(arr_pks_dsampled):
        r_pk_locs_dsampled[-1]-=1
    arr_pks_dsampled[r_pk_locs_dsampled]=1
    #print([len(ppg) for ppg in list_arr_pks_dsampled])


    list_HR=4*[Rpeak2HR(arr_pks_dsampled,win_len,step,Fs_pks)] 
    
    test_in=[ppg.astype('float32') for ppg in test_in]
    test_out=[HR[:,0].astype('float32') for HR in list_HR]
    return test_in,test_out
#%%

def create_model(in_shape,HR_win_len=200):
    expand_dims = layers.Lambda(lambda x: tf.expand_dims(x,axis=-1), 
                                name='expand_dims')
    #RNN model via. Functional API
    rnn = layers.GRU(64, return_sequences=True, return_state=True)
    sig_in = layers.Input(shape=in_shape)
    #x = expand_dims(sig_in)
    x = sig_in
    _, final_state=rnn(x[:,:-HR_win_len,:]) #warm-up RNN
    rnn_out, _ = rnn(x[:,-HR_win_len:,:],initial_state=final_state)
    HR_hat=layers.Conv1D(filters=1,kernel_size=1, strides=1,padding='same',
                         activation=None,name='Conv_{}'.format(1))(rnn_out)
    HR_hat=layers.Flatten()(HR_hat)
    model = keras.Model(sig_in, HR_hat, name='model_HR')
    return model

def create_infer_model(in_shape):
    #RNN model via. Functional API
    rnn = layers.GRU(64, return_sequences=True, return_state=True)
    initial_state = layers.Input(shape=(64,))
    sig_in = layers.Input(shape=in_shape)
    rnn_out, final_state = rnn(sig_in,initial_state=initial_state)
    HR_hat=layers.Conv1D(filters=1,kernel_size=1, strides=1,padding='same',
                         activation=None,name='Conv_{}'.format(1))(rnn_out)
    HR_hat=layers.Flatten()(HR_hat)
    model = keras.Model([initial_state,sig_in],[final_state,HR_hat], name='model_infer_HR')
    return model
#%%
def main():
    #Get Train Data
    plt.close('all')
    path_prefix='data/pre-training'
    exp_id='1_3'
    log_prefix='data/post-training/experiments/{}'.format(exp_id)
    
    path=(path_prefix+'/')
    val_files=[path+'2019092801_3154_clean.csv']
    test_files=[path+'2019092820_5701_clean.csv']
    win_len=8 #in sec
    step=1 #in n_samples
    Fs_pks=100 #in Hz
    #input_list,output_list=[],[]
    list_sigs,list_HR=get_train_data(path,val_files,test_files,win_len,
                                           step,Fs_pks)
    
    #Pre-process data
    dsample_factr=4;Fs_new=int(Fs_pks/dsample_factr)
    sample_win_len,step_size=win_len*Fs_new,2*Fs_new
    HR_win_len=sample_win_len*3 #TODO: Can change this later, 4 is arbitrary choice after profs suggestion
    ppg_win_len=sample_win_len+HR_win_len
    
    model_sigs_in,model_HR_out=[],[]
    for j in range(len(list_HR)):
        #HR=list_HR[j][list_arr_pks[j].astype(bool)]
        ppg,HR=list_sigs[j][:,0:1],list_HR[j]
        ppg=sliding_window_fragmentation([ppg],ppg_win_len,step_size)
        HR=sliding_window_fragmentation([HR],HR_win_len,step_size)
        print(len(ppg),len(HR))
        model_sigs_in.append(ppg)
        model_HR_out.append(HR[:len(ppg)]) #clipping extra HRs at the end
    model_sigs_in=np.concatenate(model_sigs_in,axis=0)
    model_HR_out=np.concatenate(model_HR_out,axis=0)
    model_in=model_sigs_in#[:,:,0] #removing last dummy dimension
    model_out=model_HR_out[:,-int(HR_win_len/3):,0] #removing last dummy dimension
    print(model_in.shape,model_out.shape)

    #Visualize
    idx=1
    plt.figure();plt.subplot(211);plt.plot(model_in[idx,:,:])
    plt.subplot(212);plt.plot(model_out[idx,:])
    
    #partition
    val_perc=0.14
    val_idx=int(val_perc*len(model_in))
    val_data=[model_in[0:val_idx],model_out[0:val_idx]]
    train_data=[model_in[val_idx:],model_out[val_idx:]]
    
    #shuffle train_data AFTER partition as time series based
    #perm=np.random.permutation(len(train_data[1]))
    #train_data=[train_data[0][perm],train_data[1][perm]]
    #perm=np.random.permutation(len(val_data[1]))
    #val_data=[val_data[0][perm],val_data[1][perm]]
    train_ds=make_data_pipe(train_data,batch_size=32,shuffle=True)
    val_ds=make_data_pipe(val_data,batch_size=128,shuffle=False)
        
    # Make HR model
    model = create_model(model_in.shape[1:],int(HR_win_len/3))
    
    #Verify model graph
    print(model.summary())
    # Include the epoch in the file name (uses `str.format`)

    ckpt_dir=log_prefix+'/sig2HR/checkpoints'
    stdout_log_file = log_prefix + '/sig2HR/stdout.log'

    #ckpt_filepath=ckpt_dir+'/cp-{epoch:04d}.ckpt'
    ckpt_filepath=ckpt_dir+'/cp.ckpt'

    os.makedirs(ckpt_dir,exist_ok=True)
    file_path=log_prefix+'/sig2HR/sig2HR.png'

    #compile and prep fo training
    model.compile(optimizer = "adam", loss = "mse", metrics = ["mse"])
    #callbacks
    callbacks=[]
    callbacks.append(tf.keras.callbacks.ModelCheckpoint(ckpt_filepath,
                    save_weights_only=True,save_best_only=True,
                    monitor="val_loss",mode='min'))
    
        
    model.fit(train_ds,epochs=500,validation_data=val_ds,callbacks=callbacks)
    
    
    #%% Create inference model
    #TODO: Change according to need
    #weights_path_prefix='../data/post-training/model_weights' #for saved weights
    weights_path_prefix=glob.glob('../experiments/' + exp_id + '*')[0] #for latest experiment weights

    pred_tsteps=200
    rmse=lambda y,y_hat:np.sqrt(np.mean((y.reshape(-1)-y_hat.reshape(-1))**2))

    infer_model_HR=create_infer_model([pred_tsteps,1])#TODO: manually set n_channels here
    #% Load HR model
    weights_dir_HR=weights_path_prefix+'/sig2HR/checkpoints'
    weights_filepath_HR=weights_dir_HR+'/cp.ckpt'
    latest_ckpt = tf.train.latest_checkpoint(weights_dir_HR)
    print('Loading model from ckpt {}'.format(latest_ckpt))
    infer_model_HR.load_weights(latest_ckpt)
    
    #Check if weights correctly loaded in infer model
    #HR_weights=[v.numpy() for v in model.variables]
    #infer_HR_weights=[v.numpy() for v in infer_model_HR.variables]
    #HR_weights_check=[(HR_weights[i]==infer_HR_weights[i]).astype(int).reshape(-1).prod()
    #                  for i in range(len(HR_weights))]
    
    ppg_in,HR_out=get_test_data(val_files[0],win_len,step,Fs_pks)
    ppg,HR=ppg_in[0][:,0:1],HR_out[0]
    ppg=sliding_window_fragmentation([ppg],pred_tsteps,pred_tsteps)
    HR=sliding_window_fragmentation([HR],pred_tsteps,pred_tsteps)

    #Get HR from True ppg
    HR_mem=np.zeros([1,*infer_model_HR.inputs[0].shape.as_list()[1:]])
    HR_out_list=[]
    for i in range(ppg.shape[0]):
        #HR_mem is updated alongwith prediction
        HR_mem, HR_out = infer_model_HR.predict([HR_mem,ppg[i:i+1,:,:]])
        HR_out_list.append(HR_out[0])
    HR_hat=np.concatenate(HR_out_list[1:],axis=0)
    
    plt.figure();plt.plot(HR.reshape(-1),'b',HR_hat.reshape(-1),'r--')
    plt.title('RMSE = {:.4f}'.format(rmse(HR,HR_hat)))

if __name__=='__main__':
    main()
