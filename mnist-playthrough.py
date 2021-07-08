#mnist playthrough
import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml 
import pdb
mnist = fetch_openml('mnist_784', version=1)
X,Y = mnist['data'], mnist['target']
pdb.set_trace()