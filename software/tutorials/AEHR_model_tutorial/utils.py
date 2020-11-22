# -*- coding: utf-8 -*-
"""
Created on Sat Oct 17 01:46:52 2020

@author: agarwal.270a
"""
import tensorflow as tf
import numpy as np
import scipy.signal as sig

eps=1e-7


def sliding_window_fragmentation(tseries,win_size,step_size,axes=None):
    '''
    sliding_window_fragmentation along the axis dimension
    for eg.:
    tseries=list of (numpy array of shape [n_tsteps,vector_dim_at_every_tstep])
    '''
    assert type(tseries)==type([]), 'Input time-series should be a list of numpy arrays'
    if axes is None:
        axes=[0 for _ in range(len(tseries))]
    tot_len=tseries[0].shape[axes[0]]
    indices=np.stack([np.arange(i,i+(tot_len-win_size+1),step_size)
                        for i in range(win_size)],axis=1)
    #slid_arr=np.stack([tseries[i:i+(tot_len-win_size+1):step_size8]
    #                    for i in range(win_size)],axis=1)
    slid_tseries=[np.take(tseries[j],indices,axis=axes[j]) 
                    for j in range(len(tseries))]
    
    if len(slid_tseries)==1:
        return slid_tseries[0]
    else:
        return slid_tseries
        
def filtr_HR(X0,Fs=100,filt=True):
    nyq=Fs/2
    if len(X0.shape)==1:
        X0=X0.reshape(-1,1)
    X1 = np.copy(X0)#sig.detrend(X0,type='constant',axis=0); # Subtract mean
    if filt:
        # filter design used from Ju's code with slight changes for python syntax
        b = sig.firls(219,np.array([0,1,1.5,nyq]),np.array([1,1,0,0]),np.array([1,1]),nyq=nyq);
        X=np.zeros(X1.shape)
        for i in range(X1.shape[1]):
            #X[:,i] = sig.convolve(X1[:,i],b,mode='same'); # filtering using convolution, mode='same' returns the centered signal without any delay
            X[:,i] = sig.filtfilt(b,[1],X1[:,i])
    else:
        X=X1
    #X=sig.detrend(X,type='constant',axis=0); # subtracted mean again to center around x=0 just in case things changed during filtering
    return X

def Rpeak2HR(test_pks,win_len=8*100,step=1,Fs_pks=100):
    
    HR_curve=[np.sum(test_pks[step*i:step*i+win_len])/(win_len/Fs_pks) for i in 
              range(int((len(test_pks)-win_len+1)/step))]
    HR_curve=filtr_HR(np.array(HR_curve))
    return HR_curve

def make_data_pipe(data,batch_size=64,shuffle=True):
    #dataset = tf.data.Dataset.from_tensor_slices((data[0],data[1],data[2]))
    dataset = tf.data.Dataset.from_tensor_slices(tuple(data))
    if shuffle:
        dataset=dataset.shuffle(buffer_size=np.max([6*batch_size,1000]).astype(int))
    dataset=dataset.batch(batch_size).prefetch(2)
    return dataset