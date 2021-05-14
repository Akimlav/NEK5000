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
n = 10 #number of the bins
step = 10
x0 = -0.5
y0 = -0.5
z0 = -0.5

box_coords = [[0 for x in range(n+1)] for x in range(3)]
box_node = [[0 for x in range(n)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

delta = 1/n
path = '/home/akim/coding/data/sphere_trajectories'

for j in range(0,3):
    for i in range(1,n+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))
box_node = np.round(box_node, 3)

fig, axs = plt.subplots(3,figsize=(5, 12))
fontP = FontProperties()
fontP.set_size('xx-small')

legend = box_node.tolist()

cm = plt.get_cmap('tab20')
angleList = []
for n in range(10):
    data = np.genfromtxt(path + '/sphere_trajectory_' + str(n) + '.dat')
    # print(n, np.shape(data))
    x = data[::step,1::3]
    y = data[::step,2::3]
    z = data[::step,3::3]
    time = data[::step, 0]
    d2List = []
    
    for t in range(len(time)):
    # for t in range(10):
        # print(t)
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
    fp = 10**0
    lp = 10**0.65
    ref_point_s = find_nearest(time, fp)
    ref_point_e = find_nearest(time, lp)
    rp = [ref_point_s, ref_point_e]
    ind = np.where(np.isin(time, rp))
    
    time2 = time[int(ind[0][0]):int(ind[0][1])+1]
    d2List2 = d2List[int(ind[0][0]):int(ind[0][1])+1]
    d2List2Log = np.log10(d2List2)
    time2Log = np.log10(time2)
    b = estimate_coef(time2Log, d2List2Log)
    y_pred = b[0] + b[1]*time2Log
    
    slope = abs((y_pred[-1] - y_pred[0])/(time2Log[-1] - time2Log[0]))
    angle = np.degrees(np.arctan((slope)))
    angleList.append(angle)
    print(angle)
    
    
    
    # plt.plot(x[t,:],y[t,:], '.')
        # plt.xlim(-0.5,0.5)
        # plt.ylim(-0.5,0.5)
        # plt.show()

    axs[0].plot(np.log10(time), np.log10(d2List),color = cm(n))
    axs[0].set_xlabel('log t, [s]')
    axs[0].set_ylabel('log D^2, [m^2]')
    axs[0].set_title('all data')
    axs[0].grid(True)

    axs[1].plot(time2Log, d2List2Log,'--',color = cm(n),linewidth=0.85)
    axs[1].plot(time2Log,y_pred,'-' ,color = cm(n),linewidth=1.5)
    axs[1].set_xlabel('log time')
    axs[1].set_ylabel('log sigma')
    axs[1].set_title('linear regression')
    axs[1].grid(True)

axs[2].plot(np.linspace(0,9,10), angleList, 'o-')
axs[2].set_xticks(np.linspace(0,9,10))
axs[2].set_xticklabels(legend,rotation=90)
axs[2].grid(True)
axs[2].set_xlabel('sphere center')
axs[2].set_ylabel('slope angle')
# axs[2].set_title('')
fig.tight_layout()
fig.legend(legend, title='location', bbox_to_anchor=(0.9, 0.67), prop=fontP)
plt.savefig('slope_relative_dispersion.png', dpi=150)
plt.show()