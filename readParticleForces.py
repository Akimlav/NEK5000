#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:09:20 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from NEK5000_func_lib import readParticleFile
# from postProcess_NEK5000_v1_3_sq import particleCoords

path = '/Users/akimlavrinenko/Documents/coding/data/room_data/'
fileName = 'fbalance01937.3D'



def particleForces (path, fileName):
    time,pdata = readParticleFile(str(path) + str(fileName))
    
    allData = []
    
    for ibatch in range(0,pdata.shape[0]):
        for ipart in range(0,pdata.shape[2]):
            for ps in range(0,pdata.shape[1]): 
            
              vel = pdata[ibatch,ps,ipart]['up']
              rest = pdata[ibatch,ps,ipart]['rest']
              xpart = pdata[ibatch,ps,ipart]['xp']
              A = np.concatenate((xpart, vel, rest),axis = 0)
              allData.append(A)
    
        forcesp = [allData[z:z+pdata.shape[2]] for z in range(0, len(allData), pdata.shape[2])]
        return(time, forcesp)




t, f = particleForces(path, fileName)


rhoP = 1350
rhoF = 1.3
us = 0.427
ls = 1.22
allData = []
meanForces = []
for wall in range(2):
    print(wall)
    for ps in f:
        partData = np.asarray(ps)
        lvl = np.linspace(-0.5, 0.5,101)
        for i in range(1,len(lvl)):
            y = partData[:,1-wall]
            ind = np.where(np.logical_and(y >= 0.495, y <= 0.5))
            a = partData[ind[0]]
    
            drag = []
            thph = []
            lift = []
            brow = []
            for j in range(len(a)):
                magDrag = (a[j,6]**2 + a[j,7]**2 + a[j,8]**2)**0.5
                magThph = (a[j,10]**2 + a[j,11]**2 + a[j,12]**2)**0.5
                magLift = (a[j,13]**2 + a[j,14]**2 + a[j,15]**2)**0.5
                magBrow = (a[j,16]**2 + a[j,17]**2 + a[j,18]**2)**0.5
                drag.append(magDrag)
                thph.append(magThph)
                lift.append(magLift)
                brow.append(magBrow)
            
        drag = np.asarray(drag)
        thph = np.asarray(thph)
        lift = np.asarray(lift)
        brow = np.asarray(brow)
        g = np.asarray(a[:,9])
        thphVert = a[:,11-wall]
        ng = -9.82*(1-rhoF/rhoP)* (ls/us**2)
        ngArr = np.full(len(a[:,0]),ng)
        allF = np.vstack((drag,thph, thphVert,lift,brow, g, ngArr)).T
        meanF = np.mean(allF, axis =0 )
        print(meanF)
        allData.append(meanF)
        plt.plot(a[:,0], a[:,1])
        plt.xlim(-0.5,0.5)
        plt.ylim(-0.5,0.5)
    plt.show()

allData = np.asarray(allData)
pSize = np.asarray((0.1, 0.5, 0.7, 1.3, 2.5,0.1, 0.5, 0.7, 1.3, 2.5))
pSize = pSize.reshape(10,1)
allData = np.concatenate((pSize, allData), axis = 1)

resToShow = np.vstack((allData[:,0],allData[:,2],allData[:,3],allData[:,6],allData[:,7])).T

    # plt.plot(thphVert)
    # plt.hist(thphVert, bins = 50)
    # plt.show()
        # meanForces = np.asarray(meanForces)
    
#     fig, axs = plt.subplots(2,figsize=(7, 7))
#     axs[0].plot(forces[:,1], 'y', label='gravity')
#     axs[0].plot(forces[:,2], 'g', label='thph')
#     axs[0].plot(forces[:,3], 'k', label='lift')
#     axs[1].plot(forces[:,4], 'm', label='brownian')
#     axs[1].plot(forces[:,0], 'c', label='drag')
#     axs[1].set_xlabel('bin in y direction')
#     axs[1].set_ylabel('force')
#     # axs[1].set_xticks(xticks)
#     axs[1].grid(True)
#     axs[0].set_xlabel('bin in y direction')
#     axs[0].set_ylabel('force')
#     # axs[0].set_xticks(xticks)
#     fig.suptitle('diameter ' + str(ps[s]) +  ' \u03BC' + 'm')
#     axs[0].grid(True)
#     fig.legend()
#     fig.tight_layout()
#     plt.savefig('diameter_' + str(ps[s]) + '.png', dpi = 100)
#     plt.show()

