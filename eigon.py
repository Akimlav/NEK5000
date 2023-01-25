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
import itertools

start_time = time()

print('path to working folder')
# path = input() + '/'
# path = '/home/afabret/data/room_deposition/roomBackUp00002_new/'
path = './fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()

#params
step = 3 # file step
n = 4 #number of the bins
num_ps = 5
axis_count = 1
fileList = fileList[0::step]
x0 = -0.5
y0 = -0.5
z0 = -0.5
# center = np.asarray([0.4,0.4,0.0])
radius = 0.1

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
box_node = np.round(box_node, 2)
# legend = []
center_list = (list(itertools.product(box_node[:,0], box_node[:,1], box_node[:,2])))
center_list = [  np.round(elem,2) for elem in center_list]
center_list = center_list[0::1]
legend = box_node.tolist()
legend1 = str(legend[0])
marker_list = ['r-', 'y-', 'g-', 'c-', 'b-',]

    
t0, a0 = particleCoordsNew (path, fileList[0])
for k in range(len(box_node[:,0])):
    print(k)
    filtered = []
    ps_index = []
    len_filtered = []
    t_c = []
    fff = np.zeros(5)
    center = box_node[0,:]

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
            xedges = box_coords[:,0]
            yedges = box_coords[:,1]
            zedges = box_coords[:,2]
            H, edges = np.histogramdd(data, bins=(xedges, yedges, zedges))
            t_c.append([t, H])
    
    tb = [t_c[z:z+(num_ps)] for z in range(0, len(t_c), (num_ps))]
    
    print('Reading all data was: %.3f seconds' % (time() - start_time2))

A = np.zeros((n**3, n**3))

a =  tb[0][0][1].flat
a = list(a)
A[:,0] = a

t1, a1 = particleCoordsNew (path, fileList[0])
t2, a2 = particleCoordsNew (path, fileList[1])
ps1 = a1[0][ps_index[0][1]]
ps2 = a2[0][ps_index[0][1]]
plt.plot(ps1[0], ps1[1], 'ro')
plt.plot(ps2[0], ps2[1], 'co')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)


empty_lists = [ [] for _ in range(n**3) ]


for el in data:
    # print(el[0])
    if el[0] > box_coords[0][0] and el[0] < box_coords[1][0]:
        empty_lists[0].append(el)
    else:
        print('fuck!')


ind = np.sort(data, axis=0)
ind1 = np.argsort(data, axis=0)
print(data[153])
    
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]

def inside_test(points , cube3d):
    """
    cube3d  =  numpy array of the shape (8,3) with coordinates in the clockwise order. first the bottom plane is considered then the top one.
    points = array of points with shape (N, 3).

    Returns the indices of the points array which are outside the cube3d
    """
    b1,b2,b3,b4,t1,t2,t3,t4 = cube3d

    dir1 = (t1-b1)
    size1 = np.linalg.norm(dir1)
    dir1 = dir1 / size1

    dir2 = (b2-b1)
    size2 = np.linalg.norm(dir2)
    dir2 = dir2 / size2

    dir3 = (b4-b1)
    size3 = np.linalg.norm(dir3)
    dir3 = dir3 / size3

    cube3d_center = (b1 + t3)/2.0

    dir_vec = points - cube3d_center

    res1 = np.where( (np.absolute(np.dot(dir_vec, dir1)) * 2) > size1 )[0]
    res2 = np.where( (np.absolute(np.dot(dir_vec, dir2)) * 2) > size2 )[0]
    res3 = np.where( (np.absolute(np.dot(dir_vec, dir3)) * 2) > size3 )[0]

    return list( set().union(res1, res2, res3) )

c0 = [-0.5, -0.5, -0.5]
c1 = [-0.5, 0.0, -0.5]
c2 = [0.0, 0.0, -0.5]
c3 = [0.0, -0.5, -0.5]
c4 = [-0.5, -0.5, 0.0]
c5 = [-0.5, 0.0, 0.0]
c6 = [0.0, 0.0, 0.0]
c7 = [0.0, -0.5, 0.0]

c = [[c0],[c1],[c2],[c3],[c4],[c5],[c6],[c7]]

ccc = np.asarray(c).reshape(8,3)

c00 = inside_test(data, ccc)

c10 = aa0[c00]



# plt.plot(aa0[:,0], aa0[:,1], ',')
# plt.xlim(-0.5, 0.5)
# plt.ylim(-0.5, 0.5)


cc0 = inside_test(aa0, ccc)

ccc0 = np.asarray(cc0)

new = aa0[ccc0]


plt.plot(new[:,0], new[:,1], ',')
plt.xlim(-0.5, 0.5)
plt.ylim(-0.5, 0.5)



hui = find_nearest(data[:,0], 0)

test1 = find_nearest(data[:,0], box_coords[1,1])
print(test1)




# t_c_1 = []
# t1, a1 = particleCoordsNew (path, fileList[0])
# t1 = np.round((t1 - 0.1628499834108E+03), 3)
# for ps in range(0,num_ps):
#     a_np1 = np.asarray(a1[ps])
#     data1 = a_np1[ps_index[ps]]
#     xedges = box_coords[:,0]
#     yedges = box_coords[:,1]
#     zedges = box_coords[:,2]
#     H1, edges = np.histogramdd(data1, bins=(xedges, yedges, zedges))
#     t_c_1.append([t1, H1])

# t_c_2 = []
# t2, a2 = particleCoordsNew (path, fileList[1])
# t2 = np.round((t2 - 0.1628499834108E+03), 3)
# for ps in range(0,num_ps):
#     a_np2 = np.asarray(a2[ps])
#     data2 = a_np2[ps_index[ps]]
#     xedges = box_coords[:,0]
#     yedges = box_coords[:,1]
#     zedges = box_coords[:,2]
#     H2, edges = np.histogramdd(data2, bins=(xedges, yedges, zedges))
#     t_c_2.append([t2, H2])

# A = np.zeros((n**3, n**3))

# a = H1.flat
# a = list(a)
# A[:,0] = a
# eigon_value, eigon_vector = np.linalg.eig(A)

# # aa0 = np.asarray(a0[ps])
# aa0 = data1[4,:]
# # index = np.where(np.isin(data1, np.asarray(ps_filtered[0])))
# index = np.where(np.isin(data1[:,0],aa0))
# print(data1[index[0]])



