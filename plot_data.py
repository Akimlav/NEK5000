import time
import numpy as np
import matplotlib.pyplot as plt
import math


def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return array[idx]


start_time = time.time()
case_name = 'lid-driven_test'
file_ext = 'his' #extension

#reading data  
f1 = open( case_name + '.' + file_ext, 'r')
n_p = int(f1.readline())  #counts number of probes (reads first line in file)
f1.close()

#data proccesing
data = np.genfromtxt( case_name + '.' + file_ext, skip_header = n_p+1, invalid_raise = False)
n = sum(1 for line in data)
f = math.floor(n/n_p)
data = data[:(f*n_p)]

probes = {}
for i in range(0, n_p):
    probes['probe_{0}'.format(i+1)] = data[i::n_p]

probes_list = []
probes_l = []
for key in probes.keys():
    probes_list.append(key)
    j = probes[key]
    p_t = j[:,][:,0]
    p_Vx = j[:,][:,1]
    probes_l.append(j)

probes_numpy = np.array(probes_l)


fp = float(input("Enter first point\n"))
lp = float(input("Enter second point\n"))
ref_point_s = find_nearest(data[0], fp)
ref_point_e = find_nearest(data[0], lp)
rp = [ref_point_s, ref_point_e]
print(rp)


# 3D slicing (i - 1, j - 2, k - 3)
# The first index, i, selects the matrix (probe number)
# The second index, j, selects the row   (choose all rows)
# The third index, k, selects the column  (choost parameter)

# plot Vx
for key in probes.keys():
    j = probes[key]
    p_t = j[:,][:,0]
    p_Vx = j[:,][:,1]
    plt.plot(p_t, p_Vx)
    plt.grid(True)
    plt.legend(probes_list)
    plt.xlabel('Time, sec')
    plt.ylabel('Vx')
plt.show()
    
# plot Vy
for key in probes.keys():
    j = probes[key]
    p_t = j[:,][:,0]
    p_Vy = j[:,][:,2]
    plt.plot(p_t, p_Vy)
    plt.grid(True)
    plt.legend(probes_list)
    plt.xlabel('Time, sec')
    plt.ylabel('Vy')
plt.show()

# plot Vz
for key in probes.keys():
    j = probes[key]
    p_t = j[:,][:,0]
    p_Vz = j[:,][:,3]
    plt.plot(p_t, p_Vz)
    plt.grid(True)
    plt.legend(probes_list)
    plt.xlabel('Time, sec')
    plt.ylabel('P')
plt.show()

# plot T
for key in probes.keys():
    j = probes[key]
    p_t = j[:,][:,0]
    p_T = j[:,][:,4]
    plt.plot(p_t, p_T)
    plt.grid(True)
    plt.legend(probes_list)
    plt.xlabel('Time, sec')
    plt.ylabel('T')
plt.show()

#plot
fig, ax = plt.subplots()
ax.grid(True)
plt.figure(1)
plt.plot(probes_numpy[0,:,0],probes_numpy[0,:,4])
#plt.legend()
plt.xlabel('Time, sec')
plt.ylabel('Vx')
plt.show()


start_time2 = time.time() - start_time
print("It was: %.5f seconds" % (start_time2))