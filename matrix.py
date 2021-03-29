#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:57:10 2021

@author: akim
"""

import numpy as np
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list, build_matrix
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

def pathTwo (ind):
    try:
        path2Ind = find_in_list_of_list(listOfFileList, allFileList[ind])
        path2 = folders[path2Ind[0]]
    except IndexError:
        path2Ind = find_in_list_of_list(listOfFileList, allFileList[-1])
        path2 = folders[path2Ind[0]]
    return path2 + '/'

step = 2
R = floor(len(allFileList)/step)
for i in range(R):
    print(i)
    file2 = 0 + i*step
    inpt =['a', 0, file2, 10, path1, pathTwo(file2), allFileList]
    t1, t2, B = build_matrix(*inpt)
    print(t2)
    # print(len(B), B.max())
    normalized = B/B.max()  # rescale to between 0 and 1
    corrected = np.power(normalized, 0.5) # try values between 0.5 and 2 as a start point
    # print(B)
    if inpt[0] == 'a':
        title = 'All particles' + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_all' + '_'+ str(int(t1)) +  '_' + str(int(t2))
        heatmap = plt.pcolor(np.array(((0,1),(0,1))))
        # heatmap = plt.pcolor(B)
    elif inpt[0] == 's':
        title = 'Sphere'  + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_sphere'  + '_'+ str(int(t1)) +  '_' + str(int(t2))
        # heatmap = plt.pcolor(np.array(((0,30),(0,30))))
    fig, ax = plt.subplots(figsize=(7, 7))
    im = ax.imshow(corrected)
    ax.set_title(title)
    fig.tight_layout()
    plt.colorbar(heatmap)
    plt.savefig(tit + '.png', dpi=200)
    np.savetxt((tit + '.txt'), B)
