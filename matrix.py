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
import math as m


path = '../fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()
step = 1 # file step
n = 5 #number of the bins
num_ps = 5
fileList = fileList[0::step]

# particle data
t1, a1 = particleCoordsNew (path, fileList[0])
t2, a2 = particleCoordsNew (path, fileList[-1])
data_t1 = np.asarray(a1[0])
data_t2 = np.asarray(a2[0])
t1 = np.round((t1 - 0.1628499834108E+03), 3)
t2 = np.round((t2 - 0.1628499834108E+03), 3)
n = 5

# nnn = 55000
# xp1 = np.random.rand(nnn,1) -.5
# yp1 = np.random.rand(nnn,1) -.5
# zp1 = np.random.rand(nnn,1) -.5
# xp2 = np.random.rand(nnn,1) -.5
# yp2 = np.random.rand(nnn,1) -.5
# zp2 = np.random.rand(nnn,1) -.5
# data_t1 = np.column_stack((xp1, yp1, zp1))
# data_t2 = np.column_stack((xp2, yp2, zp2))

A = np.zeros((n**3, n**3))

nn = np.asarray([n] * len(data_t1))

pt_box_ind_t1 = *map(binner, data_t1[:,0], data_t1[:,2], data_t1[:,1], nn),
pt_box_ind_t1 = np.asarray(pt_box_ind_t1)

pt_box_ind_t2 = *map(binner, data_t2[:,0], data_t2[:,2], data_t2[:,1], nn),
pt_box_ind_t2 = np.asarray(pt_box_ind_t2)

for i in range(len(data_t1)):
    A[pt_box_ind_t1[i],pt_box_ind_t2[i]] = A[pt_box_ind_t1[i],pt_box_ind_t2[i]] + 1


fig, ax = plt.subplots()
im = ax.imshow(A)
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")
ax.set_title("matrix A from fbalance data")
fig.tight_layout()
# plt.savefig('fbalance_data_matrix.png', dpi=150)
plt.show()