#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 19:34:09 2022

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
import pylab
#0.7 um particles

t0 = 0
t1 = 1.4e3
cc = np.asarray((234,408,318,965,4169))

C0 = np.log(55000)/np.log(55000)
Ct = np.log(55000-354)/np.log(55000)

for c in cc:
    gamma = ((np.log(55000) - np.log(55000-c)) / t1)
    print(gamma, 1/gamma)

Cgamma = C0*np.exp(gamma*2000)

kim05 = [0,1,2000,0.85]
kim05 = np.reshape(kim05,(2,2))

# plt.plot()
# plt.plot()
# plt.ylim(0,1)
# plt.xlim(0,2000)

fig = plt.figure(figsize=(5, 5))
ax = fig.add_subplot()
N0 = 55000
Nt = 55000-354
# ax.plot((t0,1400),(C0,Ct,), color='blue', lw=2)
# ax.plot((t0,2000),(C0,Cgamma,), 'b--', lw=2)
# ax.plot(kim05[:,0],kim05[:,1], color='red', lw=2)
ax.plot((t0,1400),(N0,Nt,), color='blue', lw=2)
# ax.set_yscale('log')
ax.set_xlim(0,2000)
# ax.set_ylim(0, 55500)
plt.show()

# ax.plot((t0,t1),(np.log(55000),np.log(55000-354)), color='blue', lw=2)
# # ax.plot(kim05[:,0],kim05[:,1], color='red', lw=2)
# ax.set_yscale('log')
# ax.set_xlim(0,2000)
# # ax.set_ylim(0.3, 1.1)
# plt.show()
dp = [259, 444, 354, 989, 4189]
# Diameter01 =  259
# Diameter05 = 444
# Diameter07 = 354
# Diameter13 =  989
# Diameter25 =  4189
t = 1412.7545005398442
for p in dp:
    print(p/55000 * 1/t)


