#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 17:00:01 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from NEK5000_func_lib import particleCoordsForces, readParticleFile


path = '/Users/akimlavrinenko/Documents/coding/data/room_data/'
fileName = 'fbalance01937.3D'


t, f = particleCoordsForces(path, fileName)
dist = -0.5 + 2e-3
ps = [0.5,0.7,1.3]
for s in range(len(ps)):
    forces = []
    ps0 = np.asarray(f[s])
    y = ps0[:,1] 
    ind = np.where(np.logical_and(y >= -0.5, y <= dist))
    a = ps0[ind[0]]
    drag = []
    thph = []
    lift = []
    brow = []
    browVert = []
    dragVert = []
    for j in range(len(a)):
        magDrag = (a[j,3]**2 + a[j,4]**2 + a[j,5]**2)**0.5
        magThph = (a[j,7]**2 + a[j,8]**2 + a[j,9]**2)**0.5
        magLift = (a[j,10]**2 + a[j,11]**2 + a[j,12]**2)**0.5
        magBrow = (a[j,13]**2 + a[j,14]**2 + a[j,15]**2)**0.5
        drag.append(magDrag)
        thph.append(magThph)
        lift.append(magLift)
        brow.append(magBrow)
        browVert.append(a[j,14])
        dragVert.append(a[j,4])
    forces.append([np.mean(drag),np.mean(abs(a[:,6])), np.mean(thph), np.mean(lift), np.mean(brow)])
    
    forces = np.asarray(forces)
    
    fig, axs = plt.subplots(2,figsize=(5, 7))
    axs[0].hist(dragVert,3000, label='thph')
    axs[1].hist(browVert, 3000, label='brow')
    # axs[1].plot(brow, 'm', label='brownian')
    # axs[1].plot(drag, 'c', label='drag')
    # axs[1].set_xlabel('particle number')
    axs[1].set_ylabel('lift')
    axs[0].set_xlim(-500,500)
    axs[1].set_xlim(-500,500)
    # axs[1].set_xticks(xticks)
    axs[1].grid(True)
    axs[0].set_xlabel('thermophoresis magnitude')
    axs[0].set_ylabel('')
    # axs[0].set_xticks(xticks)
    fig.suptitle('diameter ' + str(ps[s]) +  ' \u03BC' + 'm' + ',bin from -0.5 to ' + str(dist))
    axs[0].grid(True)
    fig.legend(bbox_to_anchor=(0.93,0.18))
    fig.tight_layout()
    plt.savefig('diameter_' + str(ps[s]) + '_y_' + str(abs(dist)) + '.png', dpi = 100)
    plt.show()
