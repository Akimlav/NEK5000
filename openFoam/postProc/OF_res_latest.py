
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

#replace data   
f1 = open('forces.dat', 'r')
f2 = open('forces2.dat', 'w')

for line in f1:
    f2.write(line.replace('(', ' ').replace(')', ' '))   
f1.close()
f2.close()

#calculations
data=np.genfromtxt('forces2.dat',invalid_raise = False)
split = np.array_split(data,2)
data = split[1]
time=data[:,][:,0]
pres=data[:,][:,1]
vres=data[:,][:,4]
res=(pres+vres)*2
dev=np.std(res)
avg=np.mean(res)
med=st.median(res)
avg_line=[med for i in time]
print('average = %f [N]' % avg,'median = %f [N]' % med)

##export data
#time_col=time.reshape(-1,1)
#pres_col=pres.reshape(-1,1)
#vres_col=vres.reshape(-1,1)
#res_col=res.reshape(-1,1)
#my_data=np.concatenate((time_col,pres_col,vres_col,res_col),axis=1)
#np.savetxt('export2.dat',my_data)

#plot
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(time,res,'b-')
plt.plot(time,pres*2,'r-')
plt.plot(time,vres*2,'g-')
plt.plot(time,avg_line,)
plt.legend(['Total Resistance','pressure','viscouse'])
plt.xlabel('Time, sec')
plt.ylabel('Resistance, N')
plt.ylim(0,med*3)
plt.savefig('Resistance.png')
plt.show()
