'''
Created on 26 Aug, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
import random

from EcarCore.header import *

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
          'GAM': 0.8
          }

def ImmediateCost(l1,e1,n1,p1, act, params):
    if (l1 in params['L_B']) and (act==1):
        return -1.0*params['E_B']*p1[l1]
    elif (l1 in params['L_S']) and (act==2):
        # 0.5 is a price
        return 0.5*params['E_S']
    else:
        return 0.0
    
def BellmanSolver(TransProb, params):
    print "MDP starts..."
    rangeL, rangeE, rangeN, rangeP = range('L'), range('E'), range('N'), range('P')
    V_op = [[[[0.0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    A_op = [[[[  0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        _v_temp = [None, None, None]
                        for act in [0,1,2]:
                            _s_tmp = 0.0
                            for l2 in rangeL:
                                for e2 in rangeE:
                                    for n2 in rangeN:
                                        for p2 in rangeP:
                                            _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                            _v_temp[act] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                        _v_min, _a_min = min3(_v_temp[0], _v_temp[1], _v_temp[2])
                        V_op[l1][e1][n1][p1] = _v_min
                        A_op[l1][e1][n1][p1] = _a_min
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op
        
def NaiveSolver_Myopic(TransProb, params):
    print "Myopic starts..."
    rangeL, rangeE, rangeN, rangeP = range('L'), range('E'), range('N'), range('P')
    V_op = [[[[0.0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    A_op = [[[[  0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    _v_temp, _a_temp = min3(ImmediateCost(l1,e1,n1,p1, 0, params),
                                            ImmediateCost(l1,e1,n1,p1, 1, params),
                                            ImmediateCost(l1,e1,n1,p1, 2, params))
                    A_op[l1][e1][n1][p1] = _a_temp
    
    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        act = A_op[l1][e1][n1][p1]
                        _s_tmp = 0.0
                        for l2 in rangeL:
                            for e2 in rangeE:
                                for n2 in rangeN:
                                    for p2 in rangeP:
                                        _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                        V_op[l1][e1][n1][p1] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op
        
def NaiveSolver_Rnd(TransProb, params):
    print "Random..."
    rangeL, rangeE, rangeN, rangeP = range('L'), range('E'), range('N'), range('P')
    V_op = [[[[0.0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    A_op = [[[[  0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    A_op[l1][e1][n1][p1] = random.randint(0,2)
    
    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        act = A_op[l1][e1][n1][p1]
                        _s_tmp = 0.0
                        for l2 in rangeL:
                            for e2 in rangeE:
                                for n2 in rangeN:
                                    for p2 in rangeP:
                                        _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                        V_op[l1][e1][n1][p1] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op
        
        
def NaiveSolver_Side(TransProb, params):
    print "Taking side action scheme..."
    rangeL, rangeE, rangeN, rangeP = range('L'), range('E'), range('N'), range('P')
    V_op = [[[[0.0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    A_op = [[[[  0 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    if l1 in params['L_NC']:
                        A_op[l1][e1][n1][p1] = 0
                    elif l1 in params['L_B']:
                        A_op[l1][e1][n1][p1] = 1
                    elif l1 in params['L_S']:
                        A_op[l1][e1][n1][p1] = 2
                    else:
                        print "ERROR in NaiveSolver_Side(TransProb, params)"
                        exit(0)
    
    while 1:
        delta = 0.0
        for l1 in rangeL:
            for e1 in rangeE:
                for n1 in rangeN:
                    for p1 in rangeP:
                        _v_old = V_op[l1][e1][n1][p1]
                        act = A_op[l1][e1][n1][p1]
                        _s_tmp = 0.0
                        for l2 in rangeL:
                            for e2 in rangeE:
                                for n2 in rangeN:
                                    for p2 in rangeP:
                                        _s_tmp = _s_tmp + TransProb[l1][e1][n1][p1][l2][e2][n2][p2][act] * V_op[l2][e2][n2][p2]
                        V_op[l1][e1][n1][p1] = ImmediateCost(l1,e1,n1,p1, act, params) + params['GAM'] * _s_tmp
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            return V_op, A_op