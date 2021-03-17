#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:54:28 2021

@author: akim
"""
from os import listdir, scandir
# import os


path0 = '../fbalance'
path1 = '/home/akim/room_production_pp/roomBackUp0002'
path2 = '/home/akim/room_production_pp/roomBackUp0003'


fileList = [name for name in listdir(path0) if name.endswith(".3D")]
fileList.sort()


def fast_scandir(dirname):
    subfolders= [f.path for f in scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

folders = fast_scandir('/home/akim/room_production_pp/')
folders = [word for word in folders if 'roomBackUp' in word]
folders.sort()

allFileList = []
listOfFileList = []
for folder in folders:
    fileList = [name for name in listdir(folder) if name.endswith(".3D")]
    fileList.sort()
    listOfFileList.append(fileList)
    allFileList = allFileList + fileList
    
        
    

