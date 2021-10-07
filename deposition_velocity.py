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
path = '/home/akim/coding/data/room/thatcher_deposition/'

# for i in range(1,5):
#     experiment = np.genfromtxt(path + 'image_' + str(i) + '.dat')
#     experiment[:,1] = experiment[:,1] * 0.1
#     np.savetxt('image_' + str(i) + '.dat', experiment)

bl = np.asarray([[3.63e-7, 9.91e-9,8.85e-06,9.85E-06],[6.77E-06, 7.35E-30, 2.06E-06, 9.36E-06],[1.44E-05, 3.46E-23, -5.62E-06, 9.26E-06],[5.44E-05, 3.49E-24, -4.60E-05, 8.84E-06],[2.12E-04, 3.14E-24, -2.05E-04, 7.77E-06]])


fig, axs = plt.subplots(5, figsize=(5,20))

for i in range(5):
    experiment = np.genfromtxt(path + 'image_' + str(i) + '.dat')
    experiment[:,1] = experiment[:,1]
    dl = (experiment[0,1],experiment[0,1])
    xl = (0,4)
    # experiment = np.delete(experiment,(10), axis=0)
    simulation = np.genfromtxt(path + 'sim_' + str(i) + '.dat')
    alex = np.genfromtxt(path + 'alex.dat')
    num_rows, num_cols = simulation.shape
    
    hot_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == -0.5]
    cold_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == 0.5]
    cold_ceiling = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == 0.5]
    hot_floor = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == -0.5]
    
    t = max(simulation[:,1]) - min(simulation[:,1])
    
    vd_cw = len(cold_wall)/55000 * 1/t * 1.10164
    vd_cc = len(cold_ceiling)/55000 * 1/t * 1.10164
    vd_hw = len(hot_wall)/55000 * 1/t * 1.10164
    vd_hf = len(hot_floor)/55000 * 1/t * 1.10164
    print(vd_cw,vd_cc, vd_hw, vd_hf)
    walls = 'hot floor         hot wall         cold ceiling       cold wall'
    # Left01,Right01,Floor01,Ceiling01,Back01,Fore01 = 0, 5.1294e-06, 0, 6.104e-06, 9.2329e-07, 2.5647e-07
    
    alex1 = np.array(((0, alex[i,2]),(1, alex[i,2])))
    alex2 = np.array(((1, alex[i,0]),(2, alex[i,0])))
    alex3 = np.array(((2, alex[i,3]),(3, alex[i,3])))
    alex4 = np.array(((3, alex[i,1]),(4, alex[i,1])))
    sim1 = np.array(((0,vd_hf),(1,vd_hf)))
    sim2 = np.array(((1,vd_hw),(2,vd_hw)))
    sim3 = np.array(((2,vd_cc),(3,vd_cc)))
    sim4 = np.array(((3,vd_cw),(4,vd_cw)))
    xticks = np.linspace(0,4,5)
    xlabels  = np.linspace(0.5,3.5,4)
    
    hf = np.asarray([[0,bl[i][0]],[1,bl[i][0]]])
    hw = np.asarray([[1,bl[i][1]],[2,bl[i][1]]])
    cs = np.asarray([[2,bl[i][2]],[3,bl[i][2]]])
    cw = np.asarray([[3,bl[i][3]],[4,bl[i][3]]])

    axs[i].plot(experiment[:,0], experiment[:,1],'ro', markersize = 2)
<<<<<<< HEAD
    axs[i].plot(hf[:,0], hf[:,1], 'm-')
    axs[i].plot(hw[:,0], hw[:,1], 'm-')
    axs[i].plot(cs[:,0], cs[:,1], 'm-')
    axs[i].plot(cw[:,0], cw[:,1], 'm-')
    axs[i].plot(sim1[:,0], sim1[:,1], 'b-')
    axs[i].plot(sim2[:,0], sim2[:,1], 'b-')
    axs[i].plot(sim3[:,0], sim3[:,1], 'b-')
    axs[i].plot(sim4[:,0], sim4[:,1], 'b-')
=======
    axs[i].plot(alex1[:,0], alex1[:,1], 'co-')
    axs[i].plot(alex2[:,0], alex2[:,1], 'co-')
    axs[i].plot(alex3[:,0], alex3[:,1], 'co-')
    axs[i].plot(alex4[:,0], alex4[:,1], 'co-')
    axs[i].plot(sim1[:,0], sim1[:,1], 'b--')
    axs[i].plot(sim2[:,0], sim2[:,1], 'b--')
    axs[i].plot(sim3[:,0], sim3[:,1], 'b--')
    axs[i].plot(sim4[:,0], sim4[:,1], 'b--')
>>>>>>> 0c56024e0937d04a4d45f6dc31f8d346fd616815
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
<<<<<<< HEAD
plt.savefig('particle_deposition_rBu23.png', dpi=150)
=======
plt.savefig('particle_deposition_alex.png', dpi=150)
>>>>>>> 0c56024e0937d04a4d45f6dc31f8d346fd616815
plt.show()

start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))