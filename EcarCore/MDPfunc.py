'''
Created on 26 Aug, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
import random

from EcarCore.header import *
from multiprocessing import Process, Queue, Array, Value


def ImmediateCost(l1,e1,n1,p1, act, params):
    def SellingPriceIntegral(params):
        _LAM = params['LAM']
        _R = params['R_COVERAGE']
        
        
#     # Initializing the price function
#     if params.has_key('PRICE_FUNC'):
#         Price_Func = params['PRICE_FUNC']
#     else:
#         Price_Func = [0.1, 1.0, 5.0]
        
    Price_Func = [0.1, 1.0, 5.0]
    
    if (l1 in params['L_B']) and (act==1):
        return -1.0*params['E_B'] * Price_Func[p1]
    elif (l1 in params['L_S']) and (e1>=params['E_S']) and (act==2):
        # 2.0 is a price
        return 1.0*params['E_S'] * n1
    else:
        return 0.0
#     return -1.0*np.power(0.1*e1,2)

def BellmanSolver(TransProb, params):
    print "MDP starts..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])

    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
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
                        _v_min, _a_min = max3(_v_temp[0], _v_temp[1], _v_temp[2])
                        V_op[l1][e1][n1][p1] = _v_min
                        A_op[l1][e1][n1][p1] = _a_min
                        
                        delta = delta if delta>np.fabs(V_op[l1][e1][n1][p1]-_v_old) else np.fabs(V_op[l1][e1][n1][p1]-_v_old)
        print "Delta=",delta
        if delta < params['DELTA']:
            print "MDP [DONE]"
            print
            return V_op, A_op
        
def NaiveSolver_Myopic(TransProb, params):
    print "Myopic starts..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])

    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    _v_temp, _a_temp = max3(ImmediateCost(l1,e1,n1,p1, 0, params),
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
            print "Myopic [DONE]"
            print
            return V_op, A_op
        
def NaiveSolver_Rnd(TransProb, params):
    print "Random..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']

    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
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
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    
    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
    
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
        if delta< params['DELTA']:
            print "Taking side action scheme [DONE]"
            print
            return V_op, A_op



def NaiveSolver_SideRandom(TransProb, params):
    print "Random..."
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']

    V_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ))
    A_op = np.zeros(( params['L'], params['E'], params['N'], params['P'] ), dtype=np.int)
    
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    if l1 in params['L_NC']:
                        A_op[l1][e1][n1][p1] = 0
                    elif l1 in params['L_B']:
                        A_op[l1][e1][n1][p1] = random.randint(0,1)
                    elif l1 in params['L_S']:
                        A_op[l1][e1][n1][p1] = random.randint(0,2)
                    else:
                        A_op[l1][e1][n1][p1] = 0
    
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