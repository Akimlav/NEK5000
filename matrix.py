#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 16:50:32 2021

@author: akimlavrinenko
"""
import numpy as np
from NEK5000_func_lib import particleCoordsNew
from os import listdir
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation as R
import math as m
path = './fbalance/'
fileList = [name for name in listdir(path) if name.endswith(".3D")]
fileList.sort()
t, a = particleCoordsNew (path, fileList[0])

#params
step = 3 # file step
n = 5 #number of the bins
num_ps = 5
fileList = fileList[0::step]
x0 = -0.5
y0 = -0.5
z0 = -0.5

# c = [[c0],[c1],[c2],[c3],[c4],[c5],[c6],[c7]]

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


def rot_f (angle, vector):
    fi = angle
    A = np.zeros((3,3))
    A[0,0] = np.cos(fi)
    A[0,1] = -np.sin(fi)
    A[1,0] = np.cos(fi)
    A[1,1] = np.sin(fi)
    A[2,2] = 1
    AA= np.dot(A, vector)
    return AA

vert_list = []
A = np.zeros((8,3))
A[0] = box_coords[0]
A[1] = A[0]
A[1,1] = A[0,0] + delta
A[2] = A[1]
A[2,0] = A[1,0] + delta
A[3] = A[2]
A[3,1] = A[2,1] - delta
A[4:8] = A[0:4]
A[4:8,2] = A[0:4,2] + delta
vert_list.append(A)
vert_list1 = []
for i in range(1,n):
    B = np.zeros((8,3))
    B[:,0] = A[:,0]
    B[:,2] = A[:,2]
    B[:,1] = A[:,1] + delta * i
    vert_list.append(B)
    
for i in range(n):
    for j in range(n):
        C = np.zeros((8,3))
        C[:,1:3] = vert_list[i][:,1:3]
        C[:,0] = vert_list[i][:,0] + delta * j
        vert_list1.append(C)
        
vert_list2 = []
for i in range (n**2):
    for j in range(n):
        D = np.zeros((8,3))
        D[:,0:2] = vert_list1[i][:,0:2]
        D[:,2] = vert_list1[i][:,2] + delta * j
        vert_list2.append(D)
    

# for j in range(n): 
#     B = np.zeros((8,3))
#     B = vert_list[0]
#     B[:,1] = vert_list[0][:,1] + delta
#     vert_list.append(B)
        
# print(A)
# cube3d = np.asarray(c).reshape(8,3)
# # points = np.asarray((-0.1,-0.1,-0.1))
# # points = np.asarray((0.1,0.1,0.1))
# points = np.asarray(a[0])

# b1,b2,b3,b4,t1,t2,t3,t4 = cube3d

# dir1 = (t1-b1)
# size1 = np.linalg.norm(dir1)
# dir1 = dir1 / size1

# dir2 = (b2-b1)
# size2 = np.linalg.norm(dir2)
# dir2 = dir2 / size2

# dir3 = (b4-b1)
# size3 = np.linalg.norm(dir3)
# dir3 = dir3 / size3

# cube3d_center = (b1 + t3)/2.0

# dir_vec = points - cube3d_center

# res1 = np.where( (np.absolute(np.dot(dir_vec, dir1)) * 2) > size1 )[0]
# res2 = np.where( (np.absolute(np.dot(dir_vec, dir2)) * 2) > size2 )[0]
# res3 = np.where( (np.absolute(np.dot(dir_vec, dir3)) * 2) > size3 )[0]

# res = list( set().union(res1, res2, res3) )

# A = points[res]
# B = np.delete(points, res, 0)

# plt.plot(B[:,0], B[:,1], ',')
# plt.xlim(-0.5, 0.5)
# plt.ylim(-0.5, 0.5)



# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# # ax.plot(A[:,0],A[:,2], A[:,1], ',')
# ax.plot(B[:,0],B[:,2], B[:,1], ',')
# ax.set_title('Isometric view')
# ax.set_xlim([-0.5, 0.5])
# ax.set_ylim([-0.5, 0.5])
# ax.set_xlim([-0.5, 0.5])
# ax.set_ylim([-0.5, 0.5])
# ax.set_zlim([-0.5, 0.5])

# plt.show()