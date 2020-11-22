#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:51:35 2020

@author: akimlavrinenko
"""
import numpy as np


# data1 = np.genfromtxt('inletData',skip_header=1,invalid_raise = False)
# mesh = np.genfromtxt('meshData',skip_header=1,invalid_raise = False)
# n = sum(1 for line in open('inletData', 'r'))-1     # -1 пропускаем первую строку
# m = sum(1 for line in open('meshData', 'r'))-1


def yPlus(path):
    path = path
    yPlus = np.genfromtxt(path + 'postProcessing/yPlus/yPlus.dat',invalid_raise = False)    
    yPlus_1 = yPlus[::2]
    n_str = sum(1 for line in yPlus_1) -1    # -1 пропускаем первую строку
    data_y = yPlus_1[n_str,:][:,]
    y_min = yPlus_1[n_str,:][2]
    y_max = yPlus_1[n_str,:][3]
    y_avg = yPlus_1[n_str,:][4]
    y_data = [y_min, y_max, y_avg]
    return()


# for j in range (0, m-1):
#     mesh_path = 'mesh_'+ str(mesh[j][0])+'_c=' + str(mesh[j][1])

#     for i in range (0, n-1):
#         case_path = 'case_U=' + str(data1[i][0]) + '_m_' + str(mesh[j][0])

