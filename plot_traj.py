
import statistics as st
import numpy as np
import matplotlib.pyplot as plt

#replace data   
# f1 = open('forces_1.19048e-005.dat', 'r')
# f2 = open('forces2.dat', 'w')

# for line in f1:
#     f2.write(line.replace('(', ' ').replace(')', ' '))   
# f1.close()
# f2.close()

#calculations
data=np.genfromtxt('/Users/akimlavrinenko/Downloads/trajectories.txt',invalid_raise = False)
#split = np.array_split(data,4)
#data = split[0]
time=data[:,][:,0]
x1=data[:,][:,1]
y1=data[:,][:,2]

#dev=np.std(res)
#avg=np.mean(res)
#med=st.median(res)
#avg_line=[med for i in time]
#print('average = %f [N]' % avg,'median = %f [N]' % med)

#plot
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(x1,y1)

#plt.plot(time,avg_line,)
#plt.legend(['Total Resistance','pressure','viscouse'])
# plt.xlabel('Time, sec')
# plt.ylabel('force, N')
plt.ylim(-0.5,0.5)
plt.xlim(-0.5,0.5)
# plt.savefig('Resistance.png')
plt.show()
