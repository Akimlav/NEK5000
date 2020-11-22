
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

#replace data   
f1 = open('forces_1.19048e-005.dat', 'r')
f2 = open('forces2.dat', 'w')

for line in f1:
    f2.write(line.replace('(', ' ').replace(')', ' '))   
f1.close()
f2.close()

#calculations
data=np.genfromtxt('forces2.dat',invalid_raise = False)
#split = np.array_split(data,4)
#data = split[0]
time=data[:,][:,0]
pres_x=data[:,][:,1]
vres_x=data[:,][:,4]
res_x=(pres_x+vres_x)
pres_y=data[:,][:,2]
vres_y=data[:,][:,5]
res_y=(pres_y+vres_y)
#dev=np.std(res)
#avg=np.mean(res)
#med=st.median(res)
#avg_line=[med for i in time]
#print('average = %f [N]' % avg,'median = %f [N]' % med)

#export data
time_col=time.reshape(-1,1)
pres_col=pres_x.reshape(-1,1)
vres_col=vres_x.reshape(-1,1)
res_col=res_x.reshape(-1,1)
my_data=np.concatenate((time_col,pres_col,vres_col,res_col),axis=1)
np.savetxt('export2.dat',my_data)

#plot
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(time,res_x)
plt.plot(time,pres_x)
plt.plot(time,vres_x)
plt.plot(time,res_y)
plt.plot(time,pres_y)
plt.plot(time,vres_y)
#plt.plot(time,avg_line,)
#plt.legend(['Total Resistance','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('force, N')
plt.ylim(0,1)
plt.savefig('Resistance.png')
plt.show()
