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



def max3(inp1,inp2,inp3):
    lis = np.array([inp1, inp2, inp3])
    return lis.max(), np.argmax(lis)


def L_mat(l1, l2, params):
#     mat_l = [[1.0/(params['L']) for _ in range(params['L'])] for _ in range(params['L'])]
    if params.has_key('L_MAT'):
        mat_l = params['L_MAT']
    else:
        mat_l = [[0.02, 0.29, 0.69],
                 [0.02, 0.29, 0.69],
                 [0.02, 0.29, 0.69]]
    
    if (l1 in range(params['L'])) and (l2 in range(params['L'])):
        return mat_l[l1][l2]
    else:
        return 0.0

def P_mat(p1, p2, params):
    
    if params.has_key('P_MAT'):
        mat_p = params['P_MAT']
    else:
        mat_p = [[1.0/(params['P']) for _ in range(params['P'])] for _ in range(params['P'])]
        
    if (p1 in range(params['P'])) and (p2 in range(params['P'])):
        return mat_p[p1][p2]
    else:
        return 0.0

    
def P_SpatialPoisson_Pure(k, LAM, R_COVERAGE):
    return np.exp(-1*math.pi*LAM*np.power(R_COVERAGE,2))*np.power(math.pi*LAM*np.power(R_COVERAGE,2), k)/factorial(k)

def GetUpperboundN(LAM, R_COVERAGE):
    _n = 0
    _sum = 0.0
    while 1:
        _sum = _sum + P_SpatialPoisson_Pure(_n, LAM, R_COVERAGE)
        _residual = 1.0 - _sum
        if _residual < 0.0001:
            return _n + 1, _residual
        else:
            _n = _n + 1

def N_mat(n1, n2, l1, l2, params):
    _LAM = params['LAM']
    _R_COVERAGE = params['R_COVERAGE']
    _N, _residual = GetUpperboundN(_LAM, _R_COVERAGE)
    
    if (l2 in params['L_NC']) or (l2 in params['L_B']):
        if (n1 in range(_N)) and n2==0:
            return 1.0
        else:
            return 0.0
    elif l2 in params['L_S']:
        if n1 not in range(_N):
            return 0.0
        else:
            if n2 not in range(_N):
                return 0.0
            elif n2==_N-1:
                return P_SpatialPoisson_Pure(n2, _LAM, _R_COVERAGE) + _residual
            else:
                return P_SpatialPoisson_Pure(n2, _LAM, _R_COVERAGE)        
    else:
        return 0.0


def E_mat(e1, e2, l1, l2,  act, params):
    eta_prob = 0.85 # prob of succ charging
    xi_prob = 0.99  # prob of succ transferring
    
    rangeE = range(params['E'])
    
    if act==0: # DO NOTHING
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
                elif e2 == min(e1+params['E_B'], params['E']-1):
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
            elif e2==max(0, e1-params['E_S']):
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

def ShowMatrix(Mat, mode, fixdims, fixnums, params):
    if Mat==None:
        print "ERROR INPUT ShowMatrix()"
        exit()
        
    if mode=='a': # Show action
        print "---ACTION MATRIX---"
    elif mode=='v': # Show value
        print "---UTILITY MATRIX---"
    else:
        print "ERROR, UNKNOWN MATRIX"
        exit()
#     print 'here'
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    dimList = ['l', 'e', 'n', 'p']
    feasList = [rangeL, rangeE, rangeN, rangeP]
    for item in fixdims:
        del(feasList[dimList.index(item)])
        del(dimList[dimList.index(item)])
    print 'Line: ', dimList[0]
    print 'Column: ', dimList[1]
    
#     print 'here'
    fix1, fix2 = fixnums[0], fixnums[1]
    for ra in feasList[0]:
        for rb in feasList[1]:
            if fixdims==['l','e']:
                if mode=='a':
                    print "%d" % Mat[fix1][fix2][ra][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[fix1][fix2][ra][rb],
                else:
                    print "ERROR, POS 1"
                    exit()
                print ' ',
            elif fixdims==['l','n']:
                if mode=='a':
                    print "%d" % Mat[fix1][ra][fix2][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[fix1][ra][fix2][rb],
                else:
                    print "ERROR, POS 2"
                    exit()
                print ' ',
            elif fixdims==['l','p']:
                if mode=='a':
                    print "%d" % Mat[fix1][ra][rb][fix2],
                elif mode=='v':
                    print "%8.3f" % Mat[fix1][ra][rb][fix2],
                else:
                    print "ERROR, POS 3"
                    exit()
                print ' ',
            elif fixdims==['e','n']:
                if mode=='a':
                    print "%d" % Mat[ra][fix1][fix2][rb],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][fix1][fix2][rb],
                else:
                    print "ERROR, POS 4"
                    exit()
                print ' ',
            elif fixdims==['e','p']:
                if mode=='a':
                    print "%d" % Mat[ra][fix1][rb][fix2],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][fix1][rb][fix2],
                else:
                    print "ERROR, POS 5"
                    exit()
                print ' ',
            elif fixdims==['n','p']:
                if mode=='a':
                    print "%d" % Mat[ra][rb][fix1][fix2],
                elif mode=='v':
                    print "%8.3f" % Mat[ra][rb][fix1][fix2],
                else:
                    print "ERROR, POS 6"
                    exit()
                print ' ',
            else:
                print "ERROR, POS 7"
                exit()
        print
    

def HashMatIndex(ind_mat, max_dimension_sizes_list):
    # Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
    if not len(ind_mat)==len(max_dimension_sizes_list):
        print "Error in HashMatIndex"
        exit(0)
    prodnt = np.append(np.delete(max_dimension_sizes_list,0),1)
    _sum = 0
    for i,item in enumerate(ind_mat):
        _tmp = 1
        for j in range(i,len(prodnt)):
            _tmp = _tmp * prodnt[j]
        _sum = _sum + item*_tmp
    return int(_sum)


def ReversedHashMatIndex(ind_lin, max_dimension_sizes_list):
# INPUT 1: The index in the linear matrix
# INPUT 2: A list, containing the maximum size of each dimension in the multi-dimensional matrix.
# REVERSED Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...Ha...sh
    rem = ind_lin
    _mod_list = [item for item in reversed(max_dimension_sizes_list)]
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
    
    def subfunc_MatCalc(arr,sec, params):
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
    PROCNUM = 12
    SlicingListToSections(sec, PROCNUM, _total_cnt)

    p = []
    print 'Building transition matrix...'
    for i in range(len(sec)):
        proc = Process(target=subfunc_MatCalc, args=(trans_prob_linear, sec[i], params))
        proc.start()
        p.append(proc)
        
    for proc in p:
        proc.join()
    
    trans_prob_mat = np.asarray(trans_prob_linear).reshape(_len_L, _len_E, _len_N, _len_P, _len_L, _len_E, _len_N, _len_P, _len_A)

    print 'Building transition matrix...[DONE]'
    return trans_prob_mat


# def BuildTransMatrix(params): # 0,1,2
#     rangeL = range(params['L'])
#     rangeE = range(params['E'])
#     rangeN = range(params['N'])
#     rangeP = range(params['P'])
#     rangeA = range(params['A'])
#     _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P'] 
#     _len_A = params['A']
#     
#     trans_prob_mat = np.zeros((_len_L, _len_E, _len_N, _len_P,_len_L, _len_E, _len_N, _len_P,_len_A))
#     
#     print 'Building transition matrix...'
#     
#     for l1 in rangeL:
#         for e1 in rangeE:
#             for n1 in rangeN:
#                 for p1 in rangeP:
#                     for l2 in rangeL:
#                         for e2 in rangeE:
#                             for n2 in rangeN:
#                                 for p2 in rangeP:
#                                     for act in rangeA:
# #                                         math.factorial(500)
#                                         trans_prob_mat[l1][e1][n1][p1][l2][e2][n2][p2][act] = OverallTransProb(l1,e1,n1,p1, l2,e2,n2,p2, act, params)
#     
#     print 'Building transition matrix...[DONE]'
#     return trans_prob_mat


def SteadyStateMatrix(transmat, optA, params):
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    total_dim = params['L'] * params['E'] * params['N'] * params['P']
    expanded_matrix = np.matrix( [[0.0 for _ in range(total_dim)] for _ in range(total_dim)] )
    search_list = [[[[-1 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    expd_x_ind, expd_y_ind = 0, 0
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    for l2 in rangeL:
                        for e2 in rangeE:
                            for n2 in rangeN:
                                for p2 in rangeP:
                                    act = optA[l1][e1][n1][p1]
                                    expanded_matrix[expd_x_ind, expd_y_ind] = transmat[l1][e1][n1][p1][l2][e2][n2][p2][act]
                                    expd_y_ind = expd_y_ind + 1
                    search_list[l1][e1][n1][p1] = expd_x_ind
                    expd_x_ind = expd_x_ind + 1
                    expd_y_ind = 0
    
    p_hat = expanded_matrix - np.diag(np.array([1.0 for _ in range(total_dim)]))
    for x in range(total_dim):
        p_hat[x,total_dim-1] = 1.0
    a_rhs = np.zeros(total_dim)
    a_rhs[total_dim-1] = 1.0
    steady_p = a_rhs * p_hat.getI()
    steady_p_transf = [[[[-1 for _ in rangeP] for _ in rangeN] for _ in rangeE] for _ in rangeL]
    
    for l in rangeL:
        for e in rangeE:
            for n in rangeN:
                for p in rangeP:
                    steady_p_transf[l][e][n][p] = steady_p[0,search_list[l][e][n][p]]
    return steady_p_transf
    


def GetOptResultList(V,A, transmat, params):
    rangeL, rangeE, rangeN, rangeP = range(params['L']), range(params['E']), range(params['N']), range(params['P'])
    _len_L, _len_E, _len_N, _len_P = params['L'], params['E'], params['N'], params['P']
    steady_mat = SteadyStateMatrix(transmat, A, params)
        
    V_linear = V.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]    
    v_avg = np.average(V_linear) # AVERAGE COST
    A_linear = A.reshape(1, _len_L*_len_E*_len_N*_len_P)[0]
    _act = np.bincount(A_linear)
    while len(_act) < 3:
        _act = np.append(_act, 0)
    a1_avg = _act[1]*1.0/(1.0*len(A_linear)) # ACT_1_AVG
    a2_avg = _act[2]*1.0/(1.0*len(A_linear)) # ACT_2_AVG
    
    e_steady = 0.0
    QoS_steady = 0.0
    a1_steady = 0.0
    a2_steady = 0.0
    for l1 in rangeL:
        for e1 in rangeE:
            for n1 in rangeN:
                for p1 in rangeP:
                    e_steady = e_steady + 1.0 * e1 * steady_mat[l1][e1][n1][p1]
                    if A[l1][e1][n1][p1] == 1:
                        a1_steady = a1_steady + 1.0 * steady_mat[l1][e1][n1][p1]
                    if A[l1][e1][n1][p1] == 2:
                        a2_steady = a2_steady + 1.0 * steady_mat[l1][e1][n1][p1]
                    if (l1 in params['L_S']) and (e1>=params['E_S']) and (A[l1][e1][n1][p1]==2):
                        QoS_steady = QoS_steady +  1.0*steady_mat[l1][e1][n1][p1]
    
    return v_avg, a1_steady, a2_steady, e_steady, QoS_steady
#            0       1           2         3          4

