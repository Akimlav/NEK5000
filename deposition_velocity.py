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
path = '/Users/akimlavrinenko/Documents/coding/data/room_data/thatcher_deposition/'
# for i in range(1,5):
#     experiment = np.genfromtxt(path + 'image_' + str(i) + '.dat')
#     experiment[:,1] = experiment[:,1] * 0.1
#     np.savetxt('image_' + str(i) + '.dat', experiment)




fig, axs = plt.subplots(5, figsize=(5,20))
for i in range(5):
    experiment = np.genfromtxt(path + 'image_' + str(i) + '.dat')
    experiment[:,1] = experiment[:,1]
    dl = (experiment[0,1],experiment[0,1])
    xl = (0,4)
    experiment = np.delete(experiment,(10), axis=0)
    simulation = np.genfromtxt(path + 'sim_' + str(i) + '.dat')
    
    num_rows, num_cols = simulation.shape
    
    hot_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == -0.5]
    cold_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == 0.5]
    cold_ceiling = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == 0.5]
    hot_floor = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == -0.5]
    
    t = 198.5
    
    vd_cw = len(cold_wall)/55000 * 1/t * 1.10164
    vd_cc = len(cold_ceiling)/55000 * 1/t * 1.10164
    vd_hw = len(hot_wall)/55000 * 1/t * 1.10164
    vd_hf = len(hot_floor)/55000 * 1/t * 1.10164
    print(vd_cw,vd_cc, vd_hw, vd_hf)
    walls = 'hot floor         hot wall         cold ceiling       cold wall'
    
    sim1 = np.array(((0,vd_hf),(1,vd_hf)))
    sim2 = np.array(((1,vd_hw),(2,vd_hw)))
    sim3 = np.array(((2,vd_cc),(3,vd_cc)))
    sim4 = np.array(((3,vd_cw),(4,vd_cw)))
    xticks = np.linspace(0,4,5)
    xlabels  = np.linspace(0.5,3.5,4)

    
    axs[i].plot(experiment[:,0], experiment[:,1],'ro', markersize = 2)
    axs[i].plot(sim1[:,0], sim1[:,1], 'b-')
    axs[i].plot(sim2[:,0], sim2[:,1], 'b-')
    axs[i].plot(sim3[:,0], sim3[:,1], 'b-')
    axs[i].plot(sim4[:,0], sim4[:,1], 'b-')
    axs[i].plot(xl,dl, '--')
    axs[i].set_yscale('log')
    axs[i].set_xticks(xticks)
    axs[i].set_xlim(0,4)
    axs[i].set_ylim(10e-10, 1.5*10e-04)
    axs[i].set_title('diameter ' + str(np.round((simulation[0,2] * 1.22 * 1e6), 2) ) + ' \u03BC' + 'm')
    axs[i].grid(True)
axs[4].text(0.5, -4.8, walls, horizontalalignment='center',
                verticalalignment='center', transform=axs[0].transAxes)
fig.tight_layout()
plt.savefig('particle_deposition.png', dpi=150)
plt.show()

start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))