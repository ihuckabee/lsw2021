#TICTOC TIMING
import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)
#"""
import pandas as pd
import matplotlib.pyplot as plt
import pdb
import numpy as np
from scipy.signal import find_peaks
from scipy.signal import peak_widths
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_4800-5000_xit1.0_Si_eqw.txt')
#ignoredcol = ['0.000.1','+-','1.000','0.00', '1.050', '1.050.1', '1.050.2'] #4800-5300, 5800-6300, 6300-6800
#ignoredcol = ['0.000.1','+-','1.000','0.00', '1.380', '1.380.1', '1.380.2'] #5300-5800
ignoredcol = ['0.000','+-','1.000','0.00', '7.510', '7.510.1', '7.510.2'] #Si starter
#ignoredcol = ['0.000.1','+-','1.000','0.00', '8.390', '8.390.1', '8.390.2'] #C starter
#eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
for i in ignoredcol:
    del eqw[i]
eqw.columns = ['elements', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
eqw_lim = eqw[(eqw[['ew']] != 0).all(axis=1)]
spec= pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_4800-5000_xit1.0_Si_spec.txt')
spec.columns = ['wl','Fn','F'] 
Fn_arr=spec['Fn'].to_numpy()
wlspec_arr=spec['wl'].to_numpy()
wleqw_arr=eqw_lim['wl'].to_numpy()
eqw_ew_lim=eqw_lim['ew'].to_numpy()
eqw=eqw['ew'].to_numpy()
#eqw peaks
maxima = find_peaks(eqw_ew_lim, prominence = 2, wlen = 50, threshold = 1)
max_pos = wleqw_arr[maxima[0]]
max_mag = eqw_ew_lim[maxima[0]]
#spectra peaks
Fn_arr_mr = Fn_arr* -1
minima = find_peaks(Fn_arr_mr, prominence = 0.001, wlen = 50)
min_pos = wlspec_arr[minima[0]]
min_mag = Fn_arr[minima[0]]
minima_width = peak_widths(Fn_arr_mr, minima[0], rel_height = 1.0)
min_wid = 0.001*minima_width[0]
eqw_pos = np.empty([1,1])
tic()
for i in range(len(min_pos)):
    eqw_temp = np.asarray(np.where(np.logical_and(wleqw_arr < min_pos[i]+.1,wleqw_arr > min_pos[i]-.1)))
    eqw_pos = np.append(eqw_pos, eqw_temp)
    #pdb.set_trace()
    #was 0.01
toc()


eqw_pos_merged = eqw_pos.flatten()
eqw_pos_merged = eqw_pos_merged.astype(int)
plt.plot(wlspec_arr,Fn_arr)
plt.vlines(max_pos, 0, 1, color = 'r',alpha = 0.5)
plt.scatter(min_pos, min_mag, color = 'k', marker = '*')
plt.xlim(4800,4865)
plt.ylim(0,1.05)
final_posarr = wleqw_arr[eqw_pos_merged]
final_magarr = eqw_ew_lim[eqw_pos_merged]
#pdb.set_trace()
#for i in range(len(eqw_pos_merged)):
plt.vlines(final_posarr, 0, 1, color='green', alpha = 0.5) 
#pdb.set_trace()
#plt.vlines(4861.35,0,1)
#*** reducing the eqw ***
#for i in range(len(max_mag[i]))

#getting processed data
with open('processed-4800-5300-F.txt', 'w') as f:
    for i in range(len(final_posarr)):
        f.write(str(final_posarr[i])+'  '+str(final_magarr[i]))
        f.write('\n')