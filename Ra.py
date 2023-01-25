#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 11:25:22 2022

@author: akimlavrinenko
"""

from decimal import Decimal


g = 9.81
beta = 1/300
deltaT = 20
L = 0.7
nu = 1.57e-5
alpha = 2.24e-5

Ra = (g*beta*deltaT*L**3)/(nu*alpha)

print('%.2E' % Decimal(Ra))