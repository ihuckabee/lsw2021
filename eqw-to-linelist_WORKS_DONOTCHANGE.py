# -*- coding: utf-8 -*-
"""
Created on Tue Jun 22 21:34:00 2021

@author: Huckabee
"""
import pandas as pd 
import pdb
import numpy as np 
import copy 
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
    if (lines[i].startswith("'") and p==0): #if it starts with an apostrophe and it is the first of the set (not the element)
        linewnum = np.append(linewnum,lines[i].strip()) #append the atomic weight to an array 
        element = np.append(element,lines[i+1].strip()) #append the element to an array
        p=1 #then, change it to p=1 so that when we go to the next line, we wont take that one in. 
        n = n+1
        dict_entries = []#if we have a new element set, make a new entry for it 
    else: #this will trigger when we hit the element name or any numbers, this will set it back to 0 so its ready to read in the next atomic weight
        p=0 
        #EVERYTHING ABOVE SEEMS LOGICALLY SOUND :-)) 
    if not lines[i].startswith("'"): #if it is a CW line, then this is where the dictionary stuff comes in
        #we need to put the CW and EW in different arrays then change the EW to log(EW/CW)
        entry = lines[i]#add the line to the collection of CW that appear together
        #dict_entries = np.append(dict_entries, lines[i])
        dict_entries.append(element[n])
        dict_entries.append(entry)
        #newdict[linewnum[n]+':'+element[n]] = dict_entries #add the lines to the element it is under **Using element as indicator as well
        newdict[linewnum[n]] = dict_entries #using just atomic weight and ionization(?)/excitation energy as a keyword 
        # print(i)
#for-loop where we spit out lithium (the keyword and line) and then the next keyword and line. and then lithium and then another line and so forth
keys = list(newdict.keys()) #an array with all the keys
keys_alt = keys[:]
for i in range(len(keys)):
    num = keys[i][-3:]
    keys_alt[i] = keys[i].replace(num,'  1')
items = list(newdict.values())
#****READING IN EQW
eqw = pd.read_fwf('5777g4.44z+0.00a+0.00t01-ref107857_6700-6720_xit1.0_og_eqw.txt')
eqw = eqw.drop(eqw.columns[[13,14,15]], axis =1) #for data with comments
eqw = eqw.drop(eqw.columns[[6,7,8,9,10,11,12]], axis =1) 
eqw.columns = ['element', 'ion', 'wl', 'exc', 'loggf', 'ew'] 

nonzero_eqw = eqw[eqw.ew > 1] #determines how long this program will run lol

#print(nonzero_eqw)
#print(nonzero_eqw[0])
pairs = []
lineval = []
#for loop so it takes the label value from the eqw and map it to the items value... and then adds the items value to an array... 
#for n in range(0,len(nonzero_eqw)):
    #line_index = nonzero_eqw.index[n] 
for i in range(len(newdict)): #cycling through ALL keys as the first term
    header = list([keys_alt[i], items[i][0]])#atomic weight then element then line
    fkeyitems = newdict.get(keys[i]) #getting the items of the nth key 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): #cycling through the items in this particular key
        if fkeyitems[j].startswith("'") is False:    
            line = list([fkeyitems[j]])
            lineval.append([header[:],line[:]])#header array     


#pdb.set_trace()
line_index=[]
for i in range(0,len(nonzero_eqw)): #getting all the nonzero indices 
    line_index.append(nonzero_eqw.index[i])
for i in range(len(line_index)):
    lineval1 = lineval[line_index[i]]
    for j in range(len(line_index)):
        lineval2 = copy.deepcopy(lineval[line_index[j]])
        pairs.append(copy.deepcopy(lineval1))
        pairs.append(lineval2[:])
pdb.set_trace()
Parr = np.array(pairs)
cw1 = Parr[0][1][0][2:10]
cw2 = Parr[1][1][0][2:10]
start = 3000
cw1_new = round(start+5*(np.random.random()),3)
cw2_new = round(start+5*(np.random.random()),3)
while cw1_new > cw2_new or cw2_new > start+5:
    cw1_new = round(start+5*(np.random.random()),3)
    cw2_new = round(start+5*(np.random.random()),3)
    if cw1_new < cw2_new and cw2_new < start+5:
        break
Parr[0][1][0] = Parr[0][1][0].replace(cw1,str(cw1_new))
Parr[1][1][0] = Parr[1][1][0].replace(cw2,str(cw2_new))
for i in range(2,int(len(pairs))-1,2):
    prev_line = float(Parr[i-1][1][0][2:7])
    if prev_line > 9995.0:
        prev_line = 3000.0
        start = 2995.0
    start += 5
    cw1 = Parr[i][1][0][2:10]
    cw2 = Parr[i+1][1][0][2:10]
    cw1_new = round(start+5*(np.random.random()),3)
    cw2_new = round(start+5*(np.random.random()),3)
    
    while cw1_new > cw2_new or cw2_new > start+5 or cw1_new < prev_line:
        cw1_new = round(start+5*(np.random.random()),3)
        cw2_new = round(start+5*(np.random.random()),3)
        if cw1_new < cw2_new and cw2_new < start+5 and cw1_new > prev_line:
            break
    Parr[i][1][0] = Parr[i][1][0].replace(cw1,str(cw1_new))
    Parr[i+1][1][0] = Parr[i+1][1][0].replace(cw2,str(cw2_new))
    print(i)
with open('6700-6720_pairedlinelist.txt', 'w') as f:
    for i in range(len(Parr)):
        f.writelines(Parr[i][0][0])
        f.write('\n')
        f.writelines(Parr[i][0][1])
        f.write('\n')
        f.writelines(Parr[i][1][0])
        f.write('\n')