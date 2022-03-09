#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:17:24 2020

@author: akimlavrinenko
"""
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

#data[i,j] - i for row, j for column

start_time = time.time()
# path = '/Users/akimlavrinenko/Documents/coding/data/room_data/thatcher_deposition/'
path = './'
case_name = 'part_refined'
file_ext = 'stuck' #extension

#data proccesing
dataOrig = np.genfromtxt(path + case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)

A = np.unique(dataOrig[:,2])
aList = []
for i in A:
    bList = []
    for j in range(len(dataOrig)):
        if i == dataOrig[j,2]:
            bList.append(dataOrig[j,:])
        bNp = np.asarray(bList)
    aList.append(bNp)

# for data in aList:
for data in range(0,5):
    data = aList[data]
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

    np.savetxt('hw_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', hot_wall)
    np.savetxt('cw_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', cold_wall)
    np.savetxt('cc_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', cold_ceiling)
    np.savetxt('hf_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', hot_floor)
    np.savetxt('af_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', adiabatic_front)
    np.savetxt('ab_deposited_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.dat', adiabatic_back)
    
    fig, axs = plt.subplots(6, figsize=(5,25))
    fontP = FontProperties()
    fontP.set_size('xx-small')
    # fig.suptitle('Total amount of particles are ' + str(len(data)), fontsize=16)
    if len(hot_wall) > 0:
        axs[0].plot(hot_wall[:,4],hot_wall[:,5],'ro')
        axs[0].grid(True)
        axs[0].set_xlabel('Z')
        axs[0].set_ylabel('Y')
        axs[0].set_title('hot wall, ' + str(len(hot_wall)) + ' particles')
        axs[0].set_xlim(-0.5,0.5)
        axs[0].set_ylim(-0.5,0.5)
    else:
        print('hot wall is empty')
        
    if len(cold_wall) > 0:
        axs[1].plot(cold_wall[:,4],cold_wall[:,5],'bo')
        axs[1].grid(True)
        axs[1].set_xlabel('Z')
        axs[1].set_ylabel('Y')
        axs[1].set_title('cold wall, ' + str(len(cold_wall)) + ' particles')
        axs[1].set_xlim(-0.5,0.5)
        axs[1].set_ylim(-0.5,0.5)
    else:
        print('cold wall is empty')
    
    if len(cold_ceiling) > 0:
        axs[2].plot(cold_ceiling[:,3],cold_ceiling[:,5],'bo')
        axs[2].grid(True)
        axs[2].set_xlabel('Z')
        axs[2].set_ylabel('X')
        axs[2].set_title('cold ceiling, '  + str(len(cold_ceiling)) + ' particles')
        axs[2].set_xlim(-0.5,0.5)
        axs[2].set_ylim(-0.5,0.5)
    else:
        print('cold ceiling is empty')
    
    if len(hot_floor) > 0:
        axs[3].plot(hot_floor[:,3],hot_floor[:,5],'ro', markersize=3)
        axs[3].grid(True)
        axs[3].set_xlabel('Z')
        axs[3].set_ylabel('X')
        axs[3].set_title('hot floor, '  + str(len(hot_floor)) + ' particles')
        axs[3].set_xlim(-0.5,0.5)
        axs[3].set_ylim(-0.5,0.5)
    else:
        print('hot floor is empty')
    
    if len(adiabatic_front) > 0:
        axs[4].plot(adiabatic_front[:,3],adiabatic_front[:,4],'o')
        axs[4].grid(True)
        axs[4].set_xlabel('X')
        axs[4].set_ylabel('Y')
        axs[4].set_title('adiabatic front, '  + str(len(adiabatic_front)) + ' particles')
        axs[4].set_xlim(-0.5,0.5)
        axs[4].set_ylim(-0.5,0.5)
    else:
        print('adiabatic front wall is empty')
    
    if len(adiabatic_back) > 0:
        axs[5].plot(adiabatic_back[:,3],adiabatic_back[:,4],'o')
        axs[5].grid(True)
        axs[5].set_xlabel('X')
        axs[5].set_ylabel('Y')
        axs[5].set_title('adiabatic back, '  + str(len(adiabatic_back)) + ' particles')
        axs[5].set_xlim(-0.5,0.5)
        axs[5].set_ylim(-0.5,0.5)
    else:
        print('adiabatic back wall is empty')
    
    text = 'Total amount of particles are ' + str(len(data))
    size = 'Diameter ' + str(np.round((data[0,2] * 1.22 * 1e6), 2))
    fig.tight_layout()
    plt.text(0, 6.47 , size, horizontalalignment='center', 
             verticalalignment='center')
    plt.text(0, -0.615, text, horizontalalignment='center', 
             verticalalignment='center')
    
    plt.savefig('stuck_particles_' + str(np.round((data[0,2] * 1.22 * 1e6), 2)) + '.png', dpi=150)
    plt.show()
    
start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))