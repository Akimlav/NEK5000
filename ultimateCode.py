#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 18:22:03 2023

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
from time import time
import itertools
import os


start_time = time()

# dirpath = '/Users/akimlavrinenko/Documents/coding/data/test_data/'
# fold_name = 'fbala'
dirpath = '/home/afabret/data/room_deposition/production_run/'
fold_name = 'roomBackUp'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 10 # file step
n = 5 #number of the bins
num_ps = 5
radius = 0.1
# lastfile = 10000
#
allFileList = allFileList[0::step]
allFileList = sorted(allFileList)
# allFileList = allFileList[:lastfile]

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

try:
    t0, a0 = particleCoordsNew (folders[0] + '/', allFileList[0])
except FileNotFoundError:
    print('no file in first folder! Will check in the second folder.')
try:
    t0, a0 = particleCoordsNew (folders[1] + '/', allFileList[0])
except FileNotFoundError:
    print('no file! no file in the second folder.')

indForEachSphere = []
marker_list = ['r.', 'y.', 'g.', 'c.', 'b.']

for k in range(len(box_node[:,0])):
# for k in range(1):
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
    indForEachSphere.append(ps_index)

t_c = []
cc = []
tlist = []
hlist = []
spherelist = []
trajectory = []

figures_path = os.getcwd() + '/figures'
if not os.path.exists(figures_path):
    os.makedirs(figures_path)

for file in allFileList:
    ind = find_in_list_of_list(listOfFileList, file)
    if file in listOfFileList[ind[0]]:
        path = folders[ind[0]] + '/'
        t, a = particleCoordsNew (path, file)
        t = np.round((t - t0), 3)
        tlist.append(t)
        fig, axs = plt.subplots(2, 2,figsize=(10, 10))
        axs[1, 1] = plt.subplot(224, projection='3d')
        fig.suptitle('t = ' + str(t).zfill(4), fontsize=14)
        for sphere in range(n):
            for ps in range(num_ps):
                a_np = np.asarray(a[ps])
                data = a_np[indForEachSphere[sphere][ps]]
                #get bins and save them in cc
                H, edges = np.histogramdd(data, bins=(box_coords[:,0], box_coords[:,1], box_coords[:,2]))
                cc.append(H)
                
                flatPs = data.ravel()
                trajectory.append(flatPs)
                
                axs[0, 0].plot(data[:,1],data[:,2], marker_list[sphere], markersize=0.7)
                axs[0, 0].set_title('X - projection')
                axs[0, 0].grid(True)
                axs[0, 1].plot(data[:,2],data[:,0], marker_list[sphere], markersize=0.7)
                axs[0, 1].set_title('Y - projection')
                axs[0, 1].grid(True)
                axs[1, 0].plot(data[:,0],data[:,1], marker_list[sphere], markersize=0.7)
                axs[1, 0].set_title('Z - projection')
                axs[1, 0].grid(True)
                axs[1, 1].plot(data[:,0],data[:,1], data[:,2], marker_list[sphere], markersize=0.5)
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
    plt.tight_layout()
    fig.savefig(figures_path + '/allspheres_' + file[:-3] + '.png', dpi = 250)

ts = [cc[z:z+(num_ps)] for z in range(0, len(cc), (num_ps))]
#allData consist of time step, each time step has bins, and in each bin are all particle sizes
allData = [ts[z:z+n] for z in range(0, len(ts), n)]
# Trajectory
traj_temp = [trajectory[z:z+(num_ps)] for z in range(0, len(trajectory), (num_ps))]
trajectory = [traj_temp[z:z+n] for z in range(0, len(traj_temp), n)]

reslist = []
for ps in range(num_ps):
    for sphere in range(n):
        for t in range(len(tlist)):
            d = trajectory[t][sphere][ps]
            # print(np.shape(d))
            reslist.append(d)
            
res = [reslist[z:z+len(allFileList)] for z in range(0, len(reslist), len(allFileList))]
res = [np.asarray(res[i]) for i in range(len(res))]
res = [res[z:z+n] for z in range(0, len(res), n)]

traj_path = os.getcwd() + '/trajectories'
if not os.path.exists(traj_path):
    os.makedirs(traj_path)
    

sphereAllsizes = []
for sphere in range(n):
    for ps in range(num_ps):
        datatosave = np.concatenate(((np.reshape(np.asarray(tlist), (np.shape(res[ps][sphere])[0], 1))), res[ps][sphere]), axis = 1)
        np.savetxt(traj_path + '/sphere_traj_ps_' + str(ps) + '_n_' + str(sphere) + '.dat', datatosave)
        print('sphere_traj_ps_' + str(ps) + '_n_' + str(sphere) + '.dat saved.')
        sphereAllsizes.append(res[ps][sphere])

resAllin1 = [sphereAllsizes[z:z+num_ps] for z in range(0, len(sphereAllsizes), num_ps)]
for nn in range(n):
    conc = np.concatenate((resAllin1 [nn]), axis = 1)
    datatosave = np.concatenate(((np.reshape(np.asarray(tlist), (np.shape(conc)[0], 1))), conc), axis = 1)
    np.savetxt(traj_path + '/sphere_traj_n_' + str(nn) + '.dat', datatosave)
    print('sphere_traj_allps_n_' + str(nn) + '.dat saved.')
    
# Sigma
binsList = []
binsList2d = []
for t in range(len(allData)):
    for sphere in range(n):
        allsizes= np.sum(allData[t][sphere], axis=0)
        binsList.append(allsizes)
        allsizes2d = np.sum(allsizes, axis=1)
        binsList2d.append(allsizes2d)


binsList = [binsList[z:z+n] for z in range(0, len(binsList), n)]
binsList2d = [binsList2d[z:z+n] for z in range(0, len(binsList2d), n)]

sigmalist = []
sigma2dlist = []

for t in range(len(allData)):
    for sphere in range(n):
        Cinf = (sum(sum(sum(binsList[t][sphere]))))
        Cinf2d = (sum(sum(binsList2d[t][sphere])))
        
        temp = np.zeros(np.shape(binsList[t][sphere]))
        temp2d = np.zeros(np.shape(binsList2d[t][sphere]))
        temp = (binsList[t][sphere]/delta**3 - Cinf)**2
        temp2d= (binsList2d[t][sphere]/delta**2 - Cinf2d)**2
        
        sigma = np.sqrt((sum(sum(sum(temp))))/n**3)
        sigma2d = np.sqrt((sum(sum(temp2d)))/n**2)
        sigmalist.append(sigma)
        sigma2dlist.append(sigma2d)

s = np.asarray([sigmalist[z:z+n] for z in range(0, len(sigmalist), n)])
sigmaSpheres = np.concatenate(((np.reshape(np.asarray(tlist), (np.shape(s)[0], 1))), s), axis = 1)

s2d = np.asarray([sigma2dlist[z:z+n] for z in range(0, len(sigma2dlist), n)])
sigmaSpheres2d = np.concatenate(((np.reshape(np.asarray(tlist), (np.shape(s2d)[0], 1))), s2d), axis = 1)

sigma_path = os.getcwd() + '/sigma'
if not os.path.exists(sigma_path):
    os.makedirs(sigma_path)

np.savetxt(sigma_path + '/sigma3d.dat', sigmaSpheres)
print('3D sigma data saved.')
np.savetxt(sigma_path + '/sigma2d.dat', sigmaSpheres2d)
print('2D sigma data saved.')
print('It took me ' + str(np.round((time() - start_time),2)), 'seconds.')
    


    
    
    
    