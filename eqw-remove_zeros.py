# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 22:58:44 2021

@author: Huckabee
"""

import pandas as pd
import matplotlib.pyplot as plt
import pdb
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import peak_widths
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_6700-6720_xit1.0_og_eqw.txt')
ignoredcol = ['0.000.1','+-','1.000','0.00', '1.050', '1.050.1', '1.050.2'] #4800-5300, 5800-6300, 6300-6800
#ignoredcol = ['0.000','+-','1.000','0.00', '1.380', '1.380.1', '1.380.2'] #5300-5800
#ignoredcol = ['0.000','+-','1.000','0.00', '4.560', '4.560.1', '4.560.2'] #F starter
#ignoredcol = ['0.000','+-','1.000','0.00', '8.390', '8.390.1', '8.390.2'] #C starter
eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
for i in ignoredcol:
    del eqw[i]
eqw.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
#WHY IS THE EW COLUMN ZERO???? 
#now i want to do the same thing where i pair things off and change their wavelengths. but first del all the zeros from the ew
nonzero_eqw = eqw[(eqw[['ew']] != 0).all(axis=1)]
#so first need to add shit to a dictionary ig... actually. No. i dont
#i can literally just go down the line and pair shit off.  i can do lithium or carbon or silicon
#and just say paired element other paired other paired other 
#i just need to figure out how to do that in a dataframe rather than a dict or numpy array
#and once i pair them off, alter the wavelength.... ok.... 
#so take out x row... 
#ah.... we're going to be making a new dataframe... i see... 
#so take out x row and then have a for loop going through each row 
#then place each new row into that dataframe... 
starter_pair= [nonzero_eqw.iloc[11]]#, nonzero_eqw.iloc[13], nonzero_eqw.iloc[18]]
#starter_pair = nonzero_eqw.iloc[1] #lithium 
paired_eqw = pd.DataFrame(columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'])
#creating a new dataframe with paired off lines
for n in range(len(starter_pair)):
    pair = starter_pair[n]
    range_start = n*700 +1
    for i in range(range_start,range_start*(len(nonzero_eqw)*2)-1,2):
        paired_eqw.loc[i] = pair
        paired_eqw.loc[i+1] = nonzero_eqw.iloc[int((i+1)/(2*range_start))]
#making wavelengths sequential 
#extract first two initial wavelengths and then for loop the rest 
start = 4800.000
paired_eqw['wl'][1] = round(start+1.25*(np.random.random()),3)
paired_eqw['wl'][2] = round(start+(5.0*(np.random.random())),3)

for i in range(3,int(len(paired_eqw)),2):
    if float(paired_eqw['wl'][i-1]) > 10000.0:
        start = 4800.000
    start = start+5
    paired_eqw['wl'][i] = round(start+1.25*(np.random.random()),3)
    paired_eqw['wl'][i+1] = round(start+5.0*(np.random.random()),3)
paired_eqw.to_pickle('siliconpairtest.pic')

pdb.set_trace()
