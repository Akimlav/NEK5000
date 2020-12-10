#!/usr/bin/python3.8

from sys import argv
from os import system,remove,cpu_count
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import gzip
import shutil
from multiprocessing import Pool
import random
import glob
import os
import sys
from time import time
from scipy.stats import norm
import statistics as st
import multiprocessing 



def readParticleFile(pfilename):
  # print("Reading "+pfilename)
  isgzip = 0
  if pfilename[-2:]=='gz':
    pfile = gzip.open(pfilename,"rb")
    kk = open(pfilename[:-3],'wb')
    shutil.copyfileobj(pfile,kk)
    pfile.close()
    kk.close()
  
    pfile = open(pfilename[:-3],'rb')
    isgzip = 1
  else:
    pfile = open(pfilename,'rb')
  #
  
  # The first entry in the fortran binary file is a 4 byte word, apparently.
  # I don't know why.
  dum = np.fromfile(pfile,dtype=np.int32,count=1)
  
  time = np.fromfile(pfile,dtype=np.float64,count=1)[0]
  counters = np.fromfile(pfile,dtype=np.int32,count=2)
  
  # Number of particles seeded for each set of data
  nseedParticles = counters[0]
  # Number of particle sizes
  nsizes = counters[1]
  
  # The first entry in the fortran binary file is a 4 byte word, apparently.
  # I don't know why.
  dum = np.fromfile(pfile,dtype=np.int32,count=3)
  counters = np.fromfile(pfile,dtype=np.int32,count=6)
  
  # Number of fields per particle
  nfields = counters[3]
  # Total number of particles
  nparticles = counters[4]
  print('Reading: ' + pfilename)
  print("Time: "+str(time*0.02/4.8)+" secs")
  print("-------------------------------------------------------------------")
  # This is the data structure for each particle
  dataType = np.dtype([('dum'  ,np.int64    ), # Dummy 8 byte word, unknown origin
                       ('batch',np.float64  ), # Particle batch number
                       ('sp'   ,np.float64,(1)), # Particle size
                       ('xp'   ,np.float64,(3)), # Particle coordinates
                       ('up'   ,np.float64,(3)), # Particle speed
                       ('he'   ,np.float64  ), # 
                       ('hp'   ,np.float64  ), #
                       ('rest' ,np.float64,nfields-10)]) # Fields not used at the moment
  
  # Read the data for all particles
  pdata = np.fromfile(pfile,dtype=dataType,count=nparticles)

  pfile.close()
  
  # remove the gunzipped file
  if isgzip==1: 
    remove(pfilename[:-3])
  
  # Now discard the empty part of pdata
  nfull = nparticles//2
  ndelta = nparticles//4
  while True:
    if nfull==nparticles-1 or (pdata['batch'][nfull]!=0. and pdata['batch'][nfull+1]==0.):
      break
    else:
      if pdata['batch'][nfull]!=0.:
        nfull += ndelta
      else:
        nfull -= ndelta
      if ndelta>1: ndelta = ndelta//2
    #endif
  #end while
  
  pdata = np.resize(pdata,(nfull+1,))
  
  nbatch = int(pdata['batch'][-1])
  
  # Reshape the array with nbatches, with nsizes of nseedParticles each
  pdata = pdata.reshape(nbatch,nsizes,nseedParticles)

  return time,pdata

# end def readParticleFile

def plotParticle(pfilename,time,pdata,particleSize):
  fig = plt.figure()
  
  ax = fig.add_subplot(111,projection='3d')
  
  xp = []
  yp = []
  zp = []
  
  for ibatch in range(0,pdata.shape[0]):
    for ipart in range(0,pdata.shape[2]):
      xpart = pdata[ibatch,particleSize,ipart]['xp']
      xp.append(xpart[0])
      yp.append(xpart[1])
      zp.append(xpart[2])
  
  ax.scatter(xp,yp,zp,marker='.',s=1,color='r')

  ax.set_xlabel('X')
  ax.set_ylabel('Y')
  ax.set_zlabel('Z')
  
  ax.set_xlim(-0.5,0.5)
  ax.set_ylim(-0.5,0.5)
  ax.set_zlim(-0.5,0.5)
      
  # Set a desired view angle 
  ax.view_init(90,270)
  plt.savefig(pfilename[:-3]+'.png')
  plt.close()
#end def plotParticle

def readAndPlot(pfilename):
  time,pdata = readParticleFile(pfilename)
  
  particleSize = 0
    
  plotParticle(pfilename,time,pdata,particleSize)
  (pdata)

###################################################################################################################

fileList = [name for name in os.listdir() if name.endswith(".3D")]
fileList.sort()

def particleCoords (fileName, particleSize):
    time,pdata = readParticleFile(str(fileName))
    
    xyzp = []
            
    for ibatch in range(0,pdata.shape[0]):
        for ipart in range(0,pdata.shape[2]):
          xpart = pdata[ibatch,particleSize,ipart]['xp']
          xyzp.append(xpart)
    p_coords = np.asarray(xyzp)
    return(p_coords)

def plotVideo (choose, n, Dimension, particleSize, center, radius, plotsmbl):
    start_time = time()
    xyzz = particleCoords('fbalance00001.3D', particleSize)
    index = np.random.choice(xyzz.shape[0], n, replace=False)
    for i in fileList:
        if choose.lower() in ['r', 'random', 'rnd']:
            xyz = particleCoords(i, particleSize)
            xyz1np = xyz[index]
        elif choose.lower() in ['all', 'a']:
                xyz = particleCoords(i, particleSize)
                xyz1np = np.asarray(xyz)
        elif choose.lower() in ['index', 'i']:
                xyz = particleCoords(i, particleSize)
                index = n
                xyz1np = xyz[index]
        elif choose.lower() in ['sphere', 's']:
            filtered = []
            for j in range(len(xyzz)):
                r1 = ((xyzz[j,0] - center[0])**2 + (xyzz[j,1] - center[1])**2 + (xyzz[j,2] - center[2])**2)**.5
                if r1 <= radius:
                    filtered.append(xyzz[j,:])
            filtered = np.asarray(filtered)
            index = np.where(np.isin(xyzz[:,1], filtered))
            xyz = particleCoords(i, particleSize)
            xyz1np = xyz[index]

        if Dimension.lower() in ['2d', '2D']:
            if xyz1np.shape[0] == 3:
                plt.plot(xyz1np[0],xyz1np[1], plotsmbl, markersize=0.5)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.xlim(-0.5,0.5)
                plt.ylim(-0.5,0.5)
                # plt.grid()
                plt.savefig(i[:-3] + '_2D.png', dpi=300)
                plt.clf()
            else:
                plt.plot(xyz1np[:,0],xyz1np[:,1], plotsmbl, markersize=0.5)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.xlim(-0.5,0.5)
                plt.ylim(-0.5,0.5)
                # plt.grid()
                plt.savefig(i[:-3] + '_2D.png', dpi=300)
                plt.clf()
                
        elif Dimension.lower() in ['3d', '3D']:
            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            if xyz1np.shape[0] == 3:
                ax.plot(xyz1np[0],xyz1np[1],xyz1np[2], plotsmbl, markersize=0.5)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xlim(-0.5,0.5)
                ax.set_ylim(-0.5,0.5)
                ax.set_zlim(-0.5,0.5)
                plt.savefig(i[:-3] + '_3D.png', dpi=300)
                plt.clf()
            else:
                ax.plot(xyz1np[:,0], xyz1np[:,1], xyz1np[:,2], plotsmbl, markersize=0.5)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xlim(-0.5,0.5)
                ax.set_ylim(-0.5,0.5)
                ax.set_zlim(-0.5,0.5)
                plt.savefig(i[:-3] + '_3D.png', dpi=300)
                plt.clf()

    print('It was: %.3f seconds'  % (time() - start_time))

def plotTrajectory (choose, n, Dimension, particleSize, center, radius, plotsmbl):
    start_time = time()
    xyz1 = []
    xyzz = particleCoords('fbalance00001.3D', particleSize)
    index = np.random.choice(xyzz.shape[0], n, replace=False)
    if choose.lower() in ['r', 'random', 'rnd']:
        for i in fileList:
            xyz = particleCoords(i, particleSize)
            xyz_rnd = xyz[index]
            xyz1.append(xyz_rnd)
            xyz1np = np.asarray(xyz1)
    elif choose.lower() in ['all', 'a']:
        for i in fileList:
            xyz = particleCoords(i, particleSize)
            xyz1.append(xyz)
            xyz1np = np.asarray(xyz1)
            
    elif choose.lower() in ['index', 'i']:
        for i in fileList:
            xyz = particleCoords(i, particleSize)
            index = n
            xyz_rnd = xyz[index]
            xyz1.append(xyz_rnd)
            xyz1np = np.asarray(xyz1)
    elif choose.lower() in ['sphere', 's']:
        filtered = []
        for i in range(len(xyzz)):
           r1 = ((xyzz[i,0] - center[0])**2 + (xyzz[i,1] - center[1])**2 + (xyzz[i,2] - center[2])**2)**.5
           if r1 <= radius:
               filtered.append(xyzz[i,:])
        filtered = np.asarray(filtered)   
        index = np.where(np.isin(xyzz[:,1], filtered))  
        for i in fileList:
            xyz = particleCoords(i, particleSize)
            xyz_ind = xyz[index]
            xyz1.append(xyz_ind)
            xyz1np = np.asarray(xyz1)

    if Dimension.lower() in ['3d', '3D']:
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(np.shape(xyz1np)[1]):
            if xyzz.shape[1] == 3:
                ax.plot(xyz1np[:,0],xyz1np[:,1],xyz1np[:,2], plotsmbl)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xlim(-0.5,0.5)
                ax.set_ylim(-0.5,0.5)
                ax.set_zlim(-0.5,0.5)
                
            else:
                a1 = xyz1np[:,i,:]
                ax.plot(a1[:,0],a1[:,1], a1[:,2], plotsmbl)
                ax.set_xlabel('X')
                ax.set_ylabel('Y')
                ax.set_zlabel('Z')
                ax.set_xlim(-0.5,0.5)
                ax.set_ylim(-0.5,0.5)
                ax.set_zlim(-0.5,0.5)
            ax.figure.savefig(str(choose) + '_' + str(n) + '_' + str(Dimension) + '_' +  str(particleSize) + '_' + str(center)  + '_' + str(radius) + '.png')
            # plt.show()
        
    elif Dimension.lower() in ['2d', '2D']:
        if xyz1np.shape[1] == 3:
            for i in range(np.shape(xyz1np)[1]):
                plt.plot(xyz1np[:,0],xyz1np[:,1], plotsmbl)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.xlim(-0.5,0.5)
                plt.ylim(-0.5,0.5)
            # plt.grid()
            plt.savefig(str(choose) + '_' + str(n) + '_' + str(Dimension) + '_' +  str(particleSize) + '_' + str(center)  + '_' + str(radius) + '.png', dpi = 300)
            # plt.show()
        else:
            for i in range(np.shape(xyz1np)[1]):
                a1 = xyz1np[:,i,:]
                plt.plot(a1[:,0],a1[:,1], plotsmbl)
                plt.xlabel('X')
                plt.ylabel('Y')
                plt.xlim(-0.5,0.5)
                plt.ylim(-0.5,0.5)
            # plt.grid()
            plt.savefig(str(choose) + '_' + str(n) + '_' + str(Dimension) + '_' +  str(particleSize) + '_' + str(center)  + '_' + str(radius) + '.png', dpi = 300)
            # plt.show()
    
            
    print('It was: %.3f seconds'  % (time() - start_time))
    return(xyz1np)

def totalDist(filename, extension, particleSize):
    total_dist = 0
    for i in range(1, len(fileList)+1):
        if i < len(fileList):
            time0,pdata0 = readParticleFile(filename + "{number:05}".format(number=i) + '.' + extension)
            time1,pdata1 = readParticleFile(filename + "{number:05}".format(number=i+1) + '.' + extension)
            for ibatch in range(0,pdata0.shape[0]):
                x0 = pdata0['xp'][ibatch][particleSize][:,0]
                x1 = pdata1['xp'][ibatch][particleSize][:,0]
                y0 = pdata0['xp'][ibatch][particleSize][:,1]
                y1 = pdata1['xp'][ibatch][particleSize][:,1]
                z0 = pdata0['xp'][ibatch][particleSize][:,2]
                z1 = pdata1['xp'][ibatch][particleSize][:,2]
                dist = ((x1-x0)**2+(y1-y0)**2+(z1-z0)**2)**0.5
                total_dist += dist
    return(total_dist)

def PDF (filename, extension, particleSize):
    distance = totalDist(filename, extension, particleSize)
    loc = st.mean(distance)
    scale = np.std(distance)
    y = (distance - loc) / scale
    pdf = norm.pdf(y)
    return (pdf)

def plotPDF (filename, extension, particleSize):
    a = totalDist(filename, extension, particleSize)
    b = PDF(filename, extension, particleSize)
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.plot(a,b,'o')
    plt.xlabel('distance')
    plt.ylabel('PDF')
    plt.savefig('distance PDF_' + str(particleSize) + '.png', dpi = 300)
    # plt.show()

def createVideo(name, file):
    cmd1 = 'ffmpeg -f image2 -r 30 -pattern_type glob -i '
    cmd3 = ' -pix_fmt yuv420p -vf '
    cmd4 = '"pad=ceil(iw/2)*2:ceil(ih/2)*2"'
    cmd5 = ' '
    cmd6 = '.mp4'
    cmd = cmd1 + file + cmd3 + cmd4 + cmd5 + name + cmd6
    os.system(cmd)

def stuck (case_name, file_ext):
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
    plt.plot(hot_wall[:,4],hot_wall[:,5],'ro')
    #plt.legend()
    plt.xlabel('Z')
    plt.ylabel('Y')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('hot wall.png', dpi = 300)
    # plt.show()
    
    # plot cold wall
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.title('cold wall')
    plt.plot(cold_wall[:,4],cold_wall[:,5],'bo',markersize=1)
    #plt.legend()
    plt.xlabel('Z')
    plt.ylabel('Y')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('cold wall.png', dpi = 300)
    # plt.show()
    
    # plot cold ceiling
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.title('cold ceiling')
    plt.plot(cold_ceiling[:,3],cold_ceiling[:,5],'bo',markersize=1)
    #plt.legend()
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('cold ceiling.png', dpi = 300)
    # plt.show()
    
    # plot hot floor
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.title('hot floor')
    plt.plot(hot_floor[:,3],hot_floor[:,5],'ro',markersize=1)
    #plt.legend()
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('hot floor.png', dpi = 300)
    # plt.show()

    # plot adiabatic front
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.title('adiabatic front')
    plt.plot(adiabatic_front[:,3],adiabatic_front[:,4],'o',markersize=1)
    #plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('adiabatic front.png', dpi = 300)
    # plt.show()
    
    # plot adiabatic back
    fig, ax = plt.subplots()
    ax.grid(True)
    plt.figure(1)
    plt.title('adiabatic back')
    plt.plot(adiabatic_back[:,3],adiabatic_back[:,4],'o',markersize=1)
    #plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.ylim(-0.5,0.5)
    plt.xlim(-0.5,0.5)
    plt.savefig('adiabatic back.png', dpi = 300)
    # plt.show()

#############################################################################
                                # MENU #
#############################################################################
# Exit program
def exit():
    sys.exit()
    
def menu():
    print ("\n NEK 5000 data post processing tool v 1.0 ")

    strs = (
            '1. Plot PDF \n'
            '2. Plot trajectory \n'
            '3. Plot moving particles \n'
            '4. Plot all \n'
            '5. Plot stuck particles \n'
            '9. Create video\n'
            '0. Exit\n'
            '--- Your choice : ')
    choice = input(strs) or "9"
    return int(choice) 

while True:
    choice = menu()
    if choice == 1: # PDF
        filename = 'fbalance'
        # print('--- write filename:')
        # filename = input()
        extension = '3D'
        # print('--- write file extension:')
        # extension = input()
        print('--- particle size:')
        particleSize = int(input())
        plotPDF(filename, extension, particleSize)
    elif choice == 2: # trajectories
        print('particle size:')
        particleSize = int(input())
        print('What you want to plot? \n'
              'a - all particles of one size\n'
              'i - one particle with certain index \n'
              's - particles inside sphere of certian radius and center \n'
              'r - random set of particles \n')
        choose = input()
        if choose.lower() in ['r']:
            print('number of random particles:')
            n = int(input())
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['a']:
            n = 1
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['i']:
            print('index of particle:')
            n = int(input())
            center = np.asarray(input())
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['s']:
            n = 1
            print('enter coordinates of center of the sphere informat of array x y z :')
            arr = input() 
            center = list(map(float,arr.split(' ')))
            print('enter radius of the sphere in float format:')
            radius = float(input())
        print('3D or 2D?')
        Dimension = input()
        print('choose marker type: \n'
              ' . - point marker \n'
              ' , - pixel marker \n'
              ' o - circle marker \n'
              ' - line')
        plotsmbl = (input())
        plotTrajectory (choose, n, Dimension, particleSize, center, radius, plotsmbl)
    elif choice == 3: # pictires of each timestep
        print('particle size:')
        particleSize = int(input())
        print('What you want to plot? \n'
              'a - all particles of one size\n'
              'i - one particle with certain index \n'
              's - particles inside sphere of certian radius and center \n'
              'r - random set of particles \n')
        choose = input()
        if choose.lower() in ['r']:
            print('number of random particles:')
            n = int(input())
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['a']:
            n = 1
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['i']:
            print('index of particle:')
            n = int(input())
            center = np.asarray(input())
            center = np.asarray([0,0,0])
            radius = 0.1
        elif choose.lower() in ['s']:
            n = 1
            print('enter coordinates of center of the sphere informat of array x y z :')
            arr = input() 
            center = list(map(float,arr.split(' ')))
            print('enter radius of the sphere in float format:')
            radius = float(input())
        print('3D or 2D?')
        Dimension = input()
        print('choose marker type: \n'
              ' . - point marker \n'
              ' , - pixel marker \n'
              ' o - circle marker \n'
              ' - line')
        plotsmbl = (input())
        plotVideo (choose, n, Dimension, particleSize, center, radius, plotsmbl)
    elif choice == 4:
        args1 = list(['fbalance','3D',0])
        args2 = list(['s',1,'2D',0, np.asarray([0.25,0.25,0]), 0.15, 'o'])
        args3 = list(['r',300,'2D',0, np.asarray([0.25,0.25,0]), 0.15, '-'])
        args4 = list(['part','stuck'])
        start_time = time()
        # creating processes 
        p1 = multiprocessing.Process(target=plotPDF, args=(args1),)
        p2 = multiprocessing.Process(target=plotVideo, args=(args2),)
        p3 = multiprocessing.Process(target=plotTrajectory, args=(args3),)
        p4 = multiprocessing.Process(target=stuck, args=(args4),)
        # starting processes 
        p1.start() 
        p2.start() 
        p3.start()
        p4.start() 
        # process IDs 
        print("ID of process p1: {}".format(p1.pid)) 
        print("ID of process p2: {}".format(p2.pid))
        print("ID of process p2: {}".format(p3.pid))   
        # wait until processes are finished 
        p1.join() 
        p2.join() 
        p3.join()
        p4.join()
        # both processes finished 
        print("All processes finished execution!") 
        print('All it was: %.3f seconds'  % (time() - start_time))
        name = 'video'
        file = '"*_2D.png"'
        createVideo(name, file)
    elif choice == 5:
        case_name = 'part'
        file_ext = 'stuck'
        stuck(case_name, file_ext)
    elif choice == 9:
        print('enter name of the video:')
        name = input()
        print('enter name of picture:')
        file = input()
        createVideo(name, file)
    elif choice == 0:
        exit()
    else:
        menu()

# # Main Program
if __name__ == '__main__':
  with Pool() as p:
    p.map(menu(),argv[1:])
