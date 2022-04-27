#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:25:01 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
from time import time
import itertools

start_time = time()

# dirpath = '/Users/akimlavrinenko/Dropbox/My Mac (Akims-MacBook-Pro.local)/Documents/coding/data/test_data'
# fold_name = 'fbala'

# dirpath = '/home/akim/room_production_pp/old/fbalance/'
# fold_name = 'roomBackUp'
dirpath = '/home/afabret/data/room_deposition/production_run/'
fold_name = 'roomBackUp'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 200 # file step
n = 10 #number of the bins
num_ps = 5
radius = 0.05
allFileList = allFileList[0::step]
allFileList = sorted(allFileList)
# allFileList = allFileList[:2]
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

t0, a0 = particleCoordsNew (folders[1] + '/', allFileList[0])
# t0, a0 = particleCoordsNew (folders[0] + '/', allFileList[0])

pos = [box_node[0,:], box_node[4,:]]
name = ['sph_pop_crnr_ax_', 'sph_pop_cntr_ax_']

    
for k in range(2):
    filtered = []
    ps_index = []
    len_filtered = []
    t_c = []
    cc = []
    tt = []
    fff = np.zeros(5)
    center = pos[k]

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

    for file in allFileList:
        ind = find_in_list_of_list(listOfFileList, file)
        if file in listOfFileList[ind[0]]:
            path = folders[ind[0]] + '/'
            t, a = particleCoordsNew (path, file)
            t = np.round((t - t0), 3)
            for ps in range(0,num_ps):
                a_np = np.asarray(a[ps])
                data = a_np[ps_index[ps]]
                xedges = box_coords[:,0]
                yedges = box_coords[:,1]
                zedges = box_coords[:,2]
                H, edges = np.histogramdd(data, bins=(xedges, yedges, zedges))
                # t_c.append([t, H])
                cc.append(H)
                tt.append(t)

    ts = [cc[z:z+(num_ps)] for z in range(0, len(cc), (num_ps))]
    
    A = []
    for p in range(len(ts)):
        for j in range(3):
            tss = np.asarray(ts[p])
            tsum = np.sum(tss, axis = 0)
            tsumm = np.sum(tss, axis = 0)
            tsummm = np.sum(tsumm, axis = j)
            A.append(tsummm)
    
    B = [A[z:z+3] for z in range(0, len(A), 3)]
    tt = tt[::5]
    
    axisList = ['x','y','z']
    # for axis in axisList:
    for i in range(int(len(B))):
        for axis in range(3):
            arr = B[i][axis]
            t = np.round(tt[i]*7.37,2)
            title = 'Sphere'  + ' t = ' + str(t) + ' s, ' + axisList[axis] + ' - projection'
            tit = name[k] + axisList[axis] + '_t_' + str('%04d' % t)
            fig, ax = plt.subplots(figsize=(5, 5))
            ax.set_title(title)
            c = ax.pcolor(np.log10(arr), cmap = 'Reds', vmin=0, vmax=2.3,edgecolors='k', linewidths=0.0)
            plt.xticks((np.linspace(1,10,10)))
            plt.yticks((np.linspace(1,10,10)))
            fig.colorbar(c, ax=ax)
            fig.tight_layout()
        
            plt.savefig(tit + '.png', dpi=150)
            plt.show()
            plt.close()
        # np.savetxt((tit + '.txt'), B)

