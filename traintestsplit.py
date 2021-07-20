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
#filenames = glob.glob('5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_Si_spec.txt')
filenames = glob.glob('5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si*.txt')
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
five_loop = 0
sets_of_five = np.array(range(4800,5300,5))
for i in range(len(wlspec_arr)): 
    for j in range(len(wlspec_arr[i])):
        if start >= 500:
           # wl_entries = []
            f_entries = []
            start = 0
            arraynum += 1
            five_loop +=1 
        #if five_loop >= 100:
           # five_loop = 0 
       # wavelength = wlspec_arr[i][j]
        #low = sets_of_five[five_loop]
        #wavelength = (wavelength - low)/5
        #wl_entries.append(wavelength)
        f_entries.append(Fn_arr[i][j])
        #wldict[arraynum] = wl_entries
        fdict[arraynum] = f_entries
        start += 1

#***reading in equivalent widths
filenames = glob.glob('5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_og_eqw.txt')
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
    wleqw_arr.append(eqw['wl'].values)
    eqw_arr.append(eqw['ew'].values)
reduced_eqw = []
reduced_wl = []
for i in range(len(wleqw_arr)):
    templist_eqw = []
    templist_wl = []
    for j in range(len(wleqw_arr[i])):
        if five_loop >= 100:
            five_loop = 0 
        wavelength = wlspec_arr[i][j]
        low = sets_of_five[five_loop]
        wavelength = (wavelength - low)/5
        templist_wl.append(wavelength)
        templist_eqw.append(((eqw_arr[i][j])/(wavelength)).round(decimals=3))
    reduced_wl.append(templist_wl)    
    reduced_eqw.append(templist_eqw)
#***inputs (5A windows)
X = []
Y_cw1 = []
Y_cw2 = []
Y_eqw1 = []
Y_eqw2 = []
#wldict_edit = dict([])
count = 0
n = 0
k = 0
for i in range(len(fdict)):
    minima = find_peaks(fdict[i]) 
    k += 1
    if len(minima[0]) == 2 and (reduced_eqw[n][count*2] != -inf and reduced_eqw[n][count*2+1] != -inf):
    #if len(minima[0]) == 2 and (eqw_arr[n][count*2] != 0 and eqw_arr[n][count*2+1] != 0):
        Y_cw1.append(reduced_wl[n][count*2])
        Y_cw2.append(reduced_wl[n][count*2+1])
        Y_eqw1.append(reduced_eqw[n][count*2])
        Y_eqw2.append(reduced_eqw[n][count*2+1])
        #Y.append(np.array([reduced_wl[n][count*2],reduced_wl[n][count*2+1],reduced_eqw[n][count*2],reduced_eqw[n][count*2+1]]))
        count += 1
        X.append(fdict[i])
    if k == 100:
        k = 0
        count = 0 
        n += 1 

X = np.array(X)
Y = np.array(Y_cw1, Y_eqw1,Y_cw2, Y_eqw2) #wack
pdb.set_trace()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
pdb.set_trace()
np.save('bigboi2_traintestsplits.npy',[X_train,Y_train,X_val, Y_val, X_test, Y_test])
np.save('bigboi2_nonsplitdata_X.npy', X)
np.save('bigboi2_nonsplitdata_Y.npy', Y)
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
