'''
Created on 28 Aug, 2014

@author: yzhang28
'''

# # WORKED
# from multiprocessing.dummy import Pool, Process, Value, Array
# import numpy as np
# import timeit
# import time
# import math
#  
#  
# def f(a,sec):
#     for i in range(len(sec)):
#         c = math.factorial(a[i])
#         a[i] = a[i]
#  
# COUNT = 3000
#  
# arr = Array('d', range(COUNT))
# 
# sec = []
# p = []
#  
# for i in range(COUNT/1000):
#     sec.append( range(1000*i+1, 1000*(i+1)) )
#  
# tic = timeit.default_timer()
# for i in range(len(sec)):
#     p.append( Process(target=f, args=(arr,sec[i])) )
#  
# for proc in p:
#     proc.start()
# for proc in p:
#     proc.join()
#  
# toc = timeit.default_timer()
# print toc - tic
# # print arr[10:20]
#  
#  
# sn = range(1,COUNT)
# tic = timeit.default_timer()
# f(sn, range(len(sn)))
# toc = timeit.default_timer()
# print toc - tic 

import math
import numpy as np
from math import factorial
from EcarCore.header import*

R_COVERAGE = 10.0
LAM_CONST = 0.0010

# def N_mat(n1, n2, params):
#     def P_NPoisson(k=0):
#         return np.exp(-1*math.pi*LAM_CONST*np.power(R_COVERAGE,2))*np.power(math.pi*LAM_CONST*np.power(R_COVERAGE,2), k)/factorial(k)
#     def AppxSumToOne(n2=0):
#         '''
#         summation of P^{N}(0), P^{N}(1), to P^{N}(N2)
#         The function is used to check if P^{N}(N2+1) should be neglected  
#         '''
#         if n2<0:
#             return 0
#         else:
#             return P_NPoisson(n2) + AppxSumToOne(n2-1) 
#     if 1.0-AppxSumToOne(n2-1)<0.0001:
#         return 0
# #         return 1.0-AppxSumToOne(n2-1)
#     else:
#         return P_NPoisson(n2)
 
# def GetParameterN():  # N starts from ZERO! [0,1,2,...N_max-1]
#     for i in range(65535):
#         if N_mat(0,i,None)==0:
#             return i-1+1
#    
# N_max = GetParameterN() # N starts from ZERO! [0,1,2,...N_max-1]


a,b = 5, 3
print min(a,b)