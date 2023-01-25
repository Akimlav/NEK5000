#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 13 13:24:13 2021

@author: akimlavrinenko
"""
import matplotlib.pyplot as plt
import numpy as np

dirPath = '/Users/akimlavrinenko/Documents/coding/data/room_data/1_particle_coords/'

# fig, axs = plt.subplots(7, figsize=(5, 15))
for i in range(3,4):
    data = np.genfromtxt(dirPath + 'ps' + str(i) + '_trajectory.dat')
    print(len(data))
    for j in range(len(data)):
        plt.plot(data[j,1], data[j,2], 'ro')
        plt.xlim(-0.5, 0.5)
        plt.ylim(-0.5, 0.5)
        plt.show()
