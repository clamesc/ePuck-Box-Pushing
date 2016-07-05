#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import numpy as np

Q = np.load("Data/2016_07_05-2_Q.npy")
s = np.load("Data/2016_07_05-2_s.npy")
qs = []
for q in Q:
    qs.append(np.mean(q))


fig, ax1 = plt.subplots(figsize=(6.5,5))
ax1.plot(s, 'k-')
ax1.set_xlabel('Episodes')
ax1.set_ylabel('Movements to terminal state', color='k')
for tl in ax1.get_yticklabels():
    tl.set_color('k')

ax2 = ax1.twinx()
ax2.plot(qs, 'b-')
ax2.set_ylabel('Average Q-values', color='b')
for tl in ax2.get_yticklabels():
    tl.set_color('b')

plt.xlim(0,150)
plt.show()



'''
fig, ax = plt.subplots(figsize=(6.5,5))
heatmap = ax.pcolor(Q[-1], cmap=plt.cm.Blues, alpha=0.8)

fig.colorbar(heatmap, ax=ax)

fig = plt.gcf()
#fig.set_size_inches(6.5,5)

# turn off the frame
ax.set_frame_on(False)

# put the major ticks at the middle of each cell
ax.set_yticks(np.arange(Q[-1].shape[0])+0.5, minor=False)
ax.set_xticks(np.arange(Q[-1].shape[1])+0.5, minor=False)

# want a more natural, table-like display
ax.invert_yaxis()
ax.xaxis.tick_top()

labels = ['left', 'straight', 'right']

ax.set_xticklabels(labels, minor=False)
ax.set_yticklabels(range(10), minor=False)

ax.set_xlabel('Actions')
ax.set_ylabel('States')

ax.grid(False)

ax = plt.gca()

for t in ax.xaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False 
for t in ax.yaxis.get_major_ticks(): 
    t.tick1On = False 
    t.tick2On = False  

plt.show()
'''

'''
fig, ax = plt.subplots(figsize=(6.5,5))

v = np.loadtxt("proximity_values.txt")
x = np.arange(-18,18)*10

colormap = plt.cm.coolwarm

fig.gca().set_color_cycle([colormap(i) for i in np.linspace(0, 1.0, v.shape[1])])

ax.plot(x,v)

plt.xticks(np.arange(-8,9)*45)
plt.xlim(-180,170)

ax.set_xlabel('Boxposition [deg]')
ax.set_ylabel('Proximity value')

plt.show()
'''