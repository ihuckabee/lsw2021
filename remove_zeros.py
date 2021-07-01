# -*- coding: utf-8 -*-
"""
Created on Mon Jun 21 14:10:23 2021

@author: Huckabee
"""

#getting rid of zeros 
#i wont be able to remove the feature from the spectrum... 
#i mean, i can just check in the window if there are two peaks and if there are then use that as data
import pandas as pd
from scipy.signal import find_peaks
from scipy.signal import peak_widths
import numpy as np
import matplotlib.pyplot as plt
import pdb
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_6300-6675_xit1.0_C_eqw.txt')
#ignoredcol = ['0.000','+-','1.000','0.00', '1.050', '1.050.1', '1.050.2'] #L starter
#ignoredcol = ['0.000','+-','1.000','0.00', '1.380', '1.380.1', '1.380.2'] # L 5300-5800
#ignoredcol = ['0.000','+-','1.000','0.00', '4.560', '4.560.1', '4.560.2'] #F starter
ignoredcol = ['0.000','+-','1.000','0.00', '8.390', '8.390.1', '8.390.2'] #C starter
eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
for i in ignoredcol:
    del eqw[i]
eqw.columns = ['elements', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
eqw_arr=eqw['ew'].to_numpy()
wleqw_arr=eqw['wl'].to_numpy()


spec= pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_6300-6675_xit1.0_C_spec.txt')
spec.columns = ['wl','Fn','F'] 
Fn_arr=spec['Fn'].to_numpy()
wlspec_arr=spec['wl'].to_numpy()
#spectrum peaks 
Fn_arr_mr = Fn_arr* -1
minima = find_peaks(Fn_arr_mr, prominence = 0.001, wlen = 50)
min_pos = wlspec_arr[minima[0]]
min_mag = Fn_arr[minima[0]]
minima_width = peak_widths(Fn_arr_mr, minima[0], rel_height = 1.0)
min_wid = 0.001*minima_width[0]

eqw_pos = np.empty([1,1])
for i in range(len(min_pos)):
    eqw_temp = np.asarray(np.where(np.logical_and(wleqw_arr < min_pos[i]+.1,wleqw_arr > min_pos[i]-.1)))
    eqw_pos = np.append(eqw_pos, eqw_temp)
eqw_pos_merged = eqw_pos.flatten()
eqw_pos_merged = eqw_pos_merged.astype(int)
posarr = wleqw_arr[eqw_pos_merged]
magarr = eqw_arr[eqw_pos_merged]
final_posarr = np.empty([0,0])
final_magarr = np.empty([0,0])
#go through the wl_spec array and see how many peaks there are. if there are two peaks, then take the range in
for i in range(0,len(wlspec_arr)-500,500):
    fiveA_range = np.array([wlspec_arr[i],wlspec_arr[i+500]])
    peaks = (np.where(np.logical_and(posarr < fiveA_range[1],posarr > fiveA_range[0])))

    if len(peaks[0]) == 2:
        if posarr[peaks[0][0]] == posarr[peaks[0][1]]:
                continue 
        #i need an array with a cw for each ew.... thats it
        final_posarr = np.append(final_posarr, posarr[peaks[0][0]])
        final_posarr = np.append(final_posarr, posarr[peaks[0][1]])
        final_magarr = np.append(final_magarr, magarr[peaks[0][0]])
        final_magarr = np.append(final_magarr, magarr[peaks[0][1]])

plt.plot(wlspec_arr,Fn_arr)
plt.scatter(min_pos, min_mag, color = 'k', marker = '*')
plt.xlim(6300,6400)
plt.vlines(final_posarr, 0, 1, color='green', alpha = 0.5) 
with open('sample1.npy', 'wb') as f:
    np.save(f, final_posarr)
    np.save(f, final_magarr)
#FINAL_POSARR AND FINAL_MAGARR ARE WHAT MATTER FOR THE ML ALG 
    