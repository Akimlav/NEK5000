#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 16:38:16 2022

@author: akimlavrinenko
"""

import numpy as np
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list, matrix, binner
from os import listdir
import matplotlib.pyplot as plt
import itertools
from math import floor

dirpath = '../'
fold_name = 'fbala'
# dirpath = '/home/afabret/data/room_deposition/production_run/'
# fold_name = 'roomBackUp'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

path1 = folders[0] + '/'

#params
step = 1 # file step
n = 10 #number of the bins
num_ps = 1
radius = 0.05
#axis_count = 1
allFileList = allFileList[0::step]

x0 = -0.5
y0 = -0.5
z0 = -0.5

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
box_node = np.round(box_node, 3)
center_list = (list(itertools.product(box_node[:,0], box_node[:,1], box_node[:,2])))
center_list = [np.round(elem,3) for elem in center_list]

box_list = (list(itertools.product(box_coords[:,0], box_coords[:,1], box_coords[:,2])))
box_list = [np.round(elem,3) for elem in box_list]


t0, a0 = particleCoordsNew (folders[0] + '/', allFileList[0])
# fig, axs = plt.subplots(3,figsize=(7, 10))
for k in range(len(box_node[:,0])):
    filtered = []
    ps_index = []
    len_filtered = []
    fff = np.zeros(5)
    center = box_node[k,:]

    for ps in range(num_ps):
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


box = np.asarray(box_list)
box = box[:,0:2]
boxx = np.unique(box, axis = 0)


for n in range(len(boxx)-int(np.sqrt(len(boxx)))-1):
    xy = np.asarray([boxx[n,:],boxx[n+int(np.sqrt(len(boxx))),:], boxx[n+1,:], boxx[n+int(np.sqrt(len(boxx)))+1,:]])
    plt.plot(xy[:,0],xy[:,1], 'o')
    plt.xlim(-0.5,0.5)
    plt.ylim(-0.5,0.5)
plt.show()


x = np.linspace(x0,0.5,11)
y = np.linspace(y0,0.5,11)
for i in range(len(x)):
    for j in range (1,len(y)):
        print(x[i], y[j])
        
H, yedges, xedges = np.histogram2d(x, y, bins=10)

# normalized = B/B.max()  # rescale to between 0 and 1
# corrected = np.power(normalized, 0.5) # try values between 0.5 and 2 as a start point

# title = 'All particles' + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
# tit = 'matrix_all' + '_'+ str(int(t1)) +  '_' + str(int(t2))
# heatmap = plt.pcolor(np.array(((0,1),(0,1))))

# fig, ax = plt.subplots(figsize=(7, 7))
# im = ax.imshow(corrected)
# ax.set_title(title)
# fig.tight_layout()
# plt.colorbar(heatmap)
# plt.savefig(tit + '.png', dpi=200)
# np.savetxt((tit + '.txt'), B)



    