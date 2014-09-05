'''
Created on 26 Aug, 2014

@author: yzhang28
'''

import numpy as np
import scipy as sp
from scipy.misc import factorial
import random
import math
from multiprocessing import Pool as ThreadPool
from multiprocessing import Process, Queue, Array, RawArray
import timeit
import time


R_COVERAGE = 10.0 # energy transfer distance of an energy gateway is 10.0
LAM_CONST = 0.005


def min3(inp1,inp2,inp3):
    lis = np.array([inp1, inp2, inp3])
    return lis.min(), np.argmin(lis)


def L_mat(l1, l2, params):
    mat_l = [[1.0/(params['L']) for _ in range(params['L'])] for _ in range(params['L'])]
    
    if (l1 in range(params['L'])) and (l2 in range(params['L'])):
        return mat_l[l1][l2]
    else:
        return 0.0


def P_mat(p1, p2, params):
    mat_p = [[1.0/(params['P']) for _ in range(params['P'])] for _ in range(params['P'])]
    
    if (p1 in range(params['P'])) and (p2 in range(params['P'])):
        return mat_p[p1][p2]
    else:
        return 0.0


# THIS FUNCTION IS ONLY FOR TEMPORARY USE
def N_mat(n1, n2, l1, l2, params):
    
    if (l2 in params['L_NC']) or (l2 in params['L_B']):
        if n2==0:
            return 1.0
        else:
            return 0.0
    elif l2 in params['L_S']:
        mat_n = [[1.0/(params['N']) for _ in range(params['N'])] for _ in range(params['N'])]
        if (n1 in range(params['N'])) and (n2 in range(params['N'])):
            return mat_n[n1][n2]
        else:
            return 0.0
    else:
        return 0.0
    
    
def E_mat(e1, e2, l1, l2,  act, params):
    eta_prob = 0.8
    xi_prob = 0.95
    rangeE = range(params['E'])
    
    if act==0:
        if e1==e2 and (e1 in rangeE) and (e2 in rangeE):
            return 1.0
        else:
            return 0.0
    elif act==1:  # charge from electricity charger
        if (l1 in params['L_NC']) or (l1 in params['L_S']):
            if e1==e2 and (e1 in rangeE) and (e2 in rangeE):
                return 1.0
            else:
                return 0.0
        elif (l1 in params['L_B']):
            if (e1 not in rangeE) or (e2 not in rangeE):
                return 0.0 
            elif e1 == params['E']-1:
                if e1==e2:
                    return 1.0
                else:
                    return 0.0
            else:
                if e1==e2:
                    return 1.0 - eta_prob
                elif e2 == 1+e1:
                    return eta_prob
                else:
                    return 0.0
        else:
            return 0.0
    elif act==2:
        if (e1 not in rangeE) or (e2 not in rangeE):
            return 0.0
        elif e1==0:
            if e1==e2:
                return 1.0
            else:
                return 0.0
        else:
            if e1==e2:
                return 1.0 - xi_prob
            elif e2==e1-1:
                return xi_prob
            else:
                return 0.0
    else:
        return 0.0


def OverallTransProb(l1,e1,n1,p1, l2,e2,n2,p2, act, params):
    
    overall_prob = 1.0 * L_mat(l1, l2, params) * \
                         E_mat(e1, e2, l1, l2,  act, params) * \
                         N_mat(n1, n2, l1, l2, params) * \
                         P_mat(p1, p2, params)
    return overall_prob


# def HashMatIndex(l1,e1,n1,p1, l2,e2,n2,p2, act, params):
#     # Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P'] 
#     _len_A = params['A']
#     
#     return \
#         l1 * _len_E * _len_N * _len_P * _len_L * _len_E * _len_N * _len_P * _len_A + \
#         e1 * _len_N * _len_P * _len_L * _len_E * _len_N * _len_P * _len_A + \
#         n1 * _len_P * _len_L * _len_E * _len_N * _len_P * _len_A + \
#         p1 * _len_L * _len_E * _len_N * _len_P * _len_A + \
#         l2 * _len_E * _len_N * _len_P * _len_A + \
#         e2 * _len_N * _len_P * _len_A + \
#         n2 * _len_P * _len_A + \
#         p2 * _len_A + \
#         act


def ReversedHashMatIndex(ind_lin, max_line_sizes_list):
# INPUT 1: The index in the linear matrix
# INPUT 2: A list, containing the maximum size of each dimension in the multi-dimensional matrix.
# REVERSED Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
    rem = ind_lin
    _mod_list = [item for item in reversed(max_line_sizes_list)]
    ind_mat = []
      
    for i in _mod_list:
        rem, mod_num = divmod(rem, i)
        ind_mat.insert(0, mod_num)
      
    return ind_mat
#     
#     _len_L, _len_E, _len_N, _len_P, _len_A = line_sizes[0], line_sizes[1], line_sizes[2], line_sizes[3], line_sizes[4] 
#     rem, _act = divmod(ind_lin, _len_A)
#       
#     rem, _p2 = divmod(rem, _len_P)
#     rem, _n2 = divmod(rem, _len_N)
#     rem, _e2 = divmod(rem, _len_E)
#     rem, _l2 = divmod(rem, _len_L)
#       
#     rem, _p1 = divmod(rem, _len_P)
#     rem, _n1 = divmod(rem, _len_N)
#     rem, _e1 = divmod(rem, _len_E)
#     _l1 = rem
#       
#     return _l1,_e1,_n1,_p1, _l2,_e2,_n2,_p2, _act

def SlicingListToSections(sec_list, proc_num, total_number):
    for i in range(proc_num):
        if i==0:
            _start = int(total_number/proc_num)*i
            _end = int(total_number/proc_num)*(i+1)
        elif i==proc_num-1:
            _start = int(total_number/proc_num)*i
            _end = total_number
        else:
            _start = int(total_number/proc_num)*i
            _end = int(total_number/proc_num)*(i+1)
        sec_list.append(range(_start, _end))

def BuildTransMatrix_Para(params):   
    
    def MatCalc(arr,sec, params):
        _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P'] 
        _len_A = params['A']
        _dimension_size = [_len_L, _len_E, _len_N, _len_P, _len_L, _len_E, _len_N, _len_P,  _len_A]
        
        for _ind_lin in sec:
            l1,e1,n1,p1, l2,e2,n2,p2, act = ReversedHashMatIndex(_ind_lin, _dimension_size)
            _c = OverallTransProb(l1,e1,n1,p1, l2,e2,n2,p2, act, params)
            arr[_ind_lin] = _c 

    
    _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P'] 
    _len_A = params['A']
    _total_cnt = (_len_L * _len_E * _len_N * _len_P) * (_len_L * _len_E * _len_N * _len_P) * _len_A
    trans_prob_linear = Array('d', np.zeros(_total_cnt))
    
    sec = []
    PROCNUM = 12l
    SlicingListToSections(sec, PROCNUM, _total_cnt)

    p = []
    print 'Building transition matrix...'
    for i in range(len(sec)):
        p.append( Process(target=MatCalc, args=(trans_prob_linear, sec[i], params)) )
#         p[-1].start()
#         p[-1].join()
    
    tic = timeit.default_timer()
    for proc in p:
        proc.start()
    for proc in p:
        proc.join()
    toc = timeit.default_timer()
#     print "CORE TIME - PARA: ",
#     print toc-tic
    
    trans_prob_mat = np.asarray(trans_prob_linear).reshape(_len_L, _len_E, _len_N, _len_P, _len_L, _len_E, _len_N, _len_P, _len_A)

    print 'Building transition matrix...DONE'
    return trans_prob_mat


def BuildTransMatrix(params): # 0,1,2
    rangeL = range(params['L'])
    rangeE = range(params['E'])
    rangeN = range(params['N'])
    rangeP = range(params['P'])
    rangeA = range(params['A'])
    _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P'] 
    _len_A = params['A']
    
    trans_prob_mat = np.zeros((_len_L, _len_E, _len_N, _len_P,_len_L, _len_E, _len_N, _len_P,_len_A))
    
    print 'Building transition matrix...'
    
    tic = timeit.default_timer()
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    for l2 in rangeL:
                        for e2 in rangeE:
                            for n2 in rangeN:
                                for p2 in rangeP:
                                    for act in rangeA:
#                                         math.factorial(500)
                                        trans_prob_mat[l1][e1][n1][p1][l2][e2][n2][p2][act] = OverallTransProb(l1,e1,n1,p1, l2,e2,n2,p2, act, params)
    tac = timeit.default_timer()
#     print "CORE TIME - NON-PARA: ",
#     print tac - tic
    
    print 'Building transition matrix...DONE'
    return trans_prob_mat

# tic = timeit.default_timer()
# mat_para = BuildTransMatrix_Para(PARAMS)
# toc = timeit.default_timer()
# print "Parallel: ",
# print toc - tic
# # print mat_para
#  
# print
# print '----------------------------------------------'
# print
#  
# tic = timeit.default_timer()
# mat = BuildTransMatrix(PARAMS)
# toc = timeit.default_timer()
# print "Non Parallel: ",
# print toc - tic
# # print mat
# 
# if (mat==mat_para).all():
#     print "GOOD: TWO MATRICES IDENTICAL"
# else:
#     print "WRONG!!!!"


# def N_mat(n1, n2, params):
#     def P_NPoisson(k=0):
#         return np.exp(-1*math.pi*LAM_CONST*np.power(R_COVERAGE,2))*np.power(math.pi*LAM_CONST*np.power(R_COVERAGE,2), k)/factorial(k, exact=True)
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
# 
# def GetParameterN():  # N starts from ZERO! [0,1,2,...N_max-1]
#     for i in range(65535):
#         if N_mat(0,i,None)==0:
#             return i-1+1
#   
# N_max = GetParameterN() # N starts from ZERO! [0,1,2,...N_max-1]
# 
# for x in range(N_max):
#     for y in range(N_max):
#         print N_mat(x,y,None),
#         print '   ',
#     print


def GetOptResultList(V,A, transmat, params):
#     rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']
    
    V_linear = V.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]
    A_linear = A.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]
    _act = np.bincount(A_linear)
    while len(_act) < 3:
        _act = np.append(_act, 0)
    
    v_avg = np.average(V_linear) # AVERAGE COST
    a1_avg = _act[1]*1.0/(1.0*len(A_linear)) # ACT_1_AVG
    
    return v_avg, a1_avg
    
#     v_avg = 0.0
#     a_avg = 0.0
#         
#     for l1 in rangeL:
#         for e1 in rangeE:
#             for n1 in rangeN:
#                 for p1 in rangeP:
#                     # GetValueAvg
#                     v_avg = v_avg + V[l1][e1][n1][p1]
# 
#                     # GetActionAvg
#                     a_avg = a_avg + A[l1][e1][n1][p1]
# 
#     v_avg = v_avg*1.0 / (1.0*len(rangeL)*len(rangeE)*len(rangeN)*len(rangeP))
#     a_avg = a_avg*1.0 / (1.0*len(rangeL)*len(rangeE)*len(rangeN)*len(rangeP))
#     
#     return [v_avg, a_avg] 
