#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 10:17:24 2020

@author: akimlavrinenko
"""
import time
import numpy as np
import matplotlib.pyplot as plt

#data[i,j] - i for row, j for column

start_time = time.time()


case_name = 'part'
file_ext = 'stuck' #extension

#reading data  
f1 = open( case_name + '.' + file_ext, 'r')
# n_p = int(f1.readline())  #counts number of probes (reads first line in file)
f1.close()

#data proccesing
data = np.genfromtxt( case_name + '.' + file_ext, skip_header = 0, invalid_raise = False)
num_rows, num_cols = data.shape

hot_wall = [data[i,:] for i in range (0, num_rows) if data[i,3] == -0.5]
cold_wall = [data[i,:] for i in range (0, num_rows) if data[i,3] == 0.5]
cold_ceiling = [data[i,:] for i in range (0, num_rows) if data[i,4] == 0.5]
hot_floor = [data[i,:] for i in range (0, num_rows) if data[i,4] == -0.5]
adiabatic_front = [data[i,:] for i in range (0, num_rows) if data[i,5] == 0.5]
adiabatic_back = [data[i,:] for i in range (0, num_rows) if data[i,5] == -0.5]

hot_wall = np.array(hot_wall)
cold_wall = np.array(cold_wall)     
cold_ceiling = np.array(cold_ceiling)
hot_floor = np.array(hot_floor)
adiabatic_front = np.array(adiabatic_front)
adiabatic_back = np.array(adiabatic_back)

# plot hot wall
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.title('hot wall')
plt.plot(hot_wall[:,3],hot_wall[:,4],'ro')
#plt.legend()
plt.xlabel('Z')
plt.ylabel('Y')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)
plt.show()

# plot cold wall
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.title('cold wall')
plt.plot(cold_wall[:,3],cold_wall[:,4],'bo')
#plt.legend()
plt.xlabel('Z')
plt.ylabel('Y')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)
plt.show()

# plot cold ceiling
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.title('cold ceiling')
plt.plot(cold_ceiling[:,2],cold_ceiling[:,4],'bo')
#plt.legend()
plt.xlabel('X')
plt.ylabel('Z')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)
plt.show()

# plot hot floor
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.title('hot floor')
plt.plot(hot_floor[:,2],hot_floor[:,4],'ro')
#plt.legend()
plt.xlabel('X')
plt.ylabel('Z')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)
plt.show()

# # plot adiabatic front
# fig, ax = plt.subplots()
# ax.grid(True)
# plt.figure(1)
# plt.title('adiabatic front')
# plt.plot(adiabatic_front[:,2],adiabatic_front[:,3],'o')
# #plt.legend()
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.ylim(-0.5,0.5)
# plt.xlim(-0.5,0.5)
# plt.show()

# # plot adiabatic back
# fig, ax = plt.subplots()
# ax.grid(True)
# plt.figure(1)
# plt.title('adiabatic back')
# plt.plot(adiabatic_back[:,2],adiabatic_back[:,3],'o')
# #plt.legend()
# plt.xlabel('X')
# plt.ylabel('Y')
# plt.ylim(-0.5,0.5)
# plt.xlim(-0.5,0.5)
# plt.show()

start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))