#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:25:01 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from NEK5000_func_lib import particleCoordsNew
from time import time
import itertools

start_time = time()

print('path to working folder')
# path = input() + '/'
path = './fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()

#params
step = 3  # file step
n = 5 #number of the bins
num_ps = 5
axis_count = 1
fileList = fileList[0::step]
x0 = -0.5
y0 = -0.5
z0 = -0.5
# center = np.asarray([0.4,0.4,0.0])
radius = 0.1

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

xlabel = np.linspace(0, n**2, (n**2)+1)
box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))

center_list = (list(itertools.product(box_node[:,0], box_node[:,1], box_node[:,2])))
center_list = [  np.round(elem,2) for elem in center_list]
center_list = center_list[0::25]
center_array = np.asarray(center_list)

marker_list = ['r.', 'y.', 'g.', 'c.', 'b.',]
for file in fileList:
    fig, axs = plt.subplots(2, 2,figsize=(7, 7))
    axs[1, 1] = plt.subplot(224, projection='3d')
    for k in range(len(center_array[:,0])):
    # for k in range(5):
    
        filtered = []
        ps_index = []
        len_filtered = []
        t_c = []
        fff = np.zeros(5)
        center = box_node[k,:]
        t0, a0 = particleCoordsNew (path, fileList[0])
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
        
        start_time2 = time()

        t, a = particleCoordsNew (path, file)
        t = np.round((t - 0.1628499834108E+03), 3)
        for ps in range(0,num_ps):
            a_np = np.asarray(a[ps])
            data = a_np[ps_index[ps]]

            axs[0, 0].plot(data[:,1],data[:,2], marker_list[k], markersize=0.7)
            axs[0, 0].set_title('X - projection')
            axs[0, 1].plot(data[:,2],data[:,0], marker_list[k], markersize=0.7)
            axs[0, 1].set_title('Y - projection')
            axs[1, 0].plot(data[:,0],data[:,1], marker_list[k], markersize=0.7)
            axs[1, 0].set_title('Z - projection')
            axs[1, 1].plot(data[:,0],data[:,1], data[:,2], marker_list[k], markersize=0.5)
            axs[1, 1].set_title('Isometric view')
            axs[0, 0].set_xlim([-0.5, 0.5])
            axs[0, 0].set_ylim([-0.5, 0.5])
            axs[1, 1].set_xlim([-0.5, 0.5])
            axs[1, 1].set_ylim([-0.5, 0.5])
            axs[1, 1].set_zlim([-0.5, 0.5])
            axs[0, 0].set_ylim([-0.5, 0.5])
            axs[0, 1].set_xlim([-0.5, 0.5])
            axs[0, 1].set_ylim([-0.5, 0.5])
            axs[1, 0].set_xlim([-0.5, 0.5])
            axs[1, 0].set_ylim([-0.5, 0.5])

    fig.savefig('5sp_' + file[:-3] + '.png', dpi = 250)

print('All it was: %.3f seconds'  % (time() - start_time))

