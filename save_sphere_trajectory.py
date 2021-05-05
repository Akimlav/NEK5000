#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 12:34:56 2021

@author: akimlavrinenko
"""

import numpy as np
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
import matplotlib.pyplot as plt

# dirpath = '/home/akim/coding/data'
# fold_name = 'fbala'
dirpath = '/home/afabret/data/room_deposition/production_run/'
fold_name = 'roomBackUp'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 10 # file step
allFileList = allFileList[0::step]
# allFileList = allFileList[:3000]

n = 10 #number of the bins
num_ps = 5
x0 = -0.5
y0 = -0.5
z0 = -0.5
radius = 0.05

box_coords = [[0 for x in range(n+1)] for x in range(3)]
box_node = [[0 for x in range(n)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

delta = 1/n

for j in range(0,3):
    for i in range(1,n+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))

t0, a0 = particleCoordsNew (folders[1] + '/', allFileList[0])

filtered = []
ps_index = []
len_filtered = []
final = []
fff = np.zeros(5)
center = box_node[0,:]
for ps in range(num_ps): #getting indexes of spheres for all sizes
    aa0 = np.asarray(a0[ps])
    for j in range(len(aa0)):
        r1 = ((aa0[j,0] - center[0])**2 + (aa0[j,1] - center[1])**2 + (aa0[j,2] - center[2])**2)**0.5
        if r1 <= radius:
            filtered.append(aa0[j,:])
    len_filtered.append(len(filtered))
    if len(len_filtered) == 1:
        fff[ps] = len_filtered[ps]
    else:
        fff[ps] = len_filtered[ps] - len_filtered[ps-1]
    fff = fff.astype(int)
    ps_filtered = []
    count = 0
    for size in (fff):
        ps_filtered.append([filtered[i+count] for i in range(size)])
        count += size
    index = np.where(np.isin(aa0[:,1], np.asarray(ps_filtered[ps])))
    ps_index.append(index[0])
ls = []
tl = []
for file in allFileList:
    
    ind = find_in_list_of_list(listOfFileList, file)
    if file in listOfFileList[ind[0]]:
        path = folders[ind[0]] + '/'
        t, a = particleCoordsNew (path, file)
        t = np.round((t - 0.1628499834108E+03), 3)
        ln = []
        for ps in range(len(ps_index)):
            nnn = np.asarray(a[ps])
            nn = nnn[ps_index[ps]]
            ln.append(nn)
            flat_list = [item for sublist in ln for item in sublist]
            npList = np.asarray(flat_list)
            flatList = npList.ravel()
        ls.append(flatList)
        tl.append(t)

ls = np.asarray(ls)
tl = np.asarray(tl)

t = np.reshape(tl, (len(ls), 1))
data = np.concatenate((t, ls), axis = 1)

np.savetxt('sphere_trajectory.dat', data)
