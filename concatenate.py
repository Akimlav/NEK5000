#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:12:33 2022

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt

data = np.genfromtxt('/Users/akimlavrinenko/Documents/coding/data/diag/sphr_trj_diag_c_0_ps_0.dat')
newData = np.zeros((1917,1))
for j in range(1):
    for i in range(10):
        data = np.genfromtxt('/Users/akimlavrinenko/Documents/coding/data/diag/sphr_trj_diag_c_' + str(i) + '_ps_' + str(j) + '.dat')
        print('sphr_trj_diag_c_' + str(i) + '_ps_' + str(j) + '.dat')
        print(np.shape(data))
        
        newData[:,0] = data[:,0]
        newData = np.concatenate((newData, data[:,1:4]), axis = 1)
        np.savetxt('ps_0_diag_traj.dat', newData)
        
# for k in range(10):
#     plt.plot(newData[:,3*k+1], newData[:,3*k+2])
#     print(3*k+1, 3*k+2)
#     plt.plot(newData[0,3*k+1], newData[0,3*k+2], 'ko')
#     plt.xlim(-0.5,0.5)
#     plt.ylim(-0.5,0.5)
# plt.show()
        
