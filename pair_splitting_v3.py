# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 08:08:26 2021

@author: Huckabee
"""

import pdb
import numpy as np
#to split the vald linelist into pairs 
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
pairs = []
pdb.set_trace()
#array of lithium keyword and then the line
c_header = list([keys_alt[3], items[3][0]]) #can change element pair as needed 
c_line = list([items[3][1]])
for i in range(len(newdict)): #cycling through ALL keys as the first term
    header = list([keys_alt[i], items[i][0]])#atomic weight then element then line
    fkeyitems = newdict.get(keys[i]) #getting the items of the nth key 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): #cycling through the items in this particular key
        if fkeyitems[j].startswith("'") is False:    
            ioi = fkeyitems[j] #item of interest is the jth item in this particular key
            line = list([ioi])
            #create element array of keyword and line
            pairs.append([c_header[:], c_line[:]])
            pairs.append([header[:],line[:]])#header array
            #pairs.append(element)#element array
Parr = np.array(pairs)
cw1 = Parr[0][1][0][2:10]
cw2 = Parr[1][1][0][2:10]
start = 4800
cw1_new = round(start+1.25*(np.random.random()),3)
cw2_new = round(start+(5.0*(np.random.random())),3)
Parr[0][1][0] = Parr[0][1][0].replace(cw1,str(cw1_new))
Parr[1][1][0] = Parr[1][1][0].replace(cw2,str(cw2_new))
for i in range(2,int(len(pairs))-1,2):
    if float(Parr[i-1][1][0][2:9]) > 10000.0:
        start = 4800
    start = start+5
    cw1 = Parr[i][1][0][2:10]
    cw2 = Parr[i+1][1][0][2:10]
    cw1_new = round(start+1.25*(np.random.random()),3)
    cw2_new = round(start+5.0*(np.random.random()),3)
    Parr[i][1][0] = Parr[i][1][0].replace(cw1,str(cw1_new))
    Parr[i+1][1][0] = Parr[i+1][1][0].replace(cw2,str(cw2_new))

with open('uniform-ish_spacing_C.txt', 'w') as f:
    for i in range(len(Parr)):
        f.writelines(Parr[i][0][0])
        f.write('\n')
        f.writelines(Parr[i][0][1])
        f.write('\n')
        f.writelines(Parr[i][1][0])
        f.write('\n')