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
path = '/Users/akimlavrinenko/Documents/coding/data/room_data/thatcher_deposition/'
case_name = 'part'
file_ext = 'stuck' #extension


data = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
# A = np.unique(data[:,15])
# uniqInd = np.where(np.isin(A,data[:,15]))
# dataNew = data[uniqInd[0]]
# data = dataNew
def clean(data):
    ind = []
    for i in range(1,len(data)):
        a = data[i-1,1] - data[i,1]
        if a > 0:
            ind0 = np.where(np.isin(data[:,1], data[i,1]))
            ind.append(ind0[0][0])

    indList = []
    for i in ind:
        # print(i)
        for j in range(i-1, len(data)):
            a = data[i-1,1] - data[j,1]
            if a > 0:
                index = np.where(np.isin(data[:,1], data[j,1]))
                indList.append((index[0][0]))
                
    data2 = np.delete(data,indList, axis=0)
    return data2

A1 = clean(data)
A2 = clean(A1)
# A3 = clean(A2)
# A2 = A1


for i in range(1, len(A2)):
    a = A2[i-1,1] - A2[i,1]
    if a > 0:
        print(A2[i-1,1],A2[i,1],A2[i+1,1])
        
        
np.savetxt('part_refined.stuck', A2)

# data = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
# path = '/home/akim/room_production_pp/roomBackUp00023_last_t_step/'
# case_name = 'part'
# file_ext = 'stuck' #extension


# data proccesing for each size
dataOrig = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
A = np.unique(dataOrig[:,2])
aList = []
for i in A:
    bList = []
    for j in range(len(dataOrig)):
        if i == dataOrig[j,2]:
            bList.append(dataOrig[j,:])
        bNp = np.asarray(bList)
    aList.append(bNp)
i = -1
for data in aList:
    i += 1
    print(i)
    num_rows, num_cols = data.shape
    np.savetxt('ps_rbu23_' + str(i) + '.dat', data)
    
    
# b = np.genfromtxt('./sim_0.dat')
