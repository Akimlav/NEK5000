## -*- coding: utf-8 -*-
#"""
#Created on Fri Oct  4 17:36:22 2019
#
#@author: LavrinenkoAV
#"""
#CreateCase version 1.2

import os
import numpy as np
import shutil
import subprocess
import datetime
import time
start = time.time()
from openFoam_func_lib import *


now = datetime.datetime.now()
print('Running python script')
print( "Start time and date: "+ now.strftime("%H:%M %d-%m-%Y "))

data1 = np.genfromtxt('inletData',skip_header=1,invalid_raise = False)
mesh = np.genfromtxt('meshData',skip_header=1,invalid_raise = False)

n = (sum(1 for line in data1))
m = (sum(1 for line in mesh))

#create folder
for j in range (0, m):
    mesh_path = 'mesh_'+ str(mesh[j][0])+'_c=' + str(mesh[j][1])
    createMesh(j, mesh_path)
    
    for i in range (0, n):
        start_cycle = time.time()
        print('*************************')
        case_path = 'case_U=' + str(data1[i][0]) + '_m_' + str(mesh[j][0])
        dirpath = os.path.join(case_path)
        dirpath1 = os.path.join(case_path+'/postProcessing')
        if os.path.exists(dirpath):
            print('old Case are!')
            if os.path.exists(dirpath1):
                # yPlus(case_path)
                print('post Case are!'+ case_path)
            else:
                shutil.rmtree(dirpath)
                print('Old case_U='+str(data1[i][0])+'_n='+str(data1[i][1]) + ' deleted')

                createCase(i, case_path, mesh_path)

                print('Running bash script')
                print('*************************')

    #            subprocess.call(case_location + '/'+case_path +'/run.sh')

                print('Bash script done')

    #            results(case_path + '/postProcessing/forces/0/', i)

                print('Reading results')
                print('*************************')
                cycle_time = (time.time()-start_cycle)/3600
                print('It took', cycle_time, 'hours.')
                print('*************************')
        else:
            createCase(i, case_path, mesh_path)
            print('Running bash script')
            print('*************************')

    #        subprocess.call(case_location + '/'+case_path +'/run.sh')

            print('Bash script done')

            # results(case_path + '/postProcessing/forces/0/', i)

            print('Reading results')
            print('*************************')
            cycle_time = (time.time()-start_cycle)/3600
            print('It took', cycle_time, 'hours.')
            print('*************************')
