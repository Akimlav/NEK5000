#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:25:01 2021

@author: akimlavrinenko
"""
import numpy as np

from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
from time import time


start_time = time()

# dirpath = '../data'
# fold_name = 'fbala'
dirpath = '/home/afabret/data/room_deposition/production_run/'
fold_name = 'roomBackUp'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 1 # file step
allFileList = allFileList[0::step]
allFileList = allFileList[:4500]

ls = []
filtered = []
t0, a0 = particleCoordsNew (folders[0] + '/', allFileList[0])
flat_list0 = [item for sublist in a0 for item in sublist]
flat_list0 = np.asarray(flat_list0)
index = (np.where((flat_list0[:,2] <= 0.01) & (flat_list0[:,2] >= -0.01)))

start_time2 = time()
for file in allFileList:
    ind = find_in_list_of_list(listOfFileList, file)
    if file in listOfFileList[ind[0]]:
        path = folders[ind[0]] + '/'
        t, a = particleCoordsNew (path, file)
        t = np.round((t - 0.1628499834108E+03), 3)
        flat_list = [item for sublist in a for item in sublist]
        npList = np.asarray(flat_list)
        npList = npList[index]
        flatList = npList.ravel()
        final = np.append(t, flatList)
        ls.append(final)

ls = np.asarray(ls)
np.savetxt('trajectories.txt', ls)

# print('Plotting was: %.3f seconds' % (time() - start_time4))
# print('All it was: %.3f seconds'  % (time() - start_time))




