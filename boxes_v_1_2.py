#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:25:01 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from os import listdir
from NEK5000_func_lib import particleCoords

#coords of box corners
# data = particleCoords('./', 'fbalance00001.3D', 0)
# num_rows, num_cols = data.shape
path = './'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()

step = 2 # file step
nx = 4 #number of the bins
n_ps = 5
axis_count = 1
fileList = fileList[0::step]

ll = []
lr = []
p_count = []
p_count_l = []
p_count_r = []
time_array = []

box = (-0.5, -0.46)

for axis in range(0, axis_count):

    for ps in range(0,n_ps):                 # particle size
        fig, axs = plt.subplots(2, 1,figsize=(7, 6))
        for file in fileList:
            time, data = particleCoords(path, file, ps)
            num_rows, num_cols = data.shape
            
            box_left = [data[k,:] for k in range (0, num_rows) if data[k, axis] > box[0] and data[k,axis] < box[1]]
            ll.append(np.asarray(box_left))
            p_count_l.append(len(box_left))
            
            box_right = [data[k,:] for k in range (0, num_rows) if data[k, axis] > abs(box[1]) and data[k,axis] < abs(box[0])]
            lr.append(np.asarray(box_right))
            p_count_r.append(len(box_right))
            
            ps_count_l = [p_count_l[z:z+len(fileList)] for z in range(0, len(p_count_l), len(fileList))] #ps size
            xyz_count_l = [ps_count_l[z:z+n_ps] for z in range(0, len(ps_count_l), n_ps)] #axis
            
            ps_count_r = [p_count_r[z:z+len(fileList)] for z in range(0, len(p_count_r), len(fileList))] #ps size
            xyz_count_r = [ps_count_r[z:z+n_ps] for z in range(0, len(ps_count_r), n_ps)] #axis
            
            time_array.append(np.round((time - 0.1628499834108E+03), 4))
            time_ps = [time_array[z:z+len(fileList)] for z in range(0, len(p_count_r), len(fileList))]
            time_axis = [time_ps[z:z+n_ps] for z in range(0, len(ps_count_r), n_ps)]
            
        # plot

            axs[0].plot(time_axis[axis][ps], (xyz_count_l[axis][ps]), 'o-', label=str(ps))
            axs[0].set_title('Left box')
            axs[0].set_ylabel('N of particles')
        
            axs[1].plot(time_axis[axis][ps], (xyz_count_r[axis][ps]), 'o-')
            axs[1].set_xlabel('time (s)')
            axs[1].set_title('Right box')
            axs[1].set_ylabel('N of particles')
            if axis == 0:
                axis_title = 'x'
            elif axis == 1:
                axis_title = 'y'
            elif axis == 2:
                axis_title = 'z'
            fig.suptitle('axis ' + axis_title + ', particle size ' + str(ps), fontsize=18)
            fig.legend()
            # plt.savefig(axis_title + '_N_of_particles_over_time' + '.png', dpi=200)
            # plt.show()


