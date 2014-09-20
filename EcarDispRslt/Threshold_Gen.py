'''
Created on Sep 19, 2014

@author: yzhang28
'''

import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox
import sys
from matplotlib.lines import fillStyles
from matplotlib.markers import MarkerStyle
sys.path.append("..")
from EcarCore.MDPfunc import *

from matplotlib.backends.backend_pdf import PdfPages



V_opt_set_bell_E_changing = pickle.load(open("../results/E_changing/V_opt_bell","r"))
A_opt_set_bell_E_changing = pickle.load(open("../results/E_changing/A_opt_bell","r"))
params_set_bell_E_changing = pickle.load(open("../results/E_changing/Paramsset","r"))
expnum_bell_E_changing = pickle.load(open("../results/E_changing/expnum","r"))


# V_opt_set_bell_LAM_changing = pickle.load(open("../results/LAM_changing/V_opt_bell","r"))
# A_opt_set_bell_LAM_changing = pickle.load(open("../results/LAM_changing/A_opt_bell","r"))
# params_set_bell_LAM_changing = pickle.load(open("../results/LAM_changing/Paramsset","r"))
# expnum_bell_LAM_changing = pickle.load(open("../results/LAM_changing/expnum","r"))

# f_v_e_charging = open('../V_opt_set_bell_E_changing', 'w')

sys.stdout = open('../results/Amat_N_P', 'w')
for i in range(expnum_bell_E_changing):
    L = params_set_bell_E_changing[i]['L']
    E = params_set_bell_E_changing[i]['E']
    for _l in range(L):
        for _e in range(E):
            print
            print "state L =", _l
            print "state E =", _e
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['l','e'], [_l,_e], params_set_bell_E_changing[i])
            print


sys.stdout = open('../results/Amat_E_P', 'w')
for i in range(expnum_bell_E_changing):
    L = params_set_bell_E_changing[i]['L']
    N = params_set_bell_E_changing[i]['N']
    for _l in range(L):
        for _n in range(N):
            print
            print "state L =", _l
            print "state N =", _n
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['l','n'], [_l,_n], params_set_bell_E_changing[i])


sys.stdout = open('../results/Amat_E_N', 'w')
for i in range(expnum_bell_E_changing):
    L = params_set_bell_E_changing[i]['L']
    P = params_set_bell_E_changing[i]['P']
    for _l in range(L):
        for _p in range(P):
            print
            print "state L =", _l
            print "state P =", _p
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['l','p'], [_l,_p], params_set_bell_E_changing[i])
            print
            

sys.stdout = open('../results/Amat_L_P', 'w')
for i in range(expnum_bell_E_changing):
    E = params_set_bell_E_changing[i]['E']
    N = params_set_bell_E_changing[i]['N']
    for _e in range(E):
        for _n in range(N):
            print
            print "state E =", _e
            print "state N =", _n
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['e','n'], [_e,_n], params_set_bell_E_changing[i])
            print
            

sys.stdout = open('../results/Amat_L_N', 'w')
for i in range(expnum_bell_E_changing):
    E = params_set_bell_E_changing[i]['E']
    P = params_set_bell_E_changing[i]['P']
    for _e in range(E):
        for _p in range(P):
            print
            print "state E =", _e
            print "state P =", _p
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['e','p'], [_e,_p], params_set_bell_E_changing[i])
            print


sys.stdout = open('../results/Amat_L_E', 'w')          
for i in range(expnum_bell_E_changing):
    N = params_set_bell_E_changing[i]['N']
    P = params_set_bell_E_changing[i]['P']
    for _n in range(N):
        for _p in range(P):
            print
            print "state N =", _n
            print "state P =", _p
            ShowMatrix(A_opt_set_bell_E_changing[i], 'a', ['n','p'], [_n,_p], params_set_bell_E_changing[i])
            print