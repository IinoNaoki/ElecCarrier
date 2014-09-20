'''
Created on Sep 20, 2014

@author: yzhang28
'''

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import random

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

xpos = [1,2,3,4,5,6,7,8,9,10]
ypos = [2,3,4,5,1,6,2,1,7,2]

xpos = [1,2,3,4,5,6,7,8,9,10,
        1,2,3,4,5,6,7,8,9,10,
        1,2,3,4,5,6,7,8,9,10]
ypos = [1,1,1,1,1,1,1,1,1,1,
        2,2,2,2,2,2,2,2,2,2,
        3,3,3,3,3,3,3,3,3,3]

num_elements = len(xpos)
zpos = np.zeros(len(xpos))
dx = np.ones(len(xpos))
dy = np.ones(len(xpos))
dz = [random.randint(1,5) for _ in range(len(ypos))]

# [1,2,3,4,5,6,7,8,9,10]

ax1.bar3d(xpos, ypos, zpos, dx, dy, dz, color='#00ceaa')
# plt.xlim([1,11])
# plt.ylim([1,4])
# plt.yticks((1,2,3),('1','2','3') )
# plt.axis('tight')

plt.gca().set_aspect('equal', adjustable='box')
plt.xlim([1,11])
plt.ylim([1,4])
plt.axis('equal')

plt.show()

# state L = 1
# state N = 2
# ---ACTION MATRIX---
# Line:  e
# Column:  p
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   0   0  
# 1   0   0  
# 0   0   0  

# state L = 2
# state N = 2
# ---ACTION MATRIX---
# Line:  e
# Column:  p
# 0   0   0  
# 0   0   0  
# 2   2   2  
# 2   2   2  
# 2   2   2  
# 2   2   2  


# state L = 1
# state E = 2
# ---ACTION MATRIX---
# Line:  n
# Column:  p
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  
# 1   1   0  


# state L = 2
# state E = 2
# ---ACTION MATRIX---
# Line:  n
# Column:  p
# 0   0   0  
# 0   0   0  
# 2   2   2  
# 2   2   2  
# 2   2   2  
# 2   2   2  
# 2   2   2  
# 2   2   2  
# 2   2   2  

state L = 1
state P = 1
---ACTION MATRIX---
Line:  e
Column:  n
1   1   1   1   1   1   1   1   1  
1   1   1   1   1   1   1   1   1  
1   1   1   1   1   1   1   1   1  
0   0   0   0   0   0   0   0   0  
0   0   0   0   0   0   0   0   0  
0   0   0   0   0   0   0   0   0  

state L = 2
state P = 1
---ACTION MATRIX---
Line:  e
Column:  n
0   0   0   0   0   0   0   0   0  
0   0   0   2   2   2   2   2   2  
0   0   2   2   2   2   2   2   2  
0   0   2   2   2   2   2   2   2  
0   0   2   2   2   2   2   2   2  
0   2   2   2   2   2   2   2   2  