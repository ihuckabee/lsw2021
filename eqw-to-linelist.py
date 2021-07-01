# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:34:00 2021

@author: Huckabee
"""
import pandas as pd 
import pdb
import numpy as np 
#****DICTIONARY CRAP - GETTING OG LINELIST
with open('vald-6700-6720.txt') as f:
    lines = f.readlines()
n=0
p=0
linewnum = np.empty([1,1])
element = np.empty([1,1])
newdict = dict([])
#below is reducing the EW and organizing everything into a dictionary 
for i in range(len(lines)): #cycling through every line
    if (lines[i].startswith("'") and p==0) is True: #if it starts with an apostrophe and it is the first of the set (not the element)
        linewnum = np.append(linewnum,lines[i].strip()) #append the atomic weight to an array 
        element = np.append(element,lines[i+1].strip()) #append the element to an array
        p=1 #then, change it to p=1 so that when we go to the next line, we wont take that one in. 
        n = n+1
        dict_entries = np.empty([0,0]) #if we have a new element set, make a new entry for it 
    else: #this will trigger when we hit the element name or any numbers, this will set it back to 0 so its ready to read in the next atomic weight
        p=0 
        #EVERYTHING ABOVE SEEMS LOGICALLY SOUND :-)) 
    if lines[i].startswith("'") is False: #if it is a CW line, then this is where the dictionary stuff comes in
        #we need to put the CW and EW in different arrays then change the EW to log(EW/CW)
        entry = lines[i]#add the line to the collection of CW that appear together
        #dict_entries = np.append(dict_entries, lines[i])
        dict_entries = np.append(dict_entries,element[n])
        dict_entries = np.append(dict_entries, entry)
        #newdict[linewnum[n]+':'+element[n]] = dict_entries #add the lines to the element it is under **Using element as indicator as well
        newdict[linewnum[n]] = dict_entries #using just atomic weight and ionization(?)/excitation energy as a keyword 
#for-loop where we spit out lithium (the keyword and line) and then the next keyword and line. and then lithium and then another line and so forth
keys = list(newdict.keys()) #an array with all the keys
keys_alt = keys[:]
for i in range(len(keys)):
    num = keys[i][-3:]
    keys_alt[i] = keys[i].replace(num,'  1')
items = list(newdict.values())

#****READING IN EQW
nonzero_eqw = pd.read_pickle('siliconpairtest.pic')
count = 0
pairs = []
lineval = []
nonzero_lineval = []
#for loop so it takes the label value from the eqw and map it to the items value... and then adds the items value to an array... 
#for n in range(0,len(nonzero_eqw)):
    #line_index = nonzero_eqw.index[n] 
for i in range(len(newdict)): #cycling through ALL keys as the first term
    header = list([keys_alt[i], items[i][0]])#atomic weight then element then line
    fkeyitems = newdict.get(keys[i]) #getting the items of the nth key 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): #cycling through the items in this particular key
        if fkeyitems[j].startswith("'") is False:    
            line = list([(fkeyitems[:])[j]])
            lineval.append([header[:],line[:]])#header array     
Si_header = list([keys_alt[7], items[7][0]]) #can change element pair as needed 
Si_line = list([items[7][1]])
for n in range(len(lineval)): #cycling through nonzero dataframe    
    for i in range(1,len(nonzero_eqw)):
        line_index = nonzero_eqw.index[i]    
        exc=nonzero_eqw.exc[line_index]
        loggf=nonzero_eqw.loggf[line_index]
        exc = ("{:.3f}".format(exc))[0:3]
        loggf = "{:.3f}".format(loggf)
        if exc in lineval[n][1][0][11:15] and loggf in lineval[n][1][0][17:25]: #or is a way for me to generalize the numbers between them...
            nonzero_lineval.append(lineval[n][:])
      #if that string matches the somethingth string of the lineval then WE WANT IT append it to pairs
for i in range(len(nonzero_lineval)):
    for j in range(len(nonzero_lineval)):
        pairs.append((nonzero_lineval[:])[i])
        pairs.append((nonzero_lineval[:])[j])
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
pdb.set_trace()
for i in range(2,int(len(pairs))-1,2):
    prev_line = float(Parr[i-1][1][0][2:7])
    if prev_line > 10000.0:
        start = 4800
    start += 5
    cw1 = Parr[i][1][0][2:10]
    cw2 = Parr[i+1][1][0][2:10]
    cw1_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
    cw2_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
    
    while cw1_new > cw2_new or cw2_new > start+5 or cw1_new < prev_line:
        cw1_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
        cw2_new = float("{:.3f}".format(round(start+5*(np.random.random()),3)))
        if cw1_new < cw2_new and cw2_new < start+5 and cw1_new > prev_line:
            break
    pdb.set_trace()
    Parr[i][1][0] = Parr[i][1][0].replace(cw1,str(cw1_new))
    Parr[i+1][1][0] = Parr[i+1][1][0].replace(cw2,str(cw2_new))
    
pdb.set_trace()
with open('nonzero_Si.txt', 'w') as f:
    for i in range(len(Parr)):
        f.writelines(Parr[i][0][0])
        f.write('\n')
        f.writelines(Parr[i][0][1])
        f.write('\n')
        f.writelines(Parr[i][1][0])
        f.write('\n')