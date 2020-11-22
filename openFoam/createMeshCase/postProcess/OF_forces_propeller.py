
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

#replace data   
f1 = open('force.dat', 'r')
f2 = open('force2.dat', 'w')
f3 = open('moment.dat', 'r')
f4 = open('moment2.dat', 'w')
for line in f1:
    f2.write(line.replace('(', ' ').replace(')', ' '))   
f1.close()
f2.close()
for line in f3:
    f4.write(line.replace('(', ' ').replace(')', ' '))   
f3.close()
f4.close()


#calculations
data=np.genfromtxt('force2.dat',invalid_raise = False)
data2=np.genfromtxt('moment2.dat',invalid_raise = False)
split = np.array_split(data,2)
data = split[1]
split = np.array_split(data2,2)
data2 = split[1]
time=data[:,][:,0]
time2=data2[:,][:,0]
F_x=data[:,][:,1]
M_x=data2[:,][:,1]
#pres_y=data[:,][:,2]
#vres_y=data[:,][:,5]
#res_y=(pres_y+vres_y)
dev_F=np.std(F_x)
avg_F=np.mean(F_x)
med_F=st.median(F_x)
dev_M=np.std(M_x)
avg_M=np.mean(M_x)
med_M=st.median(M_x)
avg_line=[med_M for i in time]


##export data
#time_col=time.reshape(-1,1)
#pres_col=pres_x.reshape(-1,1)
#vres_col=vres_x.reshape(-1,1)
#res_col=res_x.reshape(-1,1)
#my_data=np.concatenate((time_col,pres_col,vres_col,res_col),axis=1)
#np.savetxt('export2.dat',my_data)

#plot
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(time,F_x)
#plt.plot(time,M_x)
#plt.plot(time,vres_x)
#plt.plot(time,res_y)
#plt.plot(time,pres_y)
#plt.plot(time,vres_y)
#plt.plot(time,avg_line,)
#plt.legend(['Total Resistance','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('force, N')
#plt.ylim(med_F*0.8,med_F*1.2)
#plt.savefig('Resistance.png')
plt.show()

fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
#plt.plot(time,F_x)
plt.plot(time2,M_x)
#plt.plot(time,vres_x)
#plt.plot(time,res_y)
#plt.plot(time,pres_y)
#plt.plot(time,vres_y)
#plt.plot(time,avg_line,)
#plt.legend(['Total Resistance','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('Moment, N*m')
plt.ylim(med_M*0.8,med_M*1.2)
#plt.savefig('Resistance.png')
plt.show()

print('average = %f [N]' % avg_F,'median force = %f [N]' % med_F)
print('average = %f [N]' % avg_M,'median moment = %f [N]' % med_M)
