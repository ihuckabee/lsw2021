# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 12:06:29 2021

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
elementlines = np.empty([1,1])
runningtotal = np.empty([1,1])
for i in range(len(lines)):
    if (lines[i].startswith("'") and p==0) is True:
        linewnum = np.append(linewnum,lines[n])
        element = np.append(element,lines[n+1])
        p=1
    elif (lines[i].startswith("'") and p==1) is True: 
        p=0
    elif lines[i].startswith("'") is False:  
        runningtotal=np.append(runningtotal,lines[i])
        temp = np.array([lines[i]])
        #
        #for j in range(len(lines)):
            #if (lines[i].startswith("'") and p==0) is True:
                #temp = np.append(temp, lines[i-1])
    #make an array and store the first line into it 
    #go until you see another ' that does not match the previous one, pass by the headers, and store the first line of that into the arra
    n = n+1
    
for i in range(len(lines)):
    if (lines[i]==any(element) and lines[i]==any(linewnum)) == False: 
        elementlines = np.append(elementlines,lines[i])
        
        
pdb.set_trace()  
    