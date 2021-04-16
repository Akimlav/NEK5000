#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 14 18:03:19 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from NEK5000_func_lib import particleCoordsNew, fast_scandir, listfile, find_in_list_of_list
from time import time
import itertools
from scipy.stats import norm
import statistics as st
from matplotlib.font_manager import FontProperties

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def estimate_coef(x, y):
    # number of observations/points
    n = np.size(x)
 
    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)
 
    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y*x) - n*m_y*m_x
    SS_xx = np.sum(x*x) - n*m_x*m_x
 
    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1*m_x
 
    return (b_0, b_1)


start_time = time()

dirpath = '/Users/akimlavrinenko/Documents/coding/data/test_data'
fold_name = 'fbala'
# dirpath = '/home/afabret/data/room_deposition/production_run/'
# fold_name = 'roomBackUp'

#params
n = 10 #number of the bins

x0 = -0.5
y0 = -0.5
z0 = -0.5

box_coords = [[0 for x in range(n+1)] for x in range(3)]
box_node = [[0 for x in range(n)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

delta = 1/n

for j in range(0,3):
    for i in range(1,n+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2

box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))
box_node = np.round(box_node, 3)
legend = box_node.tolist()


cm = plt.get_cmap('tab20')

sL = []
fig, axs = plt.subplots(3,figsize=(7, 12))
fontP = FontProperties()
fontP.set_size('xx-small')

for i in range(10):
    A = np.genfromtxt('/Users/akimlavrinenko/Documents/coding/data/sigma/sigma_data_'+ str(i) + '.dat')
    
    fp = 0
    lp = 24
    ref_point_s = find_nearest(A[:,0], fp)
    ref_point_e = find_nearest(A[:,0], lp)
    rp = [ref_point_s, ref_point_e]
    ind = np.where(np.isin(A[:,0], rp))
    
    B = A[int(ind[0][0]):int(ind[0][1])+1]
    Blog = np.log(B)
    Blog = np.delete(Blog, (0), axis=0)
   
    b = estimate_coef(Blog[:,0], Blog[:,1])
    y_pred = b[0] + b[1]*Blog[:,0]
    
    slope = abs((y_pred[-1] - y_pred[0])/(Blog[-1][0] - Blog[0][0]))
    angle = np.degrees(np.arctan((slope)))
    sL.append(angle)
    axs[0].plot(np.log(A[:,0]),np.log(A[:,1]),'-', color = cm(i),linewidth=0.5)
    axs[1].plot(Blog[:,0], Blog[:,1],'--', color = cm(i),linewidth=0.5,markersize=3)
    axs[1].plot(Blog[:,0], y_pred, color = cm(i) ,linewidth=0.7)
    print(i, len(y_pred))
    
    # plt.plot(B[:,0], np.log(B[:,1]))

    # plt.plot(B[:,0], y_pred)


cd = np.linspace(0.0865, 1.65, 10)

axs[2].plot(cd, sL, 'o-')
axs[2].set_xticks(cd)
axs[2].set_xticklabels(legend,rotation=90)
axs[0].grid(True)
axs[1].grid(True)
axs[0].set_xlabel('log time')
axs[0].set_ylabel('log sigma')
axs[0].set_title('all data')
axs[1].set_xlabel('log time')
axs[1].set_ylabel('log sigma')
axs[1].set_title('linear regression')
axs[2].grid(True)
axs[2].set_xlabel('sphere center')
axs[2].set_ylabel('slope angle')
# axs[2].set_title('')
fig.tight_layout()
fig.legend(legend, title='location', bbox_to_anchor=(0.9, 0.67), prop=fontP)
plt.savefig('slope.png', dpi=200)
plt.show()



