#TICTOC TIMING
import time

def TicTocGenerator():
    # Generator that returns time differences
    ti = 0           # initial time
    tf = time.time() # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf-ti # returns the time difference

TicToc = TicTocGenerator() # create an instance of the TicTocGen generator

# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print( "Elapsed time: %f seconds.\n" %tempTimeInterval )

def tic():
    # Records a time in TicToc, marks the beginning of a time interval
    toc(False)
#""" 

from sklearn.multioutput import MultiOutputClassifier
import pdb 
import numpy as np 
from sklearn.datasets import make_regression
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RepeatedKFold
from pyearth import Earth
from sklearn.multioutput import MultiOutputRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
X = np.load('nonsplitdata_X.npy', allow_pickle = True )
Y = np.load('nonsplitdata_Y.npy', allow_pickle = True )
[X_train,Y_train,X_val, Y_val, X_test, Y_test] = np.load('traintestsplits_initial.npy', allow_pickle = True)

clf = MultiOutputRegressor(DecisionTreeRegressor()).fit(X_train,Y_train)
gross_pred = clf.predict(X_test)
pdb.set_trace()
mse = mean_squared_error(Y_test,gross_pred)
rmse = np.sqrt(mse)
print(rmse)
#print(Y_test[[0]])
#print(clf.score(X_test,Y_test))
#pdb.set_trace()
#model = Earth(rcond = None)
#cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
#n_scores = cross_val_score(model, X, Y, scoring='neg_mean_absolute_error', cv=cv, n_jobs=-1)
#print('MAE: %.3f (%.3f)' % (np.mean(n_scores), np.std(n_scores)))
#print(model.trace())
#print(model.summary())