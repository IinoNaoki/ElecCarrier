'''
Created on Sep 9, 2014

@author: yzhang28
'''


# WORKED
from multiprocessing.dummy import Pool, Process, Value, Array
import numpy as np
import timeit
import time
import math
  
  
def f(a,sec):
    for i in range(len(sec)):
        c = math.factorial(a[i])
        a[i] = a[i]
  
COUNT = 3000
  
arr = Array('d', range(COUNT))
 
sec = []
p = []
  
for i in range(COUNT/1000):
    sec.append( range(1000*i+1, 1000*(i+1)) )
  
tic = timeit.default_timer()
for i in range(len(sec)):
    p.append( Process(target=f, args=(arr,sec[i])) )
  
for proc in p:
    proc.start()
for proc in p:
    proc.join()
  
toc = timeit.default_timer()
print toc - tic
# print arr[10:20]
  
  
sn = range(1,COUNT)
tic = timeit.default_timer()
f(sn, range(len(sn)))
toc = timeit.default_timer()
print toc - tic 

