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

nonzero_eqw = eqw[eqw.ew > 1]
pdb.set_trace()
starter_pair= [nonzero_eqw.iloc[11]]#, nonzero_eqw.iloc[13], nonzero_eqw.iloc[18]]
paired_eqw = pd.DataFrame(columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'])
#creating a new dataframe with paired off lines
#for n in range(len(starter_pair)):
    #pair = starter_pair[n]
    #range_start = n*700 +1
    #for i in range(range_start,range_start*(len(nonzero_eqw)*2)-1,2):
        #paired_eqw.loc[i] = pair
        #paired_eqw.loc[i+1] = nonzero_eqw.iloc[int((i+1)/(2*range_start))]
nonzero_eqw.to_pickle('siliconpairtest.pic')

pdb.set_trace()
