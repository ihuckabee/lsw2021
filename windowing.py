# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 09:44:31 2021

@author: Huckabee
"""
import pdb
import tensorflow as tf 
import numpy as np
with open("processed-4800-5300-og.txt") as f:
    lines = f.readlines()
dataset = tf.data.Dataset.from_tensor_slices(lines)
wl = np.empty([1,1])
eqw = np.empty([1,1])
for i in range(len(lines)):
    temp = lines[i].split()
    wl = np.append(wl, temp[0])
    eqw = np.append(eqw, temp[1])
wl = np.delete(wl,0)
wl = wl.astype(np.float)
eqw = eqw.astype(np.float)
steps = np.empty([1,1])
for i in range(len(lines)-5):
    start = wl[i]
    end = start+5
    #pdb.set_trace()
    steps = np.append(steps,(len(np.where(np.logical_and(wl >= start,wl<= end))[0])))
pdb.set_trace()
for i in range(len(steps)):
    n_steps = steps[i] #i want 5 angstroms, so i gotta figure out how many spaces that is..     
    window_length = n_steps+1 #so each window is shifted one datapoint..... cool...     
    dataset = dataset.window(window_length, shift=1, drop_remainder=True)
    pdb.set_trace()
pdb.set_trace()
#abandoning this for now, last issue was asking how to set this dataset up so that it could intake 
#different n-step sizes for each window (but we might not even hae to worry about that)
#actually. yes we do. bc the step size is different from the A size. 