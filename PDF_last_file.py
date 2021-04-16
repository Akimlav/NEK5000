#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 16 14:04:22 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
from time import time
import itertools
from scipy.stats import norm
import statistics as st
from matplotlib.font_manager import FontProperties


dirpath = '/Users/akimlavrinenko/Documents/coding/data/test_data'
fold_name = 'fbala'
# dirpath = '/home/afabret/data/room_deposition/production_run/'
# fold_name = 'roomBackUp'


folders = fast_scandir(dirpath)
folders = [word for word in folders if fold_name in word]
folders.sort()

listOfFileList, allFileList = listfile(folders)

#params
step = 3 # file step
n = 10 #number of the bins
num_ps = 5
radius = 0.05
#axis_count = 1
allFileList = allFileList[0::step]

x0 = -0.5
y0 = -0.5
z0 = -0.5
delta = 1/n
box_coords = [[0 for x in range(n+1)] for x in range(3)]
box_node = [[0 for x in range(n)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

for j in range(0,3):
    for i in range(1,n+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))
box_node = np.round(box_node, 2)

t_c = []
ind = find_in_list_of_list(listOfFileList, allFileList[-1])
if allFileList[-1] in listOfFileList[ind[0]]:
    path = folders[ind[0]] + '/'
    t, a = particleCoordsNew (path, allFileList[-1])
    for ps in range(0,num_ps):
        a_np = np.asarray(a[ps])
        xedges = box_coords[:,0]
        yedges = box_coords[:,1]
        zedges = box_coords[:,2]
        H, edges = np.histogramdd(a_np, bins=(xedges, yedges, zedges))
        t_c.append(H)
    binPs = []
    for i in range(5):
        a = t_c[i]
        b = a.ravel()
        binPs.append(list(b))

x = [binPs[0][i] + binPs[1][i] + binPs[2][i] + binPs[3][i] + binPs[4][i] for i in range(len(binPs[0]))]

fig, ax = plt.subplots(1, 1)
ax.hist(x, density=False, bins=100)
ax.set_xlabel('particle count in the bin')
ax.set_ylabel('number of bins')
ax.grid(True)
plt.savefig('bins_vs_particles.png', dpi=200)
# plt.show()
