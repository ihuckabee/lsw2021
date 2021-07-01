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
#***reading in spectrum
frames = []
specFiles = ['5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si1_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si2_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si3_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si4_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si5_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si6_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si7_spec.txt', '5777g4.44z+0.00a+0.00t01-ref107857_4805-5305_xit1.0_Si8_spec.txt']
for i in range(len(specFiles)):
    spec= pd.read_fwf(specFiles[i])
    frames.append(spec)
spec= pd.concat(frames)
spec.columns = ['wl','Fn','F'] 
Fn_arr=spec['Fn'].to_numpy()
wlspec_arr=spec['wl'].to_numpy()
#pdb.set_trace()
#***setting up 5A windows
wldict = dict([])
fdict = dict([])
wl_entries = np.empty([0,0])
f_entries = np.empty([0,0])
start = 0
arraynum = 0
for i in range(len(wlspec_arr)): 
    if start >= 500:
        wl_entries = np.empty([0,0])
        f_entries = np.empty([0,0])
        start = 0
        arraynum += 1
    wl_entries = np.append(wl_entries, wlspec_arr[i])
    f_entries = np.append(f_entries, Fn_arr[i])
    wldict[arraynum] = wl_entries
    fdict[arraynum] = f_entries
    start += 1
#pdb.set_trace()
#***reading in equivalent widths 
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_works_eqw.txt')
eqw = eqw.drop(eqw.columns[[6,7,8,9,10,11,12]], axis =1)    
eqw.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'] 

wleqw_arr=eqw['wl'].to_numpy()
eqw_arr=eqw['ew'].to_numpy()
reduced_eqw = []
for i in range(len(wleqw_arr)):
    reduced_eqw.append(np.log10(float(eqw_arr[i])/float(wleqw_arr[i])).round(decimals=3))
#***inputs (5A windows)
X = []
Y = []
wldict_edit = dict([])
count = -1
for i in range(len(fdict)):
    minima = find_peaks(fdict[i]*-1)
    min_pos = fdict[i][minima[0]]
    if len(minima[0]) == 2 and (reduced_eqw[count*2] and reduced_eqw[count*2+1]) != -inf:
        count +=1
        wldict_edit[count] = wldict[i][:]
        X.append(np.array(fdict[i]))
        Y.append([wleqw_arr[count*2],wleqw_arr[count*2+1],reduced_eqw[count*2],reduced_eqw[count*2+1]])
    

X = np.array(X)

#***outputs (central wl 1, central wl 2, eqw 1,  eqw 2)
# for i in range(len(wldict_edit)):
#     for j in range(0,len(wleqw_arr)-1,2):
#         if (wleqw_arr[j] and wleqw_arr[j+1]) > wldict_edit[i][0] and (wleqw_arr[j] and wleqw_arr[j+1]) < wldict_edit[i][-1]:
#             Y.append([wleqw_arr[j],wleqw_arr[j+1],reduced_eqw[j],reduced_eqw[j+1]])
Y = np.array(Y)
pdb.set_trace()
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train, X_val, Y_train, Y_val = train_test_split(X_train, Y_train, test_size=0.25, random_state=42)
pdb.set_trace()
np.save('traintestsplits.npy',[X_train,Y_train,X_val, Y_val, X_test, Y_test])

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
