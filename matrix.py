#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:57:10 2021

@author: akim
"""

import numpy as np
from NEK5000_func_lib import particleCoordsNew, binner
from os import listdir
import matplotlib.pyplot as plt

# path = input() + '/'
# path = '/home/afabret/data/room_deposition/roomBackUp00002_new/'
path = './fbalance/'

fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()
print('enter data type: s - sphere, else - all')
choose = input()
print('enter t1')
tt1 = int(input())
print('enter t2')
tt2 = int(input())
print('enter coordinates of center of the sphere informat of array x y z :')
arr = input() 
center = list(map(float,arr.split(' ')))

def build_matrix (choose, tt1, tt2, center):

    #params
    n = 5 #number of the bins
    num_ps = 5
    x0 = -0.5
    y0 = -0.5
    z0 = -0.5
    
    radius = 0.1
    t1, a1 = particleCoordsNew (path, fileList[tt1])
    t2, a2 = particleCoordsNew (path, fileList[tt2])
    
    t1 = np.round((t1 - 0.1628499834108E+03), 3)
    t2 = np.round((t2 - 0.1628499834108E+03), 3)
    
    box_coords = [[0 for x in range(n+1)] for x in range(3)]
    box_node = [[0 for x in range(n)] for x in range(3)]
    center = np.asarray([0.0,0.0,0.0])
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
    if choose.lower() in ['s', 'sphere']:
        t0, a0 = particleCoordsNew (path, fileList[0])
        filtered = []
        ps_index = []
        len_filtered = []
        fff = np.zeros(5)
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
        
        data_list1 = []
        data_list2 = []
        for ps in range(num_ps):
            a_np1 = np.asarray(a1[ps])
            data1 = a_np1[ps_index[ps]]
            data_list1.append(data1)
            a_np2 = np.asarray(a2[ps])
            data2 = a_np2[ps_index[ps]]
            data_list2.append(data2)
        
        data_t1 = data_list1[0]
        data_t2 = data_list2[0]
        for ps in range(1,num_ps):
            data_t1 = np.vstack((data_t1, data_list1[ps]))
            data_t2 = np.vstack((data_t2, data_list2[ps]))
    else:
        data_t1 = np.asarray(a1[0])
        data_t2 = np.asarray(a2[1])

    
    A = np.zeros((n**3, n**3))
    
    nn = np.asarray([n] * len(data_t1))
    
    pt_box_ind_t1 = *map(binner, data_t1[:,0], data_t1[:,2], data_t1[:,1], nn),
    pt_box_ind_t1 = np.asarray(pt_box_ind_t1)
    
    pt_box_ind_t2 = *map(binner, data_t2[:,0], data_t2[:,2], data_t2[:,1], nn),
    pt_box_ind_t2 = np.asarray(pt_box_ind_t2)
    
    for i in range(len(data_t1)):
        A[pt_box_ind_t1[i],pt_box_ind_t2[i]] = A[pt_box_ind_t1[i],pt_box_ind_t2[i]] + 1
    
    if choose.lower() in ['a', 'all']:
        title = 'Sphere' + str(center) + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_sphere' + str(center) + '_'+ str(int(t1)) +  '_' + str(int(t2))
    else:
        title = 'All particles' + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_all' + '_'+ str(int(t1)) +  '_' + str(int(t2))
    
    
    fig, ax = plt.subplots(figsize=(7, 7))
    im = ax.imshow(A)
    plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
              rotation_mode="anchor")
    ax.set_title(title)
    fig.tight_layout()
    heatmap = plt.pcolor(A)
    plt.colorbar(heatmap)
    plt.savefig(tit + '.png', dpi=200)

    
if __name__ == '__main__':
    build_matrix(choose, tt1, tt2, center)
