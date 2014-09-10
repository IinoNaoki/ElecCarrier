'''
Created on Sep 9, 2014

@author: yzhang28
'''

import math
import numpy as np
from math import factorial
from EcarCore.header import*

R_COVERAGE = 10.0
LAM_CONST = 0.0010



############################################
LAM = 0.005
R_COVERAGE = 10.0
############################################
params = {'LAM':LAM, 'R_COVERAGE':R_COVERAGE}
 
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
 
 
def N_mat(n1, n2, params):
    _LAM = params['LAM']
    _R_COVERAGE = params['R_COVERAGE']
    _N, _residual = GetUpperboundN(_LAM, _R_COVERAGE)
 
    if n1 not in range(_N):
        return 0.0
    else:
        if n2 not in range(_N):
            return 0.0
        elif n2==_N-1:
            return P_SpatialPoisson_Pure(n2, _LAM, _R_COVERAGE) + _residual
        else:
            return P_SpatialPoisson_Pure(n2, _LAM, _R_COVERAGE)        
     
N = GetUpperboundN(LAM, R_COVERAGE)[0] 
for x in range(N):
    for y in range(N):
        print N_mat(x,y,params),
        print '  ',
    print