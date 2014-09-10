'''
Created on Sep 9, 2014

@author: yzhang28
'''

import pickle
from multiprocessing import Pool, Array

import timeit


import sys
sys.path.append("..")

from EcarCore.MDPfunc import *
from EcarCore.header import *

############################################
# PARAMETERS
############################################
L = 3
E = 5
# N Calculated from LAM and R_COVERAGE
P = 3
A = 3
L_NC, L_B, L_S = [0], [1], [2]
E_B, E_S = 1, 1
GAM = 0.95
DELTA = 0.01
LAM = 0.005
R_COVERAGE = 10.0
############################################

PriceFunc_list = [lambda x: [0.01, 1.5, 1.0][x],
                  lambda x: [1.5, 5.0, 10.0][x],
                  lambda x: [5.0, 20.0, 50.0][x]]

PriceFunc_list_picklable = range(len(PriceFunc_list))

expnum = len(PriceFunc_list)

ParamsSet = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]

RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_side = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]

tic = timeit.default_timer()

for ind, pfunc_cur in enumerate(PriceFunc_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum
    N = GetUpperboundN(LAM, R_COVERAGE)[0]
    ParamsSet[ind] = {'L': L, 'E': E, 'N': N, 'P': P, \
                      'A': A, \
                      'L_NC': L_NC, 'L_B': L_B, 'L_S': L_S, \
                      'E_B': E_B, 'E_S': E_S, \
                      'GAM': GAM, 'DELTA': DELTA, \
                      'LAM': LAM, 'R_COVERAGE': R_COVERAGE, \
                      'PRICE_FUNC': pfunc_cur
                      }
    TransProbSet[ind] = BuildTransMatrix_Para(ParamsSet[ind])
    
    # Bellman
    V_bell, A_bell = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
    RESset_bell[ind] = GetOptResultList(V_bell,A_bell, TransProbSet[ind], ParamsSet[ind])
     
    # Myopic
    V_myo, A_myo = NaiveSolver_Myopic(TransProbSet[ind], ParamsSet[ind])
    RESset_myo[ind] = GetOptResultList(V_myo,A_myo, TransProbSet[ind], ParamsSet[ind])
    
    # Taking sides
    V_side, A_side = NaiveSolver_Side(TransProbSet[ind], ParamsSet[ind])
    RESset_side[ind] = GetOptResultList(V_side,A_side, TransProbSet[ind], ParamsSet[ind])
    
    # rndmzd
#     V_rnd, A_rnd = NaiveSolver_Rnd(TransProbSet[ind], ParamsSet[ind])
#     RESset_rnd[ind] = GetOptResultList(V_rnd,A_rnd, TransProbSet[ind], ParamsSet[ind])
    
toc = timeit.default_timer()
print
print "Total time spent: ",
print toc - tic
    
print "Dumping...",
pickle.dump(expnum, open("../results/PriceFunc_changing/expnum","w"))
# THIS IS NON PICKABLE # pickle.dump(ParamsSet, open("../results/PriceFunc_changing/Paramsset","w"))
pickle.dump(PriceFunc_list_picklable, open("../results/PriceFunc_changing/xaxis","w"))
pickle.dump(RESset_bell, open("../results/PriceFunc_changing/bell","w"))
pickle.dump(RESset_myo, open("../results/PriceFunc_changing/myo","w"))
pickle.dump(RESset_side, open("../results/PriceFunc_changing/side","w"))
# pickle.dump(RESset_rnd, open("../results/PriceFunc_changing/rnd","w"))
print "Finished"