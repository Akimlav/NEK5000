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
# dataOrig = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
data = np.genfromtxt('./part_refined.stuck', skip_header = 0, invalid_raise = False)
A = np.unique(data[:,2])
aList = []
for i in A:
    bList = []
    for j in range(len(data)):
        if i == data[j,2]:
            bList.append(data[j,:])
        bNp = np.asarray(bList)
    aList.append(bNp)
i = -1
for data in aList:
    i += 1
    print(i)
    num_rows, num_cols = data.shape
    np.savetxt('ps_rbu23_' + str(i) + '.dat', data)
    
    
pData = np.genfromtxt('./ps_rbu23_0.dat')

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
l_s = 1.22

Kn = 2*lambdaa/A

Ktp = 2*Cs*(Kf+2*Kp*Kn)*(1+2*Kn*(1.2+0.41*np.exp(-0.44/Kn))) / ((1+6*Cm*Kn)*(2*Kf+Kp+4*Kp*Ct*Kn))

n_th = -18* Ktp * nu_f**2 * rho_f * Ts / ((A*l_s)**2 * u_s**2 * rho_p * T0)
n_th2 = n_th

# for i in range(len(A)):

for i in range(0,5):
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
    
    # print(np.mean(cold_ceiling[:,10] * n_th[i]))
    print('_____________')
    # print(np.mean(cold_wall[:,10]* n_th[i]))
    print(str(round((A[i]*1.22e6), 3)) + ' \u03BC' + 'm')
    print('_____________')
    # plt.hist(cold_wall[:,10] * n_th[i],bins = 10, label = 'cold_wall')
    print(len(cold_wall), 'wall')
    if len(cold_ceiling) > 0:
        # plt.hist(cold_ceiling[:,10] * n_th[i],bins = 10, label = 'cold_ceiling')1
        print(len(cold_ceiling), 'ceiling')
        
    if len (hot_floor) > 0:
        # plt.hist(hot_floor[:,10] * n_th[i],bins = 10, label = 'hot_floor')
        print(len(hot_floor), 'floor')
        
    wallList = [cold_wall, cold_ceiling, hot_wall]
    # print(len(hot_floor))
    for k in wallList:
        if len(k) > 0:
            for j in range(len(k)):
                # print(i, j)
                # thph = (k[j] * n_th[i])/9.81
                thphMag = ((k[j,10]**2 + k[j,11]**2 + k[j,12]**2)**0.5)*n_th[i] / 9.81
                # print(thph)
                thphList.append(thphMag)
            m = np.mean(thphList)
            # n = np.mean(j)
        
        print(len(thphList), '|',round((A[i]*1.22e6), 3), '|', round(m,2),'|', round(n_th[i],2))
    print('_________________________________________________')
    # plt.plot(thphList)
    # plt.plot(A[i]*1.22, m, 'o')
    # plt.ylim(0,270)
    # plt.title(str(round((A[i]*1.22e6), 3)) + ' \u03BC' + 'm')
    # plt.xlabel('thermophoresis force')
    # plt.ylabel('amount of particles')
    # plt.legend()
    # plt.savefig(str(round((A[i]*1.22e6), 3)) + '.png', dpi=150)
    # plt.show()
    
Nu_v = 78
Nu_h = 112

nthNu_v = n_th * Nu_v
nthNu_h = n_th * Nu_h
ng = -65.64
ngArr5 = np.full(5,ng)
pd = A*l_s*1e6
res = np.vstack((pd,ngArr5,nthNu_h,nthNu_v)).T
np.savetxt('./table.dat', res)
