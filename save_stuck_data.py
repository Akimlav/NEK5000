#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 20 13:16:14 2021

@author: akim
"""

import time
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties


#correct overlaping!!!
path = './'
case_name = 'part'
file_ext = 'stuck' #extension


# path = '/home/akim/Downloads/'
# case_name = 'part_01_12'
# file_ext = 'stuck' #extension


# data proccesing for each size
data = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
# data = np.genfromtxt('./part_refined0.stuck', skip_header = 0, invalid_raise = False)
ind = []
for i in range(1,len(data)):
    a = data[i-1,1] - data[i,1]
    if a > 0:
        ind0 = np.where(np.isin(data[:,1], data[i,1]))
        ind.append(ind0)
        print(i, ind0)
        

indList = []
for i in ind:
    # print(i)
    # for j in range(i-1,len(data)):
    for j in range(i-1,len(data)):
        print(i, j)
        a = data[i-1,1] - data[j,1]
        if a > 0:
            print(j)
            index = np.where(np.isin(data[:,1], data[j,1]))
            indList.append(np.asarray(index[0][0]))
    
indList = np.asarray(indList)
    # 
data2 = np.delete(data,indList, axis=0)

# np.savetxt('part_refined.stuck', data2)

# data = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
# path = '/home/akim/room_production_pp/roomBackUp00023_last_t_step/'
# case_name = 'part'
# file_ext = 'stuck' #extension


# data proccesing for each size
# dataOrig = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
# A = np.unique(dataOrig[:,2])
# aList = []
# for i in A:
#     bList = []
#     for j in range(len(dataOrig)):
#         if i == dataOrig[j,2]:
#             bList.append(dataOrig[j,:])
#         bNp = np.asarray(bList)
#     aList.append(bNp)
# i = -1
# for data in aList:
#     i += 1
#     print(i)
#     num_rows, num_cols = data.shape
#     np.savetxt('ps_rbu23_' + str(i) + '.dat', data)
    
    
# b = np.genfromtxt('./sim_0.dat')
