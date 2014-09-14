'''
Created on Sep 8, 2014

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
# left blank purposely for LAM
R_COVERAGE = 10.0
############################################


LAM_list = [0.001,0.002,0.003,0.004,0.005,0.006,0.007,0.008,0.009, 0.01]
# LAM_list = [0.000, 0.001,0.002]
expnum = len(LAM_list)

ParamsSet = [None for _ in range(expnum)]
TransProbSet = [None for _ in range(expnum)]

RESset_bell = [None for _ in range(expnum)]
RESset_myo = [None for _ in range(expnum)]
RESset_side = [None for _ in range(expnum)]
RESset_rnd = [None for _ in range(expnum)]
RESset_sidernd = [None for _ in range(expnum)]

V_opt_set_bell = [None for _ in range(expnum)]
A_opt_set_bell = [None for _ in range(expnum)]

tic = timeit.default_timer()

for ind, lam_cur in enumerate(LAM_list):
    print "---- ROUND:", ind+1,
    print "out of", expnum
    N = GetUpperboundN(lam_cur, R_COVERAGE)[0]
    ParamsSet[ind] = {'L': L, 'E': E, 'N': N, 'P': P, \
                      'A': A, \
                      'L_NC': L_NC, 'L_B': L_B, 'L_S': L_S, \
                      'E_B': E_B, 'E_S': E_S, \
                      'GAM': GAM, 'DELTA': DELTA, \
                      'LAM': lam_cur, 'R_COVERAGE': R_COVERAGE
                      }
    TransProbSet[ind] = BuildTransMatrix_Para(ParamsSet[ind])
    
    # Bellman
    V_bell, A_bell = BellmanSolver(TransProbSet[ind], ParamsSet[ind])
    V_opt_set_bell[ind] = V_bell
    A_opt_set_bell[ind] = A_bell 
    RESset_bell[ind] = GetOptResultList(V_bell,A_bell, TransProbSet[ind], ParamsSet[ind])
      
    # Myopic
    V_myo, A_myo = NaiveSolver_Myopic(TransProbSet[ind], ParamsSet[ind])
    RESset_myo[ind] = GetOptResultList(V_myo,A_myo, TransProbSet[ind], ParamsSet[ind])
     
    # Taking sides
    V_side, A_side = NaiveSolver_Side(TransProbSet[ind], ParamsSet[ind])
    RESset_side[ind] = GetOptResultList(V_side,A_side, TransProbSet[ind], ParamsSet[ind])
     
    # rndmzd
    RANDOM_COUNT = 50
    RE = []
    for rcount in range(RANDOM_COUNT):
        print "RANDOM: %d/%d running..." % (rcount+1,RANDOM_COUNT)
        V_rnd, A_rnd = NaiveSolver_Rnd(TransProbSet[ind], ParamsSet[ind])
        RE_rnd = GetOptResultList(V_rnd,A_rnd, TransProbSet[ind], ParamsSet[ind])
        if rcount == 0:
            RE = [0.0 for _ in range(len(RE_rnd))]
        for i in range(len(RE_rnd)):
            RE[i] = RE[i] + RE_rnd[i]
    for i in range(len(RE)):
        RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
    RESset_rnd[ind] = RE
    
    # Taking sides plus random actions
    RANDOM_COUNT = 50
    RE = []
    for rcount in range(RANDOM_COUNT):
        print "SIDELY RANDOM: %d/%d running..." % (rcount+1,RANDOM_COUNT)
        V_sidernd, A_sidernd = NaiveSolver_SideRandom(TransProbSet[ind], ParamsSet[ind])
        RE_sidernd = GetOptResultList(V_sidernd,A_sidernd, TransProbSet[ind], ParamsSet[ind])
        if rcount == 0:
            RE = [0.0 for _ in range(len(RE_sidernd))]
        for i in range(len(RE_sidernd)):
            RE[i] = RE[i] + RE_sidernd[i]
    for i in range(len(RE)):
        RE[i] = RE[i]*1.0/(1.0*RANDOM_COUNT)
    RESset_sidernd[ind] = RE
    
toc = timeit.default_timer()
print
print "Total time spent: ",
print toc - tic
    
print "Dumping...",
pickle.dump(expnum, open("../results/LAM_changing/expnum","w"))
pickle.dump(ParamsSet, open("../results/LAM_changing/Paramsset","w"))
pickle.dump(LAM_list, open("../results/LAM_changing/xaxis","w"))
pickle.dump(RESset_bell, open("../results/LAM_changing/bell","w"))
pickle.dump(RESset_myo, open("../results/LAM_changing/myo","w"))
pickle.dump(RESset_side, open("../results/LAM_changing/side","w"))
pickle.dump(RESset_rnd, open("../results/LAM_changing/rnd","w"))
pickle.dump(RESset_sidernd, open("../results/LAM_changing/sidernd","w"))
pickle.dump(V_opt_set_bell, open("../results/LAM_changing/V_opt_bell","w"))
pickle.dump(A_opt_set_bell, open("../results/LAM_changing/A_opt_bell","w"))
print "Finished"