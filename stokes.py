#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 11:58:12 2022

@author: akimlavrinenko
"""

import numpy as np


dp = [0.1e-6,0.5e-6, 0.7e-6, 1.3e-6, 2.5e-06] #particle diameter

rhop = 1350 #particle density
rhof = 1.3 #fluid density
us =0.428 #velocity scale
Ls = 3.14 #lenght scale
lamb = 6.8e-8 #free mean path
muf = 1.57e-5 #dinamic viscosity of the fluid
for d in dp:
    Kn =  2*lamb/(d/Ls)
    Cc = 1 + Kn*(1.205*np.e**(-0.0026/Kn) + 0.425*np.e**(-0.7400/Kn))
    St = (d**2*rhop*us*Ls)/(18*Cc*muf)
    print(St)
