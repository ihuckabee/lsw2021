#%%
import pandas as pd  
eqw = pd.read_fwf('old_linelists/5777g4.44z+0.00a+0.00t01-ref107857_4800-5300_xit1.0_ew.txt')
#eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
eqw = eqw.drop(eqw.columns[[6,7,8,9,10,11,12]], axis =1) 
eqw.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
