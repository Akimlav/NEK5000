# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 15:58:41 2019

@author: LavrinenkoAV
"""

#surface equation and normal vector
import numpy as np

p1 = np.array([1, 2, 3])
p2 = np.array([4, 6, 9])
p3 = np.array([12, 11, 9])

# These two vectors are in the plane
v1 = p3 - p1
v2 = p2 - p1

# the cross product is a vector normal to the plane
cp = np.cross(v1, v2)

a, b, c = cp

# This evaluates a * x3 + b * y3 + c * z3 which equals d
d = np.dot(cp, p3)

print('The equation is {0}x + {1}y + {2}z = {3}'.format(a, b, c, d))
print(cp)
print('******************************************')

#body mass
g = 9.81
rho = 998.2
Rz = 7116.36
m = Rz / g
V = (m/rho)*2

print('V = %f [m3]' % V)
print('mass = %f [kg]' % m)

alpha = 0.924
L = 6.19
Iyy = 0.07*alpha*m*L**2
print('Iyy = %f [kg*m2]' % Iyy)

# Xg

My1 = 328.275
Xg1 = 3.47072
My2 = 2.87
Xg2 = 3.4252

My_now = My2
Xg_now = Xg2

My = My1 - My2
Xg = Xg1 - Xg2

x = (Xg * My_now) / My
Xg_new = Xg_now - x

print('Xg_new = %f [m]' % Xg_new)
