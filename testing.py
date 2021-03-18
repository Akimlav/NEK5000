#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 17 13:54:28 2021

@author: akim
"""
from os import listdir, scandir
# import os

dirpath = '/Users/akimlavrinenko/Documents/coding'
fold_name = 'fbala'

# path0 = '../fbalance'
# path1 = '/home/akim/room_production_pp/roomBackUp0002'
# path2 = '/home/akim/room_production_pp/roomBackUp0003'


# fileList = [name for name in listdir(path0) if name.endswith(".3D")]
# fileList.sort()


def fast_scandir(dirname):
    subfolders= [f.path for f in scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

def listfile(folders):
    allFileList = []
    listOfFileList = []
    for folder in folders:
        fileList = [name for name in listdir(folder) if name.endswith(".3D")]
        fileList.sort()
        listOfFileList.append(fileList)
        allFileList = allFileList + fileList
    return (listOfFileList, allFileList)

def find_in_list_of_list(mylist, char):
    for sub_list in mylist:
        if char in sub_list:
            return (mylist.index(sub_list), sub_list.index(char))
    raise ValueError("'{char}' is not in list".format(char = char))

listOfFileList, allFileList = listfile(folders)

for file in allFileList:
    # print (file)
    ind = find_in_list_of_list(listOfFileList, file)
    if file in listOfFileList[ind[0]]:
        path = folders[ind[0]] + '/'
        print(path)
    
for i in range(len(allFileList)):
    # print (i, allFileList[i])
    if file in listOfFileList[2]:
        path = folders[2] + '/'   





