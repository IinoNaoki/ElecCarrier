'''
Created on Sep 14, 2014

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

expnum = pickle.load(open("../results/EBvES_changing/expnum","r"))

x_axis_list = pickle.load(open("../results/EBvES_changing/xaxis","r"))
RESset_bell = pickle.load(open("../results/EBvES_changing/bell","r"))
RESset_myo = pickle.load(open("../results/EBvES_changing/myo","r"))
RESset_side = pickle.load(open("../results/EBvES_changing/side","r"))
RESset_rnd = pickle.load(open("../results/EBvES_changing/rnd","r"))
RESset_sidernd = pickle.load(open("../results/EBvES_changing/sidernd","r"))


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
# y_a1_steady_rnd = [RESset_rnd[i][1] for i in range(expnum)]
# y_a2_steady_rnd = [RESset_rnd[i][2] for i in range(expnum)]
# y_e_steady_rnd = [RESset_rnd[i][3] for i in range(expnum)]
# y_QoS_steady_rnd  = [RESset_rnd[i][4] for i in range(expnum)]
# 
# y_v_avg_sidernd = [RESset_sidernd[i][0] for i in range(expnum)]
# y_a1_steady_sidernd = [RESset_sidernd[i][1] for i in range(expnum)]
# y_a2_steady_sidernd = [RESset_sidernd[i][2] for i in range(expnum)]
# y_e_steady_sidernd = [RESset_sidernd[i][3] for i in range(expnum)]
# y_QoS_steady_sidernd  = [RESset_sidernd[i][4] for i in range(expnum)]


# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_v_avg_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_v_avg_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO')
plot(x_axis_list,y_v_avg_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='SIDE')
# plot(x_axis_list,y_v_avg_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_v_avg_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='d',markersize=8,label='RND', linestyle='')
xlabel('$E_B:E_S$ pattern',fontsize=16)
ylabel('Expected cost',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best', fancybox=True)
# ylim([-24,10])
locs, labels = plt.xticks()
#plt.xticks((1,2,3),('Location\npattern 1', 'Location\npattern 2', 'Location\npattern 3',) )
#xlim([0.90, 3.10])
# plt.setp(labels, rotation=10)
  
  
# Show steady action 1
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_a1_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_a1_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO')
plot(x_axis_list,y_a1_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='SIDE')
# plot(x_axis_list,y_a1_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_a1_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='d',markersize=8,label='RND', linestyle='')
xlabel('$E_B:E_S$ pattern',fontsize=16)
ylabel('Charging rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.65), ncol=2,fancybox=True,shadow=True)
legend(loc='best', fancybox=True)
# ylim([-0.02,0.72])
locs, labels = plt.xticks()
#plt.xticks((1,2,3),('Location\npattern 1', 'Location\npattern 2', 'Location\npattern 3',) )
#xlim([0.90, 3.10])
# plt.setp(labels, rotation=10)
   
   
# Show steady action 2
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_a2_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP', linestyle='--')
plot(x_axis_list,y_a2_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO', linestyle='--')
plot(x_axis_list,y_a2_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='SIDE', linestyle='--')
# plot(x_axis_list,y_a2_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_a2_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='d',markersize=8,label='RND', linestyle='')
xlabel('$E_B:E_S$ pattern',fontsize=16)
ylabel('Charging rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.65), ncol=2,fancybox=True,shadow=True)
legend(loc='best', fancybox=True)
# ylim([-0.02,0.72])
locs, labels = plt.xticks()
#plt.xticks((1,2,3),('Location\npattern 1', 'Location\npattern 2', 'Location\npattern 3',) )
#xlim([0.90, 3.10])
# plt.setp(labels, rotation=10)
  
  
# Steady state of E
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_e_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_e_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO')
plot(x_axis_list,y_e_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='SIDE')
# plot(x_axis_list,y_e_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_e_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='d',markersize=8,label='RND', linestyle='')
xlabel('$E_B:E_S$ pattern',fontsize=16)
ylabel('Steady state energy level',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best', fancybox=True)
# ylim([-0.15,4.0])
locs, labels = plt.xticks()
#plt.xticks((1,2,3),('Location\npattern 1', 'Location\npattern 2', 'Location\npattern 3',) )
#xlim([0.90, 3.10])
# plt.setp(labels, rotation=10)
 
 
# QoS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_QoS_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_QoS_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='MYO')
plot(x_axis_list,y_QoS_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='SIDE')
# plot(x_axis_list,y_QoS_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
# plot(x_axis_list,y_QoS_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='d',markersize=8,label='RND', linestyle='')
xlabel('$E_B:E_S$ pattern',fontsize=16)
ylabel('QoS of energy charging',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc=(0.55, 0.2), fancybox=True)
# ylim([-0.005,0.16])
locs, labels = plt.xticks()
#plt.xticks((1,2,3),('Location\npattern 1', 'Location\npattern 2', 'Location\npattern 3',) )
#xlim([0.90, 3.10])
# plt.setp(labels, rotation=10)


show()