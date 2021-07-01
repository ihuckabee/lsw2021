import pandas as pd 
import pdb
import numpy as np 
with open('vald-6700-6720.txt') as f:
    lines = f.readlines()
#***reducing the EW and organizing everything into a dictionary*** 
n=0
p=0
linewnum = np.empty([1,1])
element = np.empty([1,1])
newdict = dict([])
for i in range(len(lines)): 
    if (lines[i].startswith("'") and p==0) is True: 
        linewnum = np.append(linewnum,lines[i].strip()) 
        element = np.append(element,lines[i+1].strip()) 
        p=1  
        n = n+1
        dict_entries = np.empty([0,0]) 
    else: 
        p=0 
    if lines[i].startswith("'") is False: 
        entry = lines[i]
        dict_entries = np.append(dict_entries,element[n])
        dict_entries = np.append(dict_entries, entry)
        newdict[linewnum[n]] = dict_entries 
keys = list(newdict.keys())
keys_alt = keys[:]
for i in range(len(keys)):
    num = keys[i][-3:]
    keys_alt[i] = keys[i].replace(num,'  1')
    items = list(newdict.values())
        
#***reading in .eqw file***
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_6700-6720_xit1.0_og_eqw.txt')
eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
eqw = eqw.drop(eqw.columns[[6,7,8,9,10,11,12]], axis =1) 
eqw.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'] 
nonzero_eqw = eqw[eqw.ew > 1]

nonzero_lineval = []
lineval = []
for i in range(len(newdict)): 
    header = list([keys_alt[i], items[i][0]])
    fkeyitems = newdict.get(keys[i]) 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): 
        if fkeyitems[j].startswith("'") is False:    
            line = list([fkeyitems[j]])
            lineval.append([header[:],line[:]])   
 
for n in range(len(lineval)): #cycling through nonzero dataframe    
    for i in range(1,len(nonzero_eqw)):
        line_index = nonzero_eqw.index[i]    
        exc=nonzero_eqw.exc[line_index]
        loggf=nonzero_eqw.loggf[line_index]
        exc = ("{:.3f}".format(exc))[0:3]
        loggf = "{:.3f}".format(loggf)
        if exc in lineval[n][1][0][11:15] and loggf in lineval[n][1][0][17:25]: 
            nonzero_lineval.append(lineval[n][:])
pairs = []
for i in range(len(nonzero_lineval)):
    for j in range(len(nonzero_lineval)):
        pairs.append(nonzero_lineval[i][:])
        pairs.append(nonzero_lineval[j][:])    
Parr = np.array(pairs[:])