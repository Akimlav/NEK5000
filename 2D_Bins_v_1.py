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
from NEK5000_func_lib import particleCoordsNew
from time import time
start_time = time()

#coords of box corners
# data = particleCoords('./', 'fbalance00001.3D', 0)
# num_rows, num_cols = data.shape
print('path to working folder')
# path = input() + '/'
path = '../fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()
#params
step = 3 # file step
nx = 4 #number of the bins
num_ps = 5
axis_count = 3
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
hui = []
filtered = []
fff = np.zeros(5)
l = []

ps_index = []


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
    

print('It was: %.3f seconds'  % (time() - start_time))
print('Reading data!')
start_time2 = time()
for file in fileList:
    t, a = particleCoordsNew (path, file)
    for ps in range(0,num_ps):
        a_np = np.asarray(a[ps])
        data = a_np[ps_index[ps]]
        num_rows, num_cols = data.shape
        for axis in range(axis_count):
            for j in range(0,len(box_node)):
                xb = [data[k,:] for k in range (0, num_rows) if data[k, axis] > box_coords[j][axis] and data[k,axis] < box_coords[j+1][axis]]
                if len(xb) == 0:
                    xb = []
                elif len(xb) > 0:
                    print('working...')
                for i in range(0,len(box_node)):
                    np_xb = np.asarray(xb)
                    if axis < 2:
                        yb = [np_xb[k,:] for k in range (0, len(np_xb)) if np_xb[k, axis+1] > box_coords[i][axis] and np_xb[k,axis+1] < box_coords[i+1][axis]]
                    else:
                        yb = [np_xb[k,:] for k in range (0, len(np_xb)) if np_xb[k, axis-2] > box_coords[i][axis] and np_xb[k,axis-2] < box_coords[i+1][axis]]
                    l.append(np.asarray(yb))
                    p_count.append(len(yb))

                    box_count = [p_count[z:z+(nx**2)] for z in range(0, len(p_count), (nx**2))]
                    t_count = [box_count[z:z+axis_count] for z in range(0, len(box_count), axis_count)]
                    xyz_count = [t_count[z:z+num_ps] for z in range(0, len(t_count), num_ps)] #xyz_count[file][ps][axis][box]
                    time_array.append(np.round((t - 0.1628499834108E+03), 4))
                    t_1 = [time_array[z:z+(nx**2)] for z in range(0, len(time_array), (nx**2))]
                    t_2 = [t_1[z:z+axis_count] for z in range(0, len(box_count), axis_count)]
                    t_3 = [t_2[z:z+num_ps] for z in range(0, len(t_count), num_ps)] #xyz_count[file][ps][axis][box]

print('It was: %.3f seconds'  % (time() - start_time2))
start_time3 = time()
print('Restructurizing data')
t_box_array = []

for axis in range(axis_count):
    for ps in range(0,num_ps):
        for box in range(0,len(box_node)**2):
            for file in fileList:
                tb = [t_3[fileList.index(file)][ps][axis][box], xyz_count[fileList.index(file)][ps][axis][box]]
                # print('axis', axis, 'ps', ps, 'box', box, file, '|', tb)
                t_box_array.append(tb)

tb1 = [t_box_array[z:z+(len(fileList)*nx**2*num_ps)] for z in range(0, len(t_box_array), (len(fileList)*nx**2*num_ps))]#axis
tb2 = []
tb3 = []
tb4 = []
tb5 = []
for i in range(axis_count):
    tb2 = [tb1[i][z:z+(nx**2*len(fileList))] for z in range(0, len(tb1[i]), (nx**2*len(fileList)))]
    tb3.append(tb2)
    
for i in range(axis_count):
    for j in range(num_ps):
        tb4 = [tb3[i][j][z:z+len(fileList)] for z in range(0, len(tb3[i][j]), len(fileList))]
        tb5.append(tb4)

tb6 = []
tb6 = [tb5[z:z+num_ps] for z in range(0, len(tb5), num_ps)]


print('It was: %.3f seconds'  % (time() - start_time3))
# box_list = [[t_box_array[num], t_box_array[num+4]] for num in range(4)]
# box_list = [[t_box_array[num], t_box_array[num+ (nx**2*axis_count*num_ps)]] for num in range(nx**2*axis_count*num_ps)]

start_time4 = time()
legend = np.linspace(0, nx**2-1, nx**2, dtype = int)

for axis in range(axis_count):
    for ps in range(num_ps):
        fig = plt.figure(figsize=(4.5,3), dpi=100)
        fontP = FontProperties()
        fontP.set_size('xx-small')
        for  box in range (nx**2):
            b = np.asarray(tb6[axis][ps][box])
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
            plt.ylim(0, max(p_count))
        plt.savefig(axis_title + '_p_size ' + str(ps) + '.png', dpi=200)
        # plt.show()
print('It was: %.3f seconds'  % (time() - start_time4))
print('All it was: %.3f seconds'  % (time() - start_time))
