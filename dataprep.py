# -*- coding: utf-8 -*-
"""
Created on Fri Jun 25 15:23:25 2021

@author: Huckabee
"""

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

pairs = []
lineval = []
for i in range(len(newdict)): 
    header = list([keys_alt[i], items[i][0]])
    fkeyitems = newdict.get(keys[i]) 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): 
        if fkeyitems[j].startswith("'") is False:    
            line = list([fkeyitems[j]])
            lineval.append([header[:],line[:]])   
for j in range(len(keys_alt)):
    elem_header = list([keys_alt[j], items[j][0]]) #can change element pair as needed 
    elem_line = list([items[j][1]])
    for n in range(len(lineval)): #cycling through nonzero dataframe    
        for i in range(1,len(nonzero_eqw)):
            line_index = nonzero_eqw.index[i]    
            exc=nonzero_eqw.exc[line_index]
            loggf=nonzero_eqw.loggf[line_index]
            exc = ("{:.3f}".format(exc))[0:3]
            loggf = "{:.3f}".format(loggf)
            if exc in lineval[n][1][0][11:15] and loggf in lineval[n][1][0][17:25]: #or is a way for me to generalize the numbers between them...
                pairs.append([elem_header[:], elem_line[:]])    
                pairs.append(lineval[n])
    #changing the wavelengths so they are sequential and randomly-ish placed in a 5A window              
Parr = np.array(pairs)
cw1 = Parr[0][1][0][2:10]
cw2 = Parr[1][1][0][2:10]
start = 4800
cw1_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
cw2_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
while cw1_new > cw2_new or cw2_new > start+5:
    cw1_new = round(start+5*(np.random.random()),3)
    cw2_new = round(start+5*(np.random.random()),3)
    if cw1_new < cw2_new and cw2_new < start+5:
        break
Parr[0][1][0] = Parr[0][1][0].replace(cw1,str(cw1_new))
Parr[1][1][0] = Parr[1][1][0].replace(cw2,str(cw2_new))
n=0
pdb.set_trace()
for i in range(2,int(len(Parr))-2,2):
     prev_line = float(Parr[i-1][1][0][2:7])
     if prev_line > 5295.0:
         start = 4800
         n +=1
         with open(str(n)+'linelist'+'.txt', 'w') as f:
             for k in range(len(Parr)):
                 f.writelines(Parr[k][0][0])
                 f.write('\n')
                 f.writelines(Parr[k][0][1])
                 f.write('\n')
                 f.writelines(Parr[k][1][0])
                 f.write('\n')
         pdb.set_trace()
     start += 5
     cw1 = Parr[i][1][0][2:10]
     cw2 = Parr[i+1][1][0][2:10]
     #cw1_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
     #cw2_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
    
     while cw2_new > start+5 or cw1_new > start+5 or (cw1_new or cw2_new) < prev_line: #getting stuck here
        cw1_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
        cw2_new = cw1_new+float("{:.3f}".format(round(5*(np.random.random()),3)))
        if cw2_new < start+5 and cw1_new > prev_line:
            break
     Parr[i][1][0] = Parr[i][1][0].replace(cw1,str(cw1_new))
     Parr[i+1][1][0] = Parr[i+1][1][0].replace(cw2,str(cw2_new))
if n == 0:
    with open(str(n)+'linelist'+'.txt', 'w') as f:
        for i in range(len(Parr)):
            f.writelines(Parr[i][0][0])
            f.write('\n')
            f.writelines(Parr[i][0][1])
            f.write('\n')
            f.writelines(Parr[i][1][0])
            f.write('\n')
            