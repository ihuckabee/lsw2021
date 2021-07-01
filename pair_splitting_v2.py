# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 17:09:49 2021

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
        cw = entry[2:10]
        ew = entry[11:17]
        #pdb.set_trace()
        reduced_ew = (np.log10(float(ew)/float(cw))).round(decimals=3)
        if reduced_ew == float('-inf'):
            continue 
        dict_entries = np.append(dict_entries, entry.replace(ew, str(reduced_ew)))
        #pdb.set_trace()
        newdict[linewnum[n]+element[n]] = dict_entries #add the lines to the element it is under
        
#creating the pairs - gives HELLA pairs, 2 many
keys = list(newdict.keys()) #an array with all the keys
items = list(newdict.values())
pairs = []
for i in range(len(newdict)): #cycling through ALL keys as the first term
    fkeyitems = newdict.get(keys[i]) #getting the items of the nth key 
    fkeyitems = np.delete(fkeyitems,0)
    for j in range(len(fkeyitems)): #cycling through the items in this particular key
        ioi = fkeyitems[j] #item of interest is the jth item in this particular key 
        #now cycle through EVERYTHING 
        for k in range(len(items)): 
            if ioi!=any(items[k]): #as long as the item of interest does not equal the item we're pairing it with
                if items[k][0].isdigit(): #only if we got sumthin funky like this 
                    items[k] = np.delete(items[k],0) 
                #print(k)
                for m in range(len(items[k])-1):
                    pairs.append(ioi)
                    pairs.append(items[k][m+1])
                    #pdb.set_trace()

pairs = np.array(pairs)     

#setting wavelengths
#pdb.set_trace()

cw1 = pairs[0][2:10]
cw2 = pairs[1][2:10]
#pdb.set_trace()
pairs[0] = pairs[0].replace(cw1,'5000.000')
cw2_new = round(5000+2*np.random.random(),3)
pairs[1] = pairs[1].replace(cw2,str(cw2_new))
start = 0
end = 3249
iterator = 0
for i in range(2,3250,2):
    cw1 = pairs[i][2:10]
    cw2 = pairs[i+1][2:10]
    cw1_new = 2+cw2_new
    pairs[i] = pairs[i].replace(cw1,str(cw1_new))
    cw2_new = round(cw1_new+2*np.random.random(),3)
    pairs[i+1] = pairs[i+1].replace(cw2, str(cw2_new))
    #pdb.set_trace()
    #if i >= 3250*(iterator+1):
        #pairs_file = open("pairs_file"+str(iterator)+".txt", "w")    
        #np.savetxt(pairs_file,pairs[start:end], fmt="%10s")
        #pairs_file.close()
        #iterator=iterator+1
        #start = 3250*iterator
        #end = start + 3250
        #c2_new = 4998
pairs_file = open("_pairs_file.txt", "w")    
np.savetxt(pairs_file,pairs[start:end], fmt="%10s")
pairs_file.close()    
#pdb.set_trace()