'''
Created on Sep 3, 2014

@author: yzhang28
'''

import pickle
import multiprocessing

import sys
sys.path.append("..")

from EcarCore.MDPfunc import *

# PARAMS including
PARAMS = {
          'L': 3,
          'E': 10,
          'N': 10,
          'P': 10,
          'L_NC': [0],
          'L_B': [1],
          'L_S': [2],
          'E_B': 1,
          'E_S': 1,
          'GAM': 0.8,
          'DELTA': 0.01
          }

L = 3
# left blank purposely for E
N = 10
P = 10
L_NC, L_B, L_S = [0], [1], [2]
E_B, E_S = 1, 1
GAM = 0.8
DELTA = 0.01

E_list = [1,2,3,4,5,6,7,8,9,10]
expnum = len(E_list)

ParamsSet = [None for _ in range(expnum)]
RESset_bell = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]

for ind, e_cur in enumerate(E_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum
    ParamsSet[ind] = {'L': L, 'E': e_cur, 'N': N, 'P': P, \
                      'L_NC': L_NC, 'L_B': L_B, 'L_S': L_S, \
                      'E_B': E_B, 'E_S': E_S, \
                      'GAM': GAM, 'DELTA': DELTA
                      }
    TransProbSet[ind] = BuildTransMatrix_Para(ParamsSet[ind])
    
    V_bell, A_bell = BellmanSolver(TransProbSet[ind], ParamsSet[ind])