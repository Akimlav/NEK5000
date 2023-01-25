#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:57:37 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import find_nearest, estimate_coef
#params
nn = 10 #number of the bins
num_ps = 5
step = 1
x0 = -0.5
y0 = -0.5
z0 = -0.5

# box_coords = [[0 for x in range(n+1)] for x in range(3)]
# box_node = [[0 for x in range(n)] for x in range(3)]

# box_coords[0][0] = x0
# box_coords[1][0] = y0
# box_coords[2][0] = z0

# delta = 1/n



path1 =  '/Users/akimlavrinenko/Documents/coding/data/room_data/each_size_sphere_traj'

path = '/Users/akimlavrinenko/Documents/coding/data/room_data'

# for j in range(0,3):
#     for i in range(1,n+1):
#         box_coords[j][i] = box_coords[j][i-1] + delta
#         box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

# box_coords = np.asarray(np.transpose(box_coords))
# box_node = np.asarray(np.transpose(box_node))
# box_node = np.round(box_node, 3)

fig, axs = plt.subplots(1, figsize=(5,5))
fontP = FontProperties()
fontP.set_size('xx-small')

# legend = box_node.tolist()

cm = plt.get_cmap('tab20')
# angleList = []

# t1 = np.linspace(-1, 0.5,151)
lll = []

# data0 = np.genfromtxt(path + '/sphere_trajectory_0.dat')
# data1 = np.genfromtxt(path1 + '/sphr_trj_c_0_ps_1.dat')
# d2_ps = []
for ps in range(num_ps):
    for n in range(nn):
        data = np.genfromtxt(path1 + '/sphr_trj_c_' + str(n) + '_ps_' + str(ps) + '.dat')
        print('number', n, np.shape(data), '/sphr_trj_c_' + str(n) + '_ps_' + str(ps) + '.dat')
        x = data[::step,1::3]
        y = data[::step,2::3]
        z = data[::step,3::3]
        time = data[::step, 0]
        d2List = []
        # plt.plot(x,y)
        s=0
        d2 = 0
        for t in range(len(time)):
            ll = []
            for num in range(len(x[0,:])):
                xd = [(number - x[t,num])**2 for number in x[t,:]]
                yd = [(number - y[t,num])**2 for number in y[t,:]]
                zd = [(number - z[t,num])**2 for number in z[t,:]]
                ld = [xd,yd,zd]
                sd = [sum(s) for s in zip(*ld)] #x+y+z distance
                ll.append(sd)
                s = [sum(i) for i in zip(*ll)] #sum of x[0][0] + x[1][0]...
            f = np.math.factorial(len(x[0,:]))/(2*(np.math.factorial(len(x[0,:])-2)))
            d2 = sum(s)/f
            d2List.append(d2)
        lll.append(d2List)

    arr = np.asarray(lll)
    arr = arr.T
    time  = np.reshape(time, (-1, 1))
    res = np.concatenate((time,arr), axis=1)
    # print(np.shape(res))
    # d2_ps.append(res)
    # np.savetxt('d2_' + str(ps) + '.dat', data)
    # print(np.shape(time))
np.savetxt('d2.dat', res)

# for i in range(1,50):
#     plt.plot(np.log10(res[:,0]), np.log10(res[:,i]))
# plt.show()


# d2f = np.genfromtxt('d2.dat')
# for i in range(0,5):
#     print((i*10)+5)
#     plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+6]), 'r')
#     plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+1]), 'b')
#     plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+10]), 'g')
# plt.show()
