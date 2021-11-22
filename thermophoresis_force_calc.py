#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 10:54:08 2021

@author: akim
"""
import time
import numpy as np
import matplotlib.pyplot as plt
path = './'
case_name = 'part_refined'
file_ext = 'stuck' #extension


# data proccesing for each size
dataOrig = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
# data = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
A = np.unique(dataOrig[:,2])
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
    
    
# pData = np.genfromtxt('./ps_rbu23_0.dat')

Cs = 1.17
Cm = 1.14
Ct = 2.18
lambdaa = 6.8e-8
Kf = 0.026
Kp = 0.43
Ts = 10
T0 = 300
rho_f = 1.3
rho_p = 1350
u_s = 0.427
nu_f = 1.57e-5

Kn = 2*lambdaa/A

Ktp = 2*Cs*(Kf+2*Kp*Kn)*(1+2*Kn*(1.2+0.41*np.exp(-0.44/Kn))) / ((1+6*Cm*Kn)*(2*Kf+Kp+4*Kp*Ct*Kn))

n_th = -18* Ktp * nu_f**2 * rho_f * Ts / (A**2 * u_s**2 * rho_p * T0)
n_th2 = n_th[2:]

# for i in range(len(A)):

for i in range(2,5):
    thphList = []
    data = np.genfromtxt('./ps_rbu23_' + str(i) + '.dat')
    num_rows, num_cols = data.shape
    hot_wall = [data[i,:] for i in range (0, num_rows) if data[i,3] == -0.5]
    cold_wall = [data[i,:] for i in range (0, num_rows) if data[i,3] == 0.5]
    cold_ceiling = [data[i,:] for i in range (0, num_rows) if data[i,4] == 0.5]
    hot_floor = [data[i,:] for i in range (0, num_rows) if data[i,4] == -0.5]
    adiabatic_front = [data[i,:] for i in range (0, num_rows) if data[i,5] == 0.5]
    adiabatic_back = [data[i,:] for i in range (0, num_rows) if data[i,5] == -0.5]
    
    hot_wall = np.array(hot_wall)
    cold_wall = np.array(cold_wall)
    cold_ceiling = np.array(cold_ceiling)
    hot_floor = np.array(hot_floor)
    adiabatic_front = np.array(adiabatic_front)
    adiabatic_back = np.array(adiabatic_back)
    print(len(hot_floor))
    for j in hot_floor[:,10]:
        # print(i, j)
        thph = j * n_th[i]
        thphList.append(thph)
    m = np.mean(thphList)
    print(m)
    plt.plot(thphList)
    # plt.plot(A[i]*1.22, m, 'o')
plt.show()