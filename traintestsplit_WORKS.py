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
filenames = glob.glob('Walmart/5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_bigboi1_*.spec')
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
        if start >= 500:
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
filenames = glob.glob('Walmart/5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_bigboi1_*.eqw')
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
reduced_eqw = []
for i in range(len(wleqw_arr)):
    templist = []
    for j in range(len(wleqw_arr[i])):
        templist.append(np.log10(float(eqw_arr[i][j])/float(wleqw_arr[i][j])).round(decimals=3))
    reduced_eqw.append(templist)
#***inputs (5A windows)
X = []
Y = []
wldict_edit = dict([])
count = 0
n = 0
k = 0
pdb.set_trace()
for i in range(len(fdict)):
    minima = find_peaks(fdict[i]) #checking if there are minima in a single 5A window
    k += 1
    if len(minima[0]) == 2 and (reduced_eqw[n][count*2] and reduced_eqw[n][count*2+1]) != -inf:
        Y.append(np.array([wleqw_arr[n][count*2],wleqw_arr[n][count*2+1],reduced_eqw[n][count*2],reduced_eqw[n][count*2+1]]))
        count += 1
        X.append(fdict[i])
    if k == 100:
        k = 0
        count = 0 
        n += 1 

X = np.array(X)
#***outputs (central wl 1, central wl 2, eqw 1,  eqw 2)
# for i in range(len(wldict_edit)):
#     for j in range(0,len(wleqw_arr)-1,2):
#         if (wleqw_arr[j] and wleqw_arr[j+1]) > wldict_edit[i][0] and (wleqw_arr[j] and wleqw_arr[j+1]) < wldict_edit[i][-1]:
#             Y.append([wleqw_arr[j],wleqw_arr[j+1],reduced_eqw[j],reduced_eqw[j+1]])
Y = np.array(Y)
#plt.plot(wlspec_arr, Fn_arr)
#plt.xlim(4800,4850)
#plt.show()
pdb.set_trace()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
#pdb.set_trace()
#np.save('traintestsplits.npy',[X_train,Y_train,X_val, Y_val, X_test, Y_test])

#want an svr in there too ig 
#from sklearn import linear_model
#needs different shape (1d): linear_model.BayesianRidge(), linear_model.ARDRegression(), linear_model.LogisticRegression(), , linear_model.SGDRegressor()
#linearRegressions = [linear_model.LinearRegression(), linear_model.Ridge(), linear_model.Lasso()]
#for i in range(len(linearRegressions)):
    #model = linearRegressions[i]
    #model.fit(X_train, Y_train)
    #print(model.score(X_test,Y_test))
#model = linear_model.LinearRegression()
#model.fit(X_train, Y_train)
#print(model.score(X_test,Y_test))
#y_hist = []
#for i in range(len(Y_val)):
    #y_hist.append(Y_val[i][2:4])
#y_hist = np.array(y_hist)
#y_hist = y_hist.flatten()
#plt.hist(y_hist,bins=5)
#plt.hist(Y_test)
#plt.hist(Y_val)
#plt.show()
