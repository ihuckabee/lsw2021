# -*- coding: utf-8 -*-
"""
Created on Thu Jun 24 17:37:02 2021

@author: Huckabee
"""
from math import inf
import pandas as pd
from scipy.signal import find_peaks 
import numpy as np
import pdb
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt 
import glob 
filenames = glob.glob('creatinglines/res/5777g4.44z+0.00a+0.00t01-ref107857_3000-3500_xit1.0_test0.spec')
list_of_dfs = [pd.read_fwf(filename) for filename in filenames]
Fn_arr = []
wlspec_arr = []
for i in range(len(list_of_dfs)):
    spec = list_of_dfs[i]
    spec.columns = ['wl','Fn','F'] 
    spec.dropna(subset = ['Fn', 'F'], inplace = True )
    Fn_arr.append(spec['Fn'])
    wlspec_arr.append(spec['wl'])
#***setting up 5A windows
wldict = dict([])
fdict = dict([])
wl_entries = []
f_entries = []
start = 0
arraynum = 0
for i in range(len(wlspec_arr)): 
    for j in range(len(wlspec_arr[i])):
        if start >= 250:
            wl_entries = []
            f_entries = []
            start = 0
            arraynum += 1
        wl_entries.append(wlspec_arr[i][j])
        f_entries.append(Fn_arr[i][j])
        wldict[arraynum] = wl_entries
        fdict[arraynum] = f_entries
        start += 1

#***reading in equivalent widths
filenames = glob.glob('creatinglines/res/5777g4.44z+0.00a+0.00t01-ref107857_3000-3500_xit1.0_test0.eqw')
list_of_dfs = [pd.read_fwf(filename) for filename in filenames]
wleqw_arr = []
eqw_arr = []
for i in range(len(list_of_dfs)):
    eqw = list_of_dfs[i]
    if len(eqw.columns) > 13:
        eqw = eqw.drop(eqw.columns[[13,14,15]], axis = 1)
    eqw = eqw.drop(eqw.columns[[6,7,8,9,10,11,12]], axis =1)
    eqw.columns = ['element','ion','wl','exc', 'loggf', 'ew'] 
    eqw.dropna(subset = ['loggf', 'ew'], inplace = True )
    wleqw_arr.append(eqw['wl'])
    eqw_arr.append(eqw['ew'])

#linelists are not in order -- matching 
reduced_eqw = []
reduced_wl = []
for i in range(len(wleqw_arr)):
    templist_eqw = []
    templist_wl = []
    wl = 3002.5
    wleqw_arr_new= list(sorted(wleqw_arr[i][1:]))
    sort_index = np.argsort(wleqw_arr[i][1:])
    eqw_arr_new = np.asarray(eqw_arr[i][1:])
    eqw_arr_sorted = np.take_along_axis(eqw_arr_new, sort_index, axis=0)
    for j in range(len(eqw_arr_sorted)):
        templist_eqw.append(float(eqw_arr_sorted[j])/float(wleqw_arr_new[j]))
    for k in range(0, len(wleqw_arr_new)-2, 2):
        cw1 = wleqw_arr_new[k]
        cw2 = wleqw_arr_new[k+1]
        cw1_new = (cw1-wl)/2.5
        cw2_new = (cw2-wl)/2.5
        templist_wl.append(cw1_new)
        templist_wl.append(cw2_new)
        wl +=2.5
    reduced_eqw.append(templist_eqw)
    reduced_wl.append(templist_wl)
pdb.set_trace()
#***inputs (windows)
X = []
Y_cw = []
Y_eqw = []
Y = []
wldict_edit = dict([])
count = 0
n = 0
k = 0
for i in range(len(fdict)):
    reversed_fdict = [-1.0*j for j in fdict[i]]
    minima = find_peaks(reversed_fdict) #checking if there are minima in a single 5A window
    k += 1
    if len(minima[0]) == 2 and (reduced_eqw[n][count*2] and reduced_eqw[n][count*2+1]) != 0:
        Y_cw.append(np.array([reduced_wl[n][count*2],reduced_wl[n][count*2+1]]))
        Y_eqw.append(np.array([reduced_eqw[n][count*2],reduced_eqw[n][count*2+1]]))
        #Y.append(np.array([[wleqw_arr[n][count*2],reduced_eqw[n][count*2]],[wleqw_arr[n][count*2+1],reduced_eqw[n][count*2+1]]]))
        count += 1
        X.append(fdict[i])
    if k == 200: #k == how many windows there are in the given file wavelength range (i.e. for 5A windows in a wavelength range of 500A, k == 100)
        k = 0
        count = 0 
        n += 1 
X = np.array(X)
Y_cw = np.array(Y_cw)
Y_eqw = np.array(Y_eqw)

plt.plot(X[0])
plt.vlines(Y_cw[0]*250, ymin=0.5, ymax=1)
plt.show()


pdb.set_trace()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_cw, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
np.save('X_cw.npy', [X_train, X_test, X_val])
np.save('Y_cw.npy', [Y_train, Y_test, Y_val])
X_train, X_test, Y_train, Y_test = train_test_split(X, Y_eqw, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
np.save('X_eqw.npy', [X_train, X_test, X_val])
np.save('Y_eqw.npy', [Y_train, Y_test, Y_val])