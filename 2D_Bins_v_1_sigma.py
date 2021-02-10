#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:25:01 2021

@author: akimlavrinenko
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from os import listdir
from NEK5000_func_lib import particleCoordsNew, slice_per
from time import time

start_time = time()

print('path to working folder')
# path = input() + '/'
path = '../fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()

#params
step = 3  # file step
nx = 5 #number of the bins
num_ps = 5
axis_count = 1
fileList = fileList[0::step]
x0 = -0.5
y0 = -0.5
z0 = -0.5
center = np.asarray([0.25,0.25,0])
radius = 0.1

box_coords = [[0 for x in range(nx+1)] for x in range(3)]
box_node = [[0 for x in range(nx)] for x in range(3)]

box_coords[0][0] = x0
box_coords[1][0] = y0
box_coords[2][0] = z0

delta = 1/nx
len_filtered = []
p_count = []
time_array = []
bins = []
filtered = []
fff = np.zeros(5)
l = []
ps_index = []
t_c = []

for j in range(0,3):
    for i in range(1,nx+1):
        box_coords[j][i] = box_coords[j][i-1] + delta
        box_node[j][i-1] = (box_coords[j][i-1] + box_coords[j][i])/2
            
xlabel = np.linspace(0, nx**2, (nx**2)+1)
box_coords = np.asarray(np.transpose(box_coords))
box_node = np.asarray(np.transpose(box_node))

t0, a0 = particleCoordsNew (path, fileList[0])
for ps in range(num_ps):
    aa0 = np.asarray(a0[ps])
    for j in range(len(aa0)):
        r1 = ((aa0[j,0] - center[0])**2 + (aa0[j,1] - center[1])**2 + (aa0[j,2] - center[2])**2)**0.5
        if r1 <= radius:
            filtered.append(aa0[j,:])
    len_filtered.append(len(filtered))
    if len(len_filtered) == 1:
        fff[ps] = len_filtered[ps]
    else:
        fff[ps] = len_filtered[ps] - len_filtered[ps-1]
    fff = fff.astype(int)
    ps_filtered = []
    count = 0
    for size in (fff):
        ps_filtered.append([filtered[i+count] for i in range(size)])
        count += size
    index = np.where(np.isin(aa0[:,1], np.asarray(ps_filtered[ps])))
    ps_index.append(index[0])
    
start_time2 = time()   
for file in fileList:
    t, a = particleCoordsNew (path, file)
    t = np.round((t - 0.1628499834108E+03), 3)
    for ps in range(0,num_ps):
        a_np = np.asarray(a[ps])
        data = a_np[ps_index[ps]]
        num_rows, num_cols = data.shape
        # fig = plt.figure(figsize=(5, 5))
        for axis in range(axis_count):
            if axis < 2:
                xedges = box_coords[:,axis]
                yedges = box_coords[:,axis+1]
                H, xedges, yedges = np.histogram2d(data[:,axis], data[:,axis+1], bins=(xedges, yedges))
            else:
                xedges = box_coords[:,axis]
                yedges = box_coords[:,axis-2]
                H, xedges, yedges = np.histogram2d(data[:,axis], data[:,axis-2], bins=(xedges, yedges))
            H = H.T
            t_c.append(H)
            time_array.append(t)
            
            xedges = box_coords[:,0]
            yedges = box_coords[:,1]
            x = data[:,0]
            y = data[:,1]
            H, xedges, yedges = np.histogram2d(x, y, bins=(xedges, yedges))
            if axis == 0:
                axis_title = 'x'
            elif axis == 1:
                axis_title = 'y'
            elif axis == 2:
                axis_title = 'z'
                
            # title = axis_title + ' axis, ' + str(ps) + ' ps, ' + str(t) + ' time'
            # ax = fig.add_subplot(131, title=title,)
            # plt.imshow(H, interpolation='nearest', origin='lower') #,
            #             #extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]])
            # plt.tight_layout()
            # plt.savefig('fig_' + axis_title + '_axis_' + str(ps) +'_ps_' + str(t) + '_t.png', dpi=200)
            
            
print('Reading all data was: %.3f seconds' % (time() - start_time2))   
       
start_time3 = time()

tb1 = [t_c[z:z+(axis_count*num_ps)] for z in range(0, len(t_c), (axis_count*num_ps))]
tb2 = []
tb3 = []

for i in range(len(fileList)):
    tb2 = [tb1[i][z:z+axis_count] for z in range(0, len(tb1[i]), axis_count)]
    tb3.append(tb2)

t_1 = [time_array[z:z+(axis_count*num_ps)] for z in range(0, len(t_c), (axis_count*num_ps))]
t_2 = []
t_3 = []                   
for i in range(len(fileList)):
    t_2 = [t_1[i][z:z+axis_count] for z in range(0, len(t_1[i]), axis_count)]
    t_3.append(t_2)

aa = []
for axis in range(axis_count):
    for ps in range(0,num_ps):
            for file in fileList:
                x, y = np.shape(tb3[0][0][0])
                for i in range(x):
                    for j in range(y):
                        box = tb3[fileList.index(file)][ps][axis][i][j]
                        tt = t_3[fileList.index(file)][ps][axis]
                        t_b = [tt, box]
                        aa.append(t_b)
                        
aa1 = [aa[z:z+(len(fileList)*nx**2*num_ps)] for z in range(0, len(aa), (len(fileList)*nx**2*num_ps))]#axis
aa2 = []
aa3 = []

for i in range(axis_count):
    aa2 = [aa1[i][z:z+(nx**2*len(fileList))] for z in range(0, len(aa1[i]), (nx**2*len(fileList)))]
    aa3.append(aa2)

xx = []
xxx = []

for axis in range(axis_count):
    for ps in range(num_ps):
        xx = slice_per(aa3[axis][ps], nx**2)
        xxx.append(xx)

x1 = [xxx[z:z+num_ps] for z in range(0, len(xxx), num_ps)]

print('Restructurizing was: %.3f seconds' % (time() - start_time3))

start_time4 = time()
legend = np.linspace(0, nx**2-1, nx**2, dtype = int)

for axis in range(axis_count):
    for ps in range(num_ps):
        fig = plt.figure(figsize=(4.5,3), dpi=100)
        fontP = FontProperties()
        fontP.set_size('xx-small')
        for  box in range (nx**2):
            b = np.asarray(x1[axis][ps][box])
            plt.plot(b[:,0],b[:,1], '-')
            plt.legend(legend, title='box', bbox_to_anchor=(1.13, 1),loc='upper right', prop=fontP)
            if axis == 0:
                axis_title = 'x'
            elif axis == 1:
                axis_title = 'y'
            elif axis == 2:
                axis_title = 'z'
            plt.title('axis - ' + axis_title +', particle size number - %d' %ps)
            plt.xlabel('time')
            plt.ylabel("number of particles in the bin")
            plt.grid(True)
            plt.ylim(0, np.amax(t_c))
        # plt.savefig(axis_title + '_p_size_' + str(ps) + '.png', dpi=200)
        # plt.show()
        
sss = []

for axis in range(axis_count):
    for ps in range(num_ps):
        M = fff[ps]/ nx**2
        for file in fileList:
            ss = 0
            s = 0
            sigma = 0
            for i in range (nx**2):
                s = (x1[axis][ps][i][fileList.index(file)][1] - M)**2
                ss = ss + s
                print(x1[axis][ps][i][fileList.index(file)][1], s, ss)
                print('_________________________________________________')
            sigma = ss**0.5/M
            print('sigma', sigma)
            sss.append(sigma)

s1 = [sss[z:z+(len(fileList)*num_ps)] for z in range(0, len(sss), (len(fileList)*num_ps))]
s3 = []
for axis in range(axis_count):
    s2 =  [s1[axis][z:z+(len(fileList))] for z in range(0, len(s1[axis]), (len(fileList)))]
    s3.append(s2)

legend_sigma = np.linspace(0,num_ps-1,num_ps)
for axis in range(axis_count):
    
    fig = plt.figure(figsize=(4.5,3.5), dpi=100)
    fontP = FontProperties()
    fontP.set_size('xx-small')
    for ps in range(num_ps):
        # print(ps)
        plt.plot(b[:,0],s3[axis][ps], '-')
        plt.legend(legend_sigma, title='ps', bbox_to_anchor=(1.13, 1),loc='upper right', prop=fontP)
        if axis == 0:
            axis_title = 'x'
        elif axis == 1:
            axis_title = 'y'
        elif axis == 2:
            axis_title = 'z'
        plt.title('axis - ' + axis_title)
        plt.xlabel('time')
        plt.ylabel("sigma")
        plt.grid(True)
        plt.ylim(0, np.amax(sss))
    plt.savefig(axis_title + '_sigma.png', dpi=200)
    plt.show()

print('Plotting was: %.3f seconds' % (time() - start_time4))
print('All it was: %.3f seconds'  % (time() - start_time))

