#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:24:13 2021

@author: akimlavrinenko
"""
import matplotlib.pyplot as plt
import numpy as np

data = np.genfromtxt('/Users/akimlavrinenko/Documents/coding/data/room_data/each_size_sphere_traj/sphr_trj_diag_c_0_ps_0.dat')
# fig = plt.figure(figsize=(5, 5))
for i in range(len(data)):
    # ax = fig.add_subplot(projection='3d')
    
    print(i)
    x = data[:,1]
    y = data[:,2]
    z = data[:,3]
    time = data[:, 0]
    # ax.scatter(x[i,:], z[i,:], y[i,:], c = 'r', marker='.')
    plt.plot(x[i], y[i], 'r.')
    # ax.set_xlim(-0.5, 0.5)
    # ax.set_ylim(-0.5, 0.5)
    # ax.set_zlim(-0.5, 0.5)
    # ax.scatter(x_vals, y_vals, z_vals, c = 'b', marker='o')
    # ax.set_xlabel('X-axis')
    # ax.set_ylabel('Z-axis')
    # ax.set_zlabel('Y-axis')
    # ax.set_title('sphr_trj_c_0_ps_0, t = ' + str(time[i]))
    plt.xlim(-0.5,0.5)
    plt.ylim(-0.5,0.5)
    plt.savefig('c_0_ps_0_t_' + str(i) +'.png', dpi=200)
    plt.show()
