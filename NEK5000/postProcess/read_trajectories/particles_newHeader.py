#!/usr/bin/python3

from sys import argv
from os import system,remove,cpu_count
import numpy as np
# import matplotlib
# matplotlib.use('qt5agg')
import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D
import gzip
import shutil
from multiprocessing import Pool
import random

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
  
  # print("Time: "+str(time*0.02/4.8)+" secs")
  
  # This is the data structure for each particle
  dataType = np.dtype([('dum'  ,np.int64    ), # Dummy 8 byte word, unknown origin
                       ('batch',np.float64  ), # Particle batch number
                       ('sp'   ,np.float64,1), # Particle size
                       ('xp'   ,np.float64,3), # Particle coordinates
                       ('up'   ,np.float64,3), # Particle speed
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

if __name__ == '__main__':
  with Pool() as p:
    p.map(readAndPlot,argv[1:])
    
# Command to generate a movie by just concatenating the images
#ffmpeg -framerate 60 -start_number 1 -i opt_fbalance0%04d.3D.jpg -codec copy particles_2.mkv
time, pdata = readParticleFile('fbalance00002.3D')
time0, pdata0 = readParticleFile('fbalance00001.3D')
x0 = np.asarray(pdata0['xp'][0][1][0][0])
y0 = np.asarray(pdata0['xp'][0][1][1][0])
x = np.asarray(pdata['xp'][0][1][0][0])
y = np.asarray(pdata['xp'][0][1][1][0])
# # #plot
# fig, ax = plt.subplots()
# ax.grid(True)
# plt.figure(1)
# plt.plot(x,y,'o')
# plt.plot(x0,y0,'o')
# #plt.legend()
# plt.xlabel('Z')
# plt.ylabel('Y')
# plt.ylim(-0.5,0.5)
# plt.xlim(-0.5,0.5)
# # plt.show()

xp = []
yp = []
zp = []
xyzp = []
particleSize = 0  
for ibatch in range(0,pdata.shape[0]):
  for ipart in range(0,pdata.shape[2]):
    xpart = pdata[ibatch,particleSize,ipart]['xp']
    xp.append(xpart[0])
    yp.append(xpart[1])
    zp.append(xpart[2])
    xyzp.append(xpart)

rndmp = random.sample(xyzp, 10) # ranodom set of particles at moment of time
    
xyzp = np.asarray(xyzp) 

slice_z = xyzp[(0.3 < xyzp[:,2]) & (xyzp[:,2] < 0.4)] #slice of XY

rndmp_numpy = np.array(rndmp)

itemindex = np.where(xyzp == rndmp_numpy[0][0]) 
print(rndmp_numpy[0])
x1 = int(itemindex[0][0]) #gives index of element from xyzp choozen by random
print(x1)
picked_rndmp = xyzp[x1]
print(picked_rndmp)



# xp = xp[]
# yp = yp[:100]

# fig, ax = plt.subplots()
# ax.grid(True)
# plt.figure(1)
# # plt.plot(rndmp[:,0],rndmp[:,1],'bo')
# # plt.plot(x0,y0,'o')
# #plt.legend()
# plt.xlabel('Z')
# plt.ylabel('Y')
# plt.ylim(-0.5,0.5)
# plt.xlim(-0.5,0.5)
# # plt.show()   
    