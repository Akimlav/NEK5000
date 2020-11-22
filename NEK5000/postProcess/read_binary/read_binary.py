#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:57:50 2020

@author: akimlavrinenko
"""

#data[i,j] - i for row, j for column
import time
import numpy as np
import struct
import binascii

# start_time = time.time()

case_name1 = 'fortran_ascii'
file_ext1 = 'dat' #extension

case_name2 = 'fortran_bin_fl'
file_ext2 = 'dat' #extension

#reading data
f1 = open( case_name1 + '.' + file_ext1, 'r')
f1.close()

f2 = open( case_name2 + '.' + file_ext2, 'r')
f2.close()
data0 = np.genfromtxt( case_name1 + '.' + file_ext1, skip_footer = 10, invalid_raise = False)
data1 = np.genfromtxt( case_name1 + '.' + file_ext1, skip_header = 2, invalid_raise = False)
# data2 = np.genfromtxt( case_name2 + '.' + file_ext2, skip_header = 2, invalid_raise = False)

x = np.array([[1, 2, 3], [0.4, 5, 0.6234], [221.222, 3453.0, 0.0001]], np.float32)

number = 0.994362871803
c = np.where(data0 == number)
# print(c[0])

data =  open('fortran_bin', mode='rb').read()
data3 =  open('fortran_ascii.dat', mode='r').read(32)
# print(data3)

byte_list = []
with open("fortran_bin", "rb") as f:
    while True:
        byte = f.read(1)
        if not byte:
            break
        byte_list.append(byte)

first_line = byte_list[0:32]

f3 = open('new.dat', 'w')
f3.write(str(first_line))
f3.close()

with open('new.dat', mode='rb') as file: # b is important -> binary
    fileContent = file.read()
    
ces = np.fromfile('fortran_bin', dtype='int32', count=-1)
# ces1 = np.fromfile('fortran_bin',dtype='float32', count=-1, sep='', offset=0)
# q = (byte_list[].decode("ascii"))

# with open("fortran_bin", "rb") as f:
    # while (byte := f.read(1)):
        # print(byte.decode())
        
from scipy.io import FortranFile
f4 = FortranFile('fortran_bin', 'r')
print(f4.read_ints(np.int32))
f4.close()


sum1 = 400
p = 0.01
for i in range (0,30):
    sum1 += sum1 * p
    print(sum1 * 3)