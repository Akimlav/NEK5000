
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

#replace data   




start_time = time.time()


case_name = 'forces'
file_ext = 'dat' #extension
f1 = open( case_name + '.' + file_ext, 'r')
f1 = open( case_name + '2' + '.' + file_ext, 'w')

for line in f1:
    f2.write(line.replace('(', ' ').replace(')', ' '))   
f1.close()
f2.close()

#calculations
data = np.genfromtxt( case_name + '2' + '.' + file_ext, invalid_raise = False)

time=data[:,][:,0]
pres=data[:,][:,1]
vres=data[:,][:,4]
res=(pres+vres)*2
dev=np.std(res)
avg=np.mean(res)
med=st.median(res)
avg_line=[med for i in time]
print('average = %f [N]' % avg,'median = %f [N]' % med)

itemindex = np.where(probes_numpy==4)
itemindex2 = np.where(probes_numpy==5)
x1 = int(itemindex[1][0])
x2 = int(itemindex2[1][0]) 
new_res = probes_numpy[:,x1:x2+1,:]


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
