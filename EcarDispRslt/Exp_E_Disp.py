'''
Created on Sep 4, 2014

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

expnum = pickle.load(open("../results/E_changing/expnum","r"))

x_axis_list = pickle.load(open("../results/E_changing/xaxis","r"))
RESset_bell = pickle.load(open("../results/E_changing/bell","r"))
RESset_myo = pickle.load(open("../results/E_changing/myo","r"))
RESset_side = pickle.load(open("../results/E_changing/side","r"))
RESset_rnd = pickle.load(open("../results/E_changing/rnd","r"))
RESset_sidernd = pickle.load(open("../results/E_changing/sidernd","r"))

# V_opt_set_bell = pickle.load(open("../results/E_changing/V_opt_bell","r"))
# A_opt_set_bell = pickle.load(open("../results/E_changing/A_opt_bell","r"))


y_v_avg_bell = [RESset_bell[i][0] for i in range(expnum)]
y_a1_steady_bell = [RESset_bell[i][1] for i in range(expnum)]
y_a2_steady_bell = [RESset_bell[i][2] for i in range(expnum)]
y_e_steady_bell = [RESset_bell[i][3] for i in range(expnum)]
y_QoS_steady_bell  = [RESset_bell[i][4] for i in range(expnum)]

y_v_avg_myo = [RESset_myo[i][0] for i in range(expnum)]
y_a1_steady_myo = [RESset_myo[i][1] for i in range(expnum)]
y_a2_steady_myo = [RESset_myo[i][2] for i in range(expnum)]
y_e_steady_myo = [RESset_myo[i][1] for i in range(expnum)]
y_QoS_steady_myo  = [RESset_myo[i][4] for i in range(expnum)]

y_v_avg_side = [RESset_side[i][0] for i in range(expnum)]
y_a1_steady_side = [RESset_side[i][1] for i in range(expnum)]
y_a2_steady_side = [RESset_side[i][2] for i in range(expnum)]
y_e_steady_side = [RESset_side[i][3] for i in range(expnum)]
y_QoS_steady_side  = [RESset_side[i][4] for i in range(expnum)]

y_v_avg_rnd = [RESset_rnd[i][0] for i in range(expnum)]
y_a1_steady_rnd = [RESset_rnd[i][1] for i in range(expnum)]
y_a2_steady_rnd = [RESset_rnd[i][2] for i in range(expnum)]
y_e_steady_rnd = [RESset_rnd[i][3] for i in range(expnum)]
y_QoS_steady_rnd  = [RESset_rnd[i][4] for i in range(expnum)]

y_v_avg_sidernd = [RESset_sidernd[i][0] for i in range(expnum)]
y_a1_steady_sidernd = [RESset_sidernd[i][1] for i in range(expnum)]
y_a2_steady_sidernd = [RESset_sidernd[i][2] for i in range(expnum)]
y_e_steady_sidernd = [RESset_sidernd[i][3] for i in range(expnum)]
y_QoS_steady_sidernd  = [RESset_sidernd[i][4] for i in range(expnum)]


# SHOW VALUATIONS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_v_avg_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_v_avg_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='GRDY')
plot(x_axis_list,y_v_avg_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='LOCA')
plot(x_axis_list,y_v_avg_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_v_avg_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LRND', linestyle='')
xlabel('Max. capacity $E$ of energy gateway',fontsize=14)
ylabel('Expected utility',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc='best', ncol=1,fancybox=True,shadow=True)
legend(loc='best',fancybox=True)
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('figure1.pdf')
plt.savefig(pp, format='pdf')
pp.close()
  
# Show steady action 1
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_a1_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_a1_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='GRDY')
plot(x_axis_list,y_a1_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='LOCA')
plot(x_axis_list,y_a1_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_a1_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LRND', linestyle='')
xlabel('Max. capacity $E$ of energy gateway',fontsize=14)
ylabel('Energy charging ($\mathcal{A}=1$) rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.6,0.58),fancybox=True)
# xlim([2,31])
ylim([-0.02,0.72])
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('figure2.pdf')
plt.savefig(pp, format='pdf')
pp.close()
    
    
# Show steady action 2
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_a2_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP', linestyle='--')
plot(x_axis_list,y_a2_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='GRDY', linestyle='--')
plot(x_axis_list,y_a2_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='LOCA', linestyle='--')
plot(x_axis_list,y_a2_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_a2_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LRND', linestyle='')
xlabel('Max. capacity $E$ of energy gateway',fontsize=14)
ylabel('Energy transferring ($\mathcal{A}=2$) rate',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
# legend(loc=(0.40,0.65), ncol=2,fancybox=True,shadow=True)
legend(loc=(0.6,0.56),fancybox=True)
# xlim([2,31])
ylim([-0.02,0.72])
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('figure3.pdf')
plt.savefig(pp, format='pdf')
pp.close()
   
   
# Steady state of E
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_e_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_e_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='GRDY')
plot(x_axis_list,y_e_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='LOCA')
plot(x_axis_list,y_e_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_e_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LRND', linestyle='')
xlabel('Max. capacity $E$ of energy gateway',fontsize=14)
ylabel('Steady energy state of energy gateway',fontsize=14)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.36,0.48), ncol=2,fancybox=True, prop={'size':13})
ylim([-0.02, 1.27])
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('figure4.pdf')
plt.savefig(pp, format='pdf')
pp.close()
    
    
# QoS
plt.figure(figsize=(4.5,5.0))
grid(True, which="both")
plot(x_axis_list,y_QoS_steady_bell,color='red',markerfacecolor='none', markeredgecolor='red', marker='o',markersize=8,label='MDP')
plot(x_axis_list,y_QoS_steady_myo,color='green',markerfacecolor='none', markeredgecolor='green', marker='^',markersize=8,label='GRDY')
plot(x_axis_list,y_QoS_steady_side,color='blue',markerfacecolor='none', markeredgecolor='blue', marker='s',markersize=8,label='LOCA')
plot(x_axis_list,y_QoS_steady_rnd,color='black',markerfacecolor='none', markeredgecolor='black', marker='d',markersize=8,label='RND', linestyle='')
plot(x_axis_list,y_QoS_steady_sidernd,color='magenta',markerfacecolor='none', markeredgecolor='magenta', marker='x',markersize=8,label='LRND', linestyle='')
xlabel('Max. capacity $E$ of energy gateway',fontsize=14)
ylabel('Transferring QoS of energy gateway',fontsize=16)
subplots_adjust(top=0.93,bottom=0.16,left=0.12, right=0.95)
legend(loc=(0.31, 0.66), ncol=2,fancybox=True, prop={'size':13})
ylim([-0.005, 0.26])
locs, labels = plt.yticks()
plt.setp(labels, rotation=90)
pp = PdfPages('figure5.pdf')
plt.savefig(pp, format='pdf')
pp.close()

# show()