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

path = '/home/akim/coding/data/room/thatcher_deposition/'


experiment = np.genfromtxt(path + 'image_0.dat')
experiment[:,1] = experiment[:,1] * 0.1
dl = (experiment[10,1],experiment[10,1])
xl = (0,4)
experiment = np.delete(experiment,(10), axis=0)
simulation = np.genfromtxt(path + 'sim_0.dat')

num_rows, num_cols = simulation.shape

hot_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == -0.5]
cold_wall = [simulation[i,:] for i in range (0, num_rows) if simulation[i,3] == 0.5]
cold_ceiling = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == 0.5]
hot_floor = [simulation[i,:] for i in range (0, num_rows) if simulation[i,4] == -0.5]

vd_cw = len(cold_wall)/55000 * 1.22/191.6
walls = 'hot floor         hot wall         cold ceiling       cold wall'

xticks = np.linspace(0,4,5)
xlabels  = np.linspace(0.5,3.5,4)
fig, axs = plt.subplots(2, figsize=(5,10))

axs[0].plot(experiment[:,0], experiment[:,1],'ro')
axs[0].plot(xl,dl, '--')
axs[0].set_yscale('log')
axs[0].set_xticks(xticks)
axs[0].set_xlim(0,4)
axs[0].grid(True)
axs[0].text(0.5, -0.08, walls, horizontalalignment='center',
            verticalalignment='center', transform=axs[0].transAxes)
plt.show()

start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))