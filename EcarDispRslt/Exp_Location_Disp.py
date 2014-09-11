'''
Created on Sep 11, 2014

@author: yzhang28
'''


import pickle
import matplotlib.pyplot as plt
from pylab import *
from matplotlib.ticker import FuncFormatter
from matplotlib.transforms import Bbox
import sys
sys.path.append("..")
from EcarCore.MDPfunc import *

expnum = pickle.load(open("../results/LocDistr_changing/expnum","r"))

x_axis_list = pickle.load(open("../results/LocDistr_changing/xaxis","r"))
RESset_bell = pickle.load(open("../results/LocDistr_changing/bell","r"))
RESset_myo = pickle.load(open("../results/LocDistr_changing/myo","r"))
RESset_side = pickle.load(open("../results/LocDistr_changing/side","r"))
# RESset_rnd = pickle.load(open("../results/LocDistr_changing/rnd","r"))


y_v_avg_bell = [RESset_bell[i][0] for i in range(expnum)]
y_a1_steady_bell = [RESset_bell[i][1] for i in range(expnum)]
y_a2_steady_bell = [RESset_bell[i][2] for i in range(expnum)]
y_e_steady_bell = [RESset_bell[i][3] for i in range(expnum)]
y_QoS_steady_bell = [RESset_bell[i][4] for i in range(expnum)]

y_v_avg_myo = [RESset_myo[i][0] for i in range(expnum)]
y_a1_steady_myo = [RESset_myo[i][1] for i in range(expnum)]
y_a2_steady_myo = [RESset_myo[i][2] for i in range(expnum)]
y_e_steady_myo = [RESset_myo[i][3] for i in range(expnum)]
y_QoS_steady_myo = [RESset_myo[i][4] for i in range(expnum)]

y_v_avg_side = [RESset_side[i][0] for i in range(expnum)]
y_a1_steady_side = [RESset_side[i][1] for i in range(expnum)]
y_a2_steady_side = [RESset_side[i][2] for i in range(expnum)]
y_e_steady_side = [RESset_side[i][3] for i in range(expnum)]
y_QoS_steady_side = [RESset_side[i][4] for i in range(expnum)]

# y_v_avg_rnd = [RESset_rnd[i][0] for i in range(expnum)]
# y_a_avg_rnd = [RESset_rnd[i][1] for i in range(expnum)]
# y_a2_steady_rnd = [RESset_rnd[i][2] for i in range(expnum)]
# y_e_steady_rnd = [RESset_rnd[i][3] for i in range(expnum)]
# y_QoS_steady_rnd  = [RESset_rnd[i][4] for i in range(expnum)]



# SHOW ACTIONS
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_a1_steady_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_a1_steady_myo,color='green',marker='^',label='MYO')
plot(x_axis_list,y_a1_steady_side,color='black',marker='s',label='SIDE')
plot(x_axis_list,y_a2_steady_bell,color='red',linestyle='--',marker='o',label='MDP')
plot(x_axis_list,y_a2_steady_myo,color='green',linestyle='--',marker='^',label='MYO')
plot(x_axis_list,y_a2_steady_side,color='black',linestyle='--',marker='s',label='SIDE')
# plot(x_axis_list,y_a_avg_rnd,color='grey',linestyle='--',marker='v',label='RND')
xlabel('Location Distr',fontsize=16)
ylabel('Charging rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.65), ncol=2,fancybox=True,shadow=True)
legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)
# xlim([2,31])
# ylim([-0.02,0.9])


# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_v_avg_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_v_avg_myo,color='green',marker='^',label='MYO')
plot(x_axis_list,y_v_avg_side,color='black',marker='s',label='SIDE')
# plot(x_axis_list,y_v_avg_rnd,color='grey',linestyle='--',marker='v',label='RND')
xlabel('Location Distr',fontsize=16)
ylabel('Expected cost',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)


# Steady state of E
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_e_steady_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_e_steady_myo,color='green',marker='^',label='MYO')
plot(x_axis_list,y_e_steady_side,color='black',marker='s',label='SIDE')
# plot(x_axis_list,y_v_avg_rnd,color='grey',linestyle='--',marker='v',label='RND')
xlabel('Location Distr',fontsize=16)
ylabel('Steady state energy level',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)

# QoS
plt.figure(figsize=(4.5,5.0))
# grid(True, which="both")
plot(x_axis_list,y_QoS_steady_bell,color='red',marker='o',label='MDP')
plot(x_axis_list,y_QoS_steady_myo,color='green',marker='^',label='MYO')
plot(x_axis_list,y_QoS_steady_side,color='black',marker='s',label='SIDE')
# plot(x_axis_list,y_QoS_steady_rnd,color='grey',linestyle='--',marker='v',label='RND')
xlabel('Location Distr',fontsize=16)
ylabel('Steady state energy level',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best')
# locs, labels = plt.yticks()
# plt.setp(labels, rotation=90)

show()