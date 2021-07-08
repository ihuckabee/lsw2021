import pandas as pd 
import pdb
import numpy as np 

with open('lines/grid_lines/vald-4800-5300-for-grid.list') as f:
    lines = f.readlines()
n=0
p=0
linewnum = []
element = []
newdict = dict([])
#below is reducing the EW and organizing everything into a dictionary 
for i in range(len(lines)): #cycling through every line
    if (lines[i].startswith("'") and p==0): #if it starts with an apostrophe and it is the first of the set (not the element)
        linewnum.append(lines[i].strip()) #append the atomic weight to an array 
        element.append(lines[i+1].strip()) #append the element to an array
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
        dict_entries.append(element[n-1])
        dict_entries.append(entry)
        #newdict[linewnum[n]+':'+element[n]] = dict_entries #add the lines to the element it is under **Using element as indicator as well
        newdict[(linewnum[n-1],element[n-1])] = dict_entries #using just atomic weight and ionization(?)/excitation energy as a keyword 
        # print(i)
#for-loop where we spit out lithium (the keyword and line) and then the next keyword and line. and then lithium and then another line and so forth
keys = list(newdict.keys()) #an array with all the keys
keys_copy = keys[:]
#for i in range(len(keys)):
    #num = keys[i][0][-3:]
    #keys_copy[i][0] = keys[i][0].replace(num,'  1') 
items = list(newdict.values())
keyitemlines = []
for i in range(len(items)): #here is where we pair everything together 
    for j in range(len(items[i])):
        key_idx1 = (keys[i], j)
        keyitemlines.append(key_idx1)
with open('test_2.txt', 'w') as f:
    for i in range(len(keyitemlines)):
        for j in range(len(keyitemlines)):
            kline1, kline2 = keyitemlines[i], keyitemlines[j]
            line1 = newdict[kline1[0]][1]
            line2 = newdict[kline2[0]][1] #success reading in lines
            if 'prev_line' in globals():
                prev_line = float(line2[2:10])
            else:
                prev_line = 4795.0
                start = 4795.0
            if prev_line > 5295.0:
                prev_line = 4800.0
                start = 4795.0
            start += 5
            cw1 = line1[2:10]
            cw2 = line2[2:10]
            cw1_new = round(start+5*(np.random.random()),3)
            cw2_new = round(start+5*(np.random.random()),3)
    
            while cw1_new > cw2_new or cw2_new > start+5 or cw1_new < prev_line:
                cw1_new = round(start+5*(np.random.random()),3)
                cw2_new = round(start+5*(np.random.random()),3)
                if cw1_new < cw2_new and cw2_new < start+5 and cw1_new > prev_line:
                    break
            line1 = line1.replace(cw1,str(cw1_new))
            line2 = line2.replace(cw2,str(cw2_new)) 
            f.writelines(kline1[0][0])
            f.write('\n')
            f.writelines(kline1[0][1])
            f.write('\n')
            f.writelines(line1)
            f.write('\n')
            f.writelines(kline2[0][0])
            f.write('\n')
            f.writelines(kline2[0][1])
            f.write('\n')
            f.writelines(line2)
            f.write('\n')
