#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:57:37 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#params
n = 10 #number of the bins
step = 100
x0 = -0.5
y0 = -0.5
z0 = -0.5

box_coords = [[0 for x in range(n+1)] for x in range(3)]
box_node = [[0 for x in range(n)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

delta = 1/n

for j in range(0,3):
    for i in range(1,n+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))
box_node = np.round(box_node, 3)

legend = box_node.tolist()

cm = plt.get_cmap('tab20')

for n in range(3):
    data = np.genfromtxt('/Users/akimlavrinenko/Documents/coding/data/room_data/sphere_trajectory_' + str(n) + '.dat')
    print(n)
    x = data[::1,1::step]
    y = data[::1,2::step]
    z = data[::1,3::step]
    time = data[::1, 0]
    d2List = []
    for t in range(len(x)):
        ll = []
        for num in range(len(x[0,:])):
            xd = [(number - x[t,num])**2 for number in x[t,:]]
            yd = [(number - y[t,num])**2 for number in y[t,:]]
            zd = [(number - z[t,num])**2 for number in z[t,:]]
            ld = [xd,yd,zd]
            sd = [sum(i) for i in zip(*ld)]
            ll.append(sd)
        s = [sum(i) for i in zip(*ll)]
        d2 = sum(s)/len(x[0,:])
        d2List.append(d2)
        # print(d2)
        
    plt.plot(np.log(time), np.log(d2List))
    plt.xlabel('log t, [s]')
    plt.ylabel('log D^2, [m^2]')
    plt.grid()
    plt.legend(legend, title='location', bbox_to_anchor=(0.9, 0.67))
# plt.savefig('log_relative_dispersion.png', dpi=150)
plt.show()