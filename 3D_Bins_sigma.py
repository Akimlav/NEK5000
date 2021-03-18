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


dirpath = '/Users/akimlavrinenko/Documents/coding'
fold_name = 'fbala'

folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 5 # file step
n = 5 #number of the bins
num_ps = 1
axis_count = 1
allFileList = allFileList[0::step]
x0 = -0.5
y0 = -0.5
z0 = -0.5
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
box_node = np.round(box_node, 2)
center_list = (list(itertools.product(box_node[:,0], box_node[:,1], box_node[:,2])))
center_list = [  np.round(elem,2) for elem in center_list]
# center_list = center_list[0::1]
legend = box_node.tolist()
legend1 = str(legend[0])
marker_list = ['r-', 'y-', 'g-', 'c-', 'b-',]

    
t0, a0 = particleCoordsNew (folders[0] + '/', allFileList[0])
for k in range(len(box_node[:,0])):
    print(k)
    filtered = []
    ps_index = []
    len_filtered = []
    t_c = []
    fff = np.zeros(5)
    center = box_node[0,:]

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
    for file in allFileList:
        ind = find_in_list_of_list(listOfFileList, file)
        if file in listOfFileList[ind[0]]:
            path = folders[ind[0]] + '/'
            t, a = particleCoordsNew (path, file)
            t = np.round((t - 0.1628499834108E+03), 3)
            for ps in range(0,num_ps):
                a_np = np.asarray(a[ps])
                data = a_np[ps_index[ps]]
                xedges = box_coords[:,0]
                yedges = box_coords[:,1]
                zedges = box_coords[:,2]
                H, edges = np.histogramdd(data, bins=(xedges, yedges, zedges))
                t_c.append([t, H])
    
    print('Reading all data was: %.3f seconds' % (time() - start_time2))
    
    start_time3 = time()
    
    tb = [t_c[z:z+(num_ps)] for z in range(0, len(t_c), (num_ps))]
    
    sss = []
    for file in allFileList:
        ind = find_in_list_of_list(listOfFileList, file)
        if file in listOfFileList[ind[0]]:
            path = folders[ind[0]] + '/'
            for ps in range(num_ps):
                M = fff[ps]/ n**3
                s = 0
                ss = 0
                sigma = 0
                for x in range (n):
                    for y in range (n):
                        for z in range (n):
                            s = (tb[allFileList.index(file)][ps][1][x][y][z] - M)**2
                            ss = ss + s
                            tt = tb[allFileList.index(file)][ps][0]
                sigma = ss**0.5/(fff[ps])
                sss.append([tt, sigma])

    ts = [sss[z:z+(num_ps)] for z in range(0, len(sss), (num_ps))]
    sigma_mean_list = []
    for i in range(len(ts)):
        sigma_sum = 0
        for j in range(len(ts[0])):
            sigma_sum = sigma_sum + ts[i][j][1]
            sigma_mean = sigma_sum / len(ts[0])
        sigma_mean_list.append([ts[i][j][0], sigma_mean])
    
    np_sigma_mean = np.asarray(sigma_mean_list)
    
    start_time4 = time()
    

    fontP = FontProperties()
    fontP.set_size('xx-small')
    plt.legend(legend, title='loc', bbox_to_anchor=(1.05, 1.01),loc='upper right', prop=fontP)
    plt.plot(np_sigma_mean[:,0], np_sigma_mean[:,1], marker_list[k])
    plt.xlabel('time')
    plt.ylabel('mean sigma')
    plt.yticks(np.arange(0, 1.1, step=0.1))
    plt.grid(True)
    plt.ylim(0, 1.05)
plt.savefig('mean_sigma_all_boxes' + '.png', dpi=200)

print('Plotting was: %.3f seconds' % (time() - start_time4))
print('All it was: %.3f seconds'  % (time() - start_time))


        



