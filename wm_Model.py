#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 14:13:08 2022

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt

dp = [259, 444, 354, 989, 4189]

t_sim = 1412.7545005398442
H = 3.1475
V = 320
ACH = 10
vd = dp[0]/55000 * 1/t_sim
lwm = vd/H #+ ACH/3600
def nwm (vd,t,H, lwm):
    return 1/(lwm*H**3) *(1 - np.exp(-lwm*t))

resList = []

# for p in range(len(dp)):
for p in range(1):
    for t in range(900):
        n = nwm(vd,t,H, lwm)
        nInf = 1/(lwm*H)
        res = n /nInf
        # print (res)
        resList.append(res)
        
        
tPlt = np.linspace(1,900,900)
plt.plot(tPlt, resList)


