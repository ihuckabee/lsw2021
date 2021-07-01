# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#import tensorflow
#import keras
#import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import pdb
#from scipy.signal import find_peaks
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_5300-5800_xit1.0_ew.txt')
#ignoredcol = ['0.000','+-','1.000','0.00', '1.050', '1.050.1', '1.050.2'] #4800-5300, 5800-6300, 6300-6800
ignoredcol = ['0.000','+-','1.000','0.00', '1.380', '1.380.1', '1.380.2'] #5300-5800
eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
for i in ignoredcol:
    del eqw[i]
eqw.columns = ['elements', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
eqw_lim = eqw[(eqw[['ew']] != 0).all(axis=1)]
spec= pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_spec.txt')
spec.columns = ['wl','Fn','F'] 
Fn_arr=spec['Fn'].to_numpy()
wlspec_arr=spec['wl'].to_numpy()
eqw_ew_lim=eqw_lim['ew'].to_numpy()
eqw=eqw['ew'].to_numpy()
#plt.plot(wlspec_arr,Fn_arr)
plt.hist(eqw_ew_lim, bins=25)
plt.ylim(0,200)
plt.xlim(0,100)
pdb.set_trace()
plt.title('5300-5800 w/o zeros')
wleqw_arr=eqw_lim['wl'].to_numpy()
plt.vlines(wleqw_arr, 0, 1, color = 'r',alpha = 0.5)
#plt.xlim(4900,4905)
# we are trying to find the "useable" features, and then create sets from those. 
#so basically, what lines matter in describing the lines? grab those and make a new dataframe of them 
#plt.vlines(wleqw_arr, 0, 1, color = 'r',alpha = 0.5)