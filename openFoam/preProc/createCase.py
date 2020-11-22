## -*- coding: utf-8 -*-
#"""
#Created on Fri Oct  4 17:36:22 2019
#
#@author: LavrinenkoAV
#"""
#CreateCase version 1

import os
import numpy as np
import shutil
import subprocess
import fileinput
import sys
import datetime
import time


start_time = time.time()

#read mean prop
air_data = np.genfromtxt('air',skip_header=1,invalid_raise = False)
fresh_data = np.genfromtxt('fresh_water',skip_header=1,invalid_raise = False)
sea_data = np.genfromtxt('sea_water',skip_header=1,invalid_raise = False)

#turbulence calculator function
def turb_calc( U, nu, nutnu, Tu ):
    Cnu = 0.09
    u1 = (Tu/100)*U
    k = 3/2*u1**2
    eps = (k**2*Cnu)/(nutnu*nu)
    o = eps/(k*Cnu)
    return (k, eps, o)

def air (T):
    air_rho = np.interp(T,air_data[:,][:,0],air_data[:,][:,1])
    air_nu = np.interp(T,air_data[:,][:,0],air_data[:,][:,2])
    return (air_rho, air_nu)

def sea (T):
    sea_rho = np.interp(T, sea_data[:,][:,0], sea_data[:,][:,1])
    sea_nu = np.interp(T, sea_data[:,][:,0], sea_data[:,][:,2])
    return (sea_rho, sea_nu)

def fresh (T):
    fresh_rho = np.interp(T, fresh_data[:,][:,0], fresh_data[:,][:,1])
    fresh_nu = np.interp(T,fresh_data[:,][:,0], fresh_data[:,][:,2])
    return (fresh_rho, fresh_nu)

def replaceAll(file,searchExp,replaceExp):
    for line in fileinput.input(file, inplace=1):
        if searchExp in line:
            line = line.replace(searchExp,replaceExp)
        sys.stdout.write(line)

def createCase (i):
    src = 'headCase'    
    dst = case_path
    shutil.copytree(src, dst) 
#       src = 'mesh_1.0/1/polyMesh'    
#       dst = case_path+'/constant/polyMesh'
#       shutil.copytree(src, dst)
    src = case_path+'/0.orig'    
    dst = case_path+'/0'
    shutil.copytree(src, dst)
    turb_parameters = (turb_calc(abs(data[i][0]), water_prop[1], nutnu, Tu))
    path = case_path +'/0.orig'
    path1 = case_path +'/0/include/initialConditions'
    path2 = case_path +'/constant/transportProperties'
    f1 = open(path1, 'r')
    f2 = open(path1+'1', 'w')
    checkWords = ("U*","k*","omega*")
    repWords = (str(data[i][0]),str(turb_parameters[0]),str(turb_parameters[2]))
    for line in f1:
        for check, rep in zip(checkWords, repWords):
            line = line.replace(check, rep)
        f2.write(line)
    f1.close()
    f2.close()
    os.remove(path1)
    os.rename(path1+'1',path1)
    f3 = open(path2, 'r')
    f4 = open(path2+'1', 'w')
    checkWords2 = ("rho_air*","nu_air*", "rho_water*","nu_water*")
    repWords2 = (str(air_prop[0]),str(air_prop[1]), str(water_prop[0]), str(water_prop[1]))
    for line in f3:
        for check2, rep2 in zip(checkWords2, repWords2):
            line = line.replace(check2, rep2)
        f4.write(line)
    f3.close()
    f4.close()
    os.remove(path2)
    os.rename(path2+'1',path2)
    print('New case_U='+str(data[i][0])+' created')
    path3 = case_location + '/'+case_path
    path4 = case_location + '/'+case_path + '/run.sh'
    replaceAll(path4, "loc1", case_path)
    with fileinput.FileInput(path3 + '/run.sh' , inplace=True) as file:
        for line in file:
            print(line.replace('loc', path3 ), end='')
    return()
    
# initial data
T = 20
water_prop = fresh(T)
air_prop = air(T)
nutnu = 20
Tu = 0.5
n = 4
case_location = os.getcwd()
print('Running python script')
now = datetime.datetime.now()
print('Running python script')
print( "Start date and time: "+ now.strftime("%H:%M %d-%m-%Y "))
#read U
data = np.genfromtxt('in',skip_header=1,invalid_raise = False)
#create folder
for i in range (0, n):
    start_time_loop = time.time()
    print('*************************')
    case_path = 'case_U='+str(data[i][0])
    dirpath = os.path.join(case_path)
    dirpath1 = os.path.join(case_path+'/postProcessing')
    if os.path.exists(dirpath):
        print('old Case are!')
        if os.path.exists(dirpath1):
            print('post Case are!'+ case_path)
        else:
            print('else')
            shutil.rmtree(dirpath)
            print('Old case_U='+str(data[i][0]) + ' deleted')
            createCase(i)
            print('Running bash script')
            print('*************************')
            # subprocess.call(case_location + '/'+case_path +'/run.sh')
            print('Bash script done')
            print('*************************')
            print("--- %s seconds ---" % (time.time() - start_time_loop))
    else:
        createCase(i)
        print('Running bash script')
        print('*************************')
        # subprocess.call(case_location + '/'+case_path +'/run.sh')
        print('Bash script done')
        print('*************************')
        print("--- %s seconds ---" % (time.time() - start_time_loop))
print('Python script done')
print("--- %s seconds ---" % (time.time() - start_time))

    
    
    
    
