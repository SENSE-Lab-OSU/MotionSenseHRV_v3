# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 23:39:30 2020

@author: agarwal.270a
"""
import shutil
import getpass
from zipfile import ZipFile
import requests
import os
#from urllib.request import urlretrieve

def download_file(url,local_path):
    with requests.get(url, stream=True) as r:
        #r.raw.decode_content = True
        with open(local_path, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    return local_path

def unzip_file(zip_path,dir_path):
    try:
        with ZipFile(zip_path,'r') as zf:
            zf.extractall(path=dir_path)
    except RuntimeError:
        print('AES Encrypted zip file. Need pyzipper to continue.\n')
        shutil.rmtree(dir_path, ignore_errors=True) #delete old dir
        import pyzipper
        with pyzipper.AESZipFile(zip_path,'r',encryption=pyzipper.WZ_AES) as zf:
            pwd=getpass.getpass(prompt='Archive is password protected. Please enter the password to continue \n')
            zf.extractall(path=dir_path,pwd=pwd.encode())
        

def get_file(zip_file_url,zip_path,dir_path):
    print('\nDownloading {} File...\n'.format(zip_path))
    download_file(zip_file_url,zip_path)
    print('Extracting Files from {}...\n'.format(zip_path))
    unzip_file(zip_path,dir_path)
    print('Deleting temp Files...\n')
    os.remove(zip_path)
    print('All Done!\n')
    return

def main():
    zip_file_urls = ['https://osu.box.com/shared/static/0udt0xmitcbm3lkd0u3meq1wpya75h5p.zip',
                     'https://osu.box.com/shared/static/hwmd05bi26md2rowuiqfc2mc25ceehqv.zip']
    zip_paths=['./data/pre-training.zip','./data/post-training.zip']
    #dir_path=''#zip_path[:-4]#'./bio_gen_model/post-training_test'
    for i in range(2):
        get_file(zip_file_urls[i],zip_paths[i],'./data')

if __name__=='__main__':
    main()
    
