#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:09:20 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from NEK5000_func_lib import particleCoordsForces, readParticleFile


path = '/Users/akimlavrinenko/Documents/coding/data/room_data/'
fileName = 'fbalance01937.3D'


t, f = particleCoordsForces(path, fileName)

ps = [0.1,0.5,0.7,1.3,2.5]
for s in range(len(ps)):
    check = 0
    forces = []
    ps0 = np.asarray(f[s])
    lvl = np.linspace(-0.5, 0.5,1001)
    xticks = np.linspace(0,9,10)
    for i in range(1,len(lvl)):
        y = ps0[:,1]
        ind = np.where(np.logical_and(y >= lvl[i-1], y <= lvl[i]))
        a = ps0[ind[0]]
        check += len(a)
        drag = []
        thph = []
        lift = []
        brow = []
        for j in range(len(a)):
            magDrag = (a[j,3]**2 + a[j,4]**2 + a[j,5]**2)**0.5
            magThph = (a[j,7]**2 + a[j,8]**2 + a[j,9]**2)**0.5
            magLift = (a[j,10]**2 + a[j,11]**2 + a[j,12]**2)**0.5
            magBrow = (a[j,13]**2 + a[j,14]**2 + a[j,15]**2)**0.5
            drag.append(magDrag)
            thph.append(magThph)
            lift.append(magLift)
            brow.append(magBrow)
        
        forces.append([np.mean(drag),np.mean(abs(a[:,6])), np.mean(thph), np.mean(lift), np.mean(brow)])
    print(check)
    forces = np.asarray(forces)
    
    fig, axs = plt.subplots(2,figsize=(7, 7))
    axs[0].plot(forces[:,1], 'y', label='gravity')
    axs[0].plot(forces[:,2], 'g', label='thph')
    axs[0].plot(forces[:,3], 'k', label='lift')
    axs[1].plot(forces[:,4], 'm', label='brownian')
    axs[1].plot(forces[:,0], 'c', label='drag')
    axs[1].set_xlabel('bin in y direction')
    axs[1].set_ylabel('force')
    # axs[1].set_xticks(xticks)
    axs[1].grid(True)
    axs[0].set_xlabel('bin in y direction')
    axs[0].set_ylabel('force')
    # axs[0].set_xticks(xticks)
    fig.suptitle('diameter ' + str(ps[s]) +  ' \u03BC' + 'm')
    axs[0].grid(True)
    fig.legend()
    fig.tight_layout()
    plt.savefig('diameter_' + str(ps[s]) + '.png', dpi = 100)
    plt.show()
