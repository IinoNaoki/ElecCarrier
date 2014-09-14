'''
Created on 28 Aug, 2014

@author: yzhang28
'''

import numpy as np
import matplotlib.pyplot as plt


# N = 5
# menMeans   = (20, 35, 30, 35, 27)
# womenMeans = (25, 32, 34, 20, 25)
# aaaMeans = (55, 33, 36, 45, 48)
# 
# bottom1 = menMeans
# bottom2 = tuple(sum(t) for t in zip(menMeans, womenMeans))
# ind = np.arange(N)    # the x locations for the groups
# width = 0.45       # the width of the bars: can also be len(x) sequence
#  
# p1 = plt.bar(ind, menMeans,   width, color='r')
# p2 = plt.bar(ind, womenMeans, width, color='y', bottom=menMeans)
# p3 = plt.bar(ind, aaaMeans, width, color='g', bottom=bottom2)
#  
# plt.ylabel('Scores')
# plt.title('Scores by group and gender')
# plt.xticks(ind+width/2., ('G1', 'G2', 'G3', 'G4', 'G5') )
# # plt.yticks(np.arange(0,81,10))
# # plt.legend( (p1[0], p2[0]), ('Men', 'Women') )
#  
# plt.show()
# 
# 
# # aaa = zip((1,2,3),(4,5,6))
# # print aaa
import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox
import sys

a = [1,2,3,4,5]
b = [i*3 for i in a]
plot(a,b,color='cyan',markerfacecolor='none', markeredgecolor='cyan', marker='d',markersize=8,label='RND', linestyle='')
show()