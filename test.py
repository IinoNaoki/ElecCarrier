'''
Created on 28 Aug, 2014

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




# import numpy as np
# 
# A = 2
# B = 3
# C = 4
# D = 5
# ALL = A*B*C*D
# 
# def hashing(a,b,c,d, A,B,C,D):
#     def sggn(pp):
#         if pp>0:
#             return pp
#         else:
#             return 0
#     return a*B*C*D + b*C*D + c*D + d
# 
# 
# a = np.zeros((A,B,C,D))
# b_compare = a.reshape(1, ALL) 
# # print a
# # print
# 
# count = 0
# for ia in range(A):
#     for ib in range(B):
#         for ic in range(C):
#             for idd in range(D):
#                 count = count + 1
#                 a[ia][ib][ic][idd] = count
# # print a
# # print '----------------------------'
# 
# b = a.reshape(1,ALL)
# print b
# print
# 
# count = 0
# for ia in range(A):
#     for ib in range(B):
#         for ic in range(C):
#             for idd in range(D):
#                 count = count + 1
#                 k = hashing(ia, ib, ic, idd, A, B, C, D)
#                 b_compare[0][k] = count
# print b_compare
# 
# 
# ccc = np.zeros(10)
# print ccc