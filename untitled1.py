#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  7 16:09:20 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import readParticleFile, particleForces, fast_scandir, listfile, find_in_list_of_list


path = '/Users/akimlavrinenko/Documents/coding/data/room_data/'
fileName = 'fbalance01910.3D'

# t, a = particleCoordsNew ('/Users/akimlavrinenko/Documents/coding/data/room_data/', 'fbalance01910.3D')

# time,pdata = readParticleFile(str(path) + str(fileName))

# aa = pdata[0][0][0][7][8]
# xpart = pdata[0,0,0]

t, f = particleForces(path, fileName)

# time,pdata = readParticleFile(str(path) + str(fileName))

# fp = []
        
# for ibatch in range(0,pdata.shape[0]):
#     for ipart in range(0,pdata.shape[2]):
#         for ps in range(0,pdata.shape[1]):
        
#           fpart = pdata[ibatch,ps,ipart][7]
#           fp.append(fpart)
        
# allp = [fp[z:z+pdata.shape[2]] for z in range(0, len(fp), pdata.shape[2])]
          