
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
n = 20
split = np.array_split(data,n)
data = split[n-1]
split = np.array_split(data2,n)
data2 = split[n-1]
time=data[:,][:,0]
time2=data2[:,][:,0]
F_x=data[:,][:,1]
F_p=data[:,][:,4]
F_v=data[:,][:,7]
M_x=data2[:,][:,1]
M_p=data2[:,][:,4]
M_v=data2[:,][:,7]
#pres_y=data[:,][:,2]
#vres_y=data[:,][:,5]
#res_y=(pres_y+vres_y)
dev_F=np.std(F_x)
avg_F=np.mean(F_x)
med_F=st.median(F_x)
med_Fp=st.median(F_p)
med_Fv=st.median(F_v)
dev_M=np.std(M_x)
avg_M=np.mean(M_x)
med_M=st.median(M_x)
med_Mp=st.median(M_p)
med_Mv=st.median(M_v)
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
plt.plot(time,F_p)
plt.plot(time,F_v)

#plt.plot(time,avg_line,)
plt.legend(['Total force','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('force_p, N')
#plt.ylim(med_F*0.8,med_F*1.2)
plt.ylim(-2,8)
#plt.savefig('Resistance.png')
plt.show()

fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(time2,M_x)
plt.plot(time2,M_p)
plt.plot(time2,M_v)

#plt.plot(time,avg_line,)
plt.legend(['Total force','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('Moment_p, N*m')
#plt.ylim(med_M*0.8,med_M*1.2)
plt.ylim(-0.4,0)
#plt.savefig('Resistance.png')
plt.show()

print('average = %f [N]' % avg_F,'median force = %f [N]' % med_F)
print('average = %f [N]' % avg_M,'median moment = %f [N]' % med_M)
print("___________________________________________________________")
print('F pressure = %f [N]' % med_Fp,'F viscouse = %f [N]' % med_Fv)
print('M pressure = %f [N]' % med_Mp,'M viscouse = %f [N]' % med_Mv)