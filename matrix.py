#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 24 13:57:10 2021

@author: akim
"""

import numpy as np
from NEK5000_func_lib import particleCoordsNew, binner, matrix, build_matrix
from os import listdir
import matplotlib.pyplot as plt
import itertools


# path = input() + '/'
# path = ''
# path = '../fbalance/'

fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()

# inpt =[['a', 0, 1, 5, path, fileList],['s', 0, -1, 5, path, fileList], ['s', 0, 1, 5, path, fileList], ['a', 0, 1, 5, path, fileList]]

inpt = [['a', 0, 50, 5, path, fileList],['a', 0, 1000, 5, path, fileList],['a', 0, 2500, 5, path, fileList],['a', 0, -1, 5, path, fileList],['a', 0, -1, 5, path, fileList],
        ['s', 0, 50, 5, path, fileList],['s', 0, 1000, 5, path, fileList],['s', 0, 2500, 5, path, fileList],['s', 0, -1, 5, path, fileList],['s', 0, -1, 5, path, fileList]]

for i in range(len(inpt)):
    print(i)
    t1, t2, B = build_matrix(*inpt[i])
    print(len(B), B.sum())
    print(B)
    if inpt[i][0] == 'a':
        title = 'All particles' + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_all' + '_'+ str(int(t1)) +  '_' + str(int(t2))
        heatmap = plt.pcolor(np.array(((0,2000),(0,2000))))
    elif inpt[i][0] == 's':
        title = 'Sphere'  + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
        tit = 'matrix_sphere'  + '_'+ str(int(t1)) +  '_' + str(int(t2))
        heatmap = plt.pcolor(np.array(((0,30),(0,30))))
    fig, ax = plt.subplots(figsize=(7, 7))
    im = ax.imshow(B)
    ax.set_title(title)
    fig.tight_layout()
    plt.colorbar(heatmap)
    plt.savefig(tit + '.png', dpi=200)
    plt.show()


# if choose == 'a':
#     title = 'All particles' + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
#     tit = 'matrix_all' + '_'+ str(int(t1)) +  '_' + str(int(t2))
#     heatmap = plt.pcolor(np.array(((0,2000),(0,2000))))
# elif choose == 's':
#     title = 'Sphere'  + ' t1 = ' + str(t1) +  ', t2 = ' + str(t2)
#     tit = 'matrix_sphere'  + '_'+ str(int(t1)) +  '_' + str(int(t2))
#     heatmap = plt.pcolor(np.array(((0,30),(0,30))))
# fig, ax = plt.subplots(figsize=(7, 7))
# im = ax.imshow(B)
# ax.set_title(title)
# fig.tight_layout()
# plt.colorbar(heatmap)
# # plt.savefig(tit + '.png', dpi=200)
# plt.show()
