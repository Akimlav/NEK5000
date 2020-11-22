#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 14:51:35 2020

@author: akimlavrinenko
"""
import numpy as np
import statistics as st 


data1 = np.genfromtxt('inletData',skip_header=1,invalid_raise = False)
mesh = np.genfromtxt('meshData',skip_header=1,invalid_raise = False)
n = sum(1 for line in data1)
m = sum(1 for line in mesh)

y1 = []
y2 = []
f1 = []
f2 = []

def prop_forces(path):
    #replace data    
    f1 = open(path + '/postProcessing/forces/0/force.dat', 'r') 
    f2 = open(path + '/postProcessing/forces/0/force_cleared.dat', 'w') 
    f3 = open(path + '/postProcessing/forces/0/moment.dat', 'r') 
    f4 = open(path + '/postProcessing/forces/0/moment_cleared.dat', 'w') 
    for line in f1: 
        f2.write(line.replace('(', ' ').replace(')', ' '))    
    f1.close() 
    f2.close() 
    for line in f3: 
        f4.write(line.replace('(', ' ').replace(')', ' '))    
    f3.close() 
    f4.close() 
    path = path
    force = np.genfromtxt(path + '/postProcessing/forces/0/force_cleared.dat',invalid_raise = False)
    moment = np.genfromtxt(path + '/postProcessing/forces/0/moment_cleared.dat',invalid_raise = False) 
    split = np.array_split(force,4) 
    force = split[3] 
    split = np.array_split(moment,4) 
    moment= split[3]
    time = force[:,][:,0] 
    time2 = moment[:,][:,0] 
    F_x = force[:,][:,1] 
    F_p = force[:,][:,4] 
    F_v = force[:,][:,7] 
    M_x = moment[:,][:,1] 
    M_p = moment[:,][:,4] 
    M_v = moment[:,][:,7]
    avg_F = np.mean(F_x) 
    avg_Fp = np.mean(F_p) 
    avg_Fv = np.mean(F_v) 
    avg_M = np.mean(M_x) 
    avg_Mp = np.mean(M_p) 
    avg_Mv = np.mean(M_v)
    res = [avg_F, avg_Fp, avg_Fv, avg_M, avg_Mp, avg_Mv, ]
    return(res)

def yPlus(path):
    path = path
    yPlus = np.genfromtxt(path + '/postProcessing/yPlus/0/yPlus.dat',invalid_raise = False)    
    yPlus_1 = yPlus[::2]
    n_str = sum(1 for line in yPlus_1) -1
    y_min = yPlus_1[n_str,:][2]
    y_max = yPlus_1[n_str,:][3]
    y_avg = yPlus_1[n_str,:][4]
    y_data = [y_min, y_max, y_avg]
    return(y_data)

for j in range (0, m):
    mesh_path = 'mesh9_'+ str(mesh[j][0])+'_c=' + str(mesh[j][1])
    print('pew')
    for i in range (0, n):
        case_path = 'case9_U=' + str(data1[i][0]) + '_c_' + str(mesh[j][1])
        print(case_path)
        f1 = list(prop_forces(case_path))
        f2.append(f1)
        y1 = list(yPlus(case_path))
        y2.append(y1)
       
np.savetxt("prop_forces.csv", f2, delimiter=",", fmt='%s')
np.savetxt("yPlus.csv", y2, delimiter=",", fmt='%s')

