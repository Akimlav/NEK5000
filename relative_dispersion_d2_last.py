#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 20:57:37 2021

@author: akimlavrinenko
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import find_nearest, estimate_coef
#params
nn = 10 #number of the bins
num_ps = 5
step = 1
x0 = -0.5
y0 = -0.5
z0 = -0.5

path1 =  '/Users/akimlavrinenko/Documents/coding/data/room_data/each_size_sphere_traj/sphr2/'

path = '/Users/akimlavrinenko/Documents/coding/data/room_data'

lll = []



for ps in range(num_ps):
    for n in range(nn):
        data = np.genfromtxt(path1 + '/sphr_trj2_c_' + str(n) + '_ps_' + str(ps) + '.dat')
        print('number', n, np.shape(data), '/sphr_trj2_c_' + str(n) + '_ps_' + str(ps) + '.dat')
        x = data[::step,1::3]
        y = data[::step,2::3]
        z = data[::step,3::3]
        time = data[::step, 0]
        d2List = []
        # plt.plot(x,y)
        s=0
        d2 = 0
        for t in range(len(time)):
            ll = []
            for num in range(len(x[0,:])):
                xd = [(number - x[t,num])**2 for number in x[t,:]]
                yd = [(number - y[t,num])**2 for number in y[t,:]]
                zd = [(number - z[t,num])**2 for number in z[t,:]]
                ld = [xd,yd,zd]
                sd = [sum(s) for s in zip(*ld)] #x+y+z distance
                ll.append(sd)
                s = [sum(i) for i in zip(*ll)] #sum of x[0][0] + x[1][0]...
            f = np.math.factorial(len(x[0,:]))/(2*(np.math.factorial(len(x[0,:])-2)))
            d2 = sum(s)/f
            d2List.append(d2)
        lll.append(d2List)

    arr = np.asarray(lll)
    arr = arr.T
    time  = np.reshape(time, (-1, 1))
    res = np.concatenate((time,arr), axis=1)
    print(np.shape(res))
np.savetxt('d2.dat', res)



d2f = np.genfromtxt('d2.dat')
for i in range(0,5):
    print((i*10)+5)
    plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+6]), 'r')
    plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+1]), 'b')
    plt.plot(np.log10(d2f[:,0]), np.log10(d2f[:,(i*10)+10]), 'g')
plt.show()
