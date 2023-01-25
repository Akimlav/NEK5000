#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:16:14 2021

@author: akim
"""

import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


#correct overlaping!!!
path = '/Users/akimlavrinenko/Documents/coding/data/room_data/'
# case_name = 'metricsCleared'
# file_ext = 'dat' #extension

dataOrig = np.genfromtxt(path + 'metricsAll.dat', invalid_raise = False)
data = dataOrig[32222:, :]
# data = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
# A = np.unique(data[:,15])
# uniqInd = np.where(np.isin(A,data[:,15]))
# dataNew = data[uniqInd[0]]
# data = dataNew
def clear(data):
    ind = []
    for i in range(1,len(data)):
        a = data[i-1,0] - data[i,0]
        if a > 0:
            ind.append(i)
    
    indList = []
    for i in ind:
        for j in range(i-1, len(data)):
            a = data[i-1,0] - data[j,0]
            if a > 0:
                indList.append(j)
    
    data2 = np.delete(data,indList, axis=0)
    return data2

data = clear(data)
data[:,0] = 1.10164 * data[:,0]

# np.savetxt(path + 'metricsCleared.dat', A1)

fontP = FontProperties()
fontP.set_size('xx-small')
fig, axs = plt.subplots(3, figsize=(5, 10))

axs[0].plot(data[:,0], data[:,1])# ,label = allFileList[6])
axs[0].plot(data[:,0], data[:,2])# ,label = allFileList[6])

axs[0].set_title('k')
axs[0].grid(True)
# axs[0].set_xlim(0,0.6)
# axs[0].set_ylim(0,0.4)
axs[0].set_xlabel('t, s')
axs[0].set_ylabel('k')
###########################################
axs[1].plot(data[:,0], data[:,7])
axs[1].plot(data[:,0], data[:,8])

axs[1].set_title('e')
axs[1].grid(True)
# axs[1].set_xlim(0,0.6)
# axs[1].set_ylim(0,0.01)
axs[1].set_xlabel('t, s')
axs[1].set_ylabel('e')
###########################################
axs[2].plot(data[:,0], data[:,3])
axs[2].plot(data[:,0], data[:,4])

axs[2].plot(data[:,0], data[:,5])
axs[2].plot(data[:,0], data[:,6])

axs[2].set_title('Nu v')
axs[2].grid(True)
# axs[1].set_xlim(0,0.6)
axs[2].set_ylim(-70, -120)
axs[2].set_xlabel('t, s')
axs[2].set_ylabel('Nu')

# Nu = np.asarray([data[::50,0], abs(data[::50,3]),abs(data[::50,4]),abs(data[::50,5]),abs(data[::50,6])]).T
k_eps = np.asarray([data[::50,0], abs(data[::50,1]),abs(data[::50,2])]).T
np.savetxt('k_eps_Ra3e9.dat', k_eps)
fig.suptitle('metrics', fontsize=14)
fig.tight_layout()

plt.show()

for i in range(1,9):
    print(np.mean(data[:,i]))

# z = abs(data[::20,3])
