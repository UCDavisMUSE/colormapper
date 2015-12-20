import math
import numpy as np
import numpy.linalg as lin
import scipy.optimize.nnls as nnls
import scipy.optimize as opt
import cv2
import matplotlib.pyplot as plt
import time
from joblib import Parallel, delayed
from itertools import product
import itertools

# Function Definitions

def subspaceNNLS(A, y):
    """
    Perform NNLS unmixing by shrinking the size of the subspace.
    Turns out that this is much slower than just performing the
    Fortran NNLS routine, so don't ever use this. Just keeping 
    the code around in case the subset selection idea comes in
    handy in the future.
    """
    k = A.shape[1]
    x = np.zeros(k)
    columns = range(k)
    numColumns = range(1,k+1)
    numColumns.reverse()
    foundNNSolution = False
    for i in numColumns:
        bestResidual = float("inf")
        bestSubspace = []
        bestxTest = []
        for subspace in itertools.combinations(columns, i):
            Asub = A[:,subspace]
            xTest = np.dot(np.linalg.pinv(Asub),y)
            if xTest.min() >= 0:
                # Then it is nonnegative
                foundNNSolution = True
                residual = np.linalg.norm( np.dot(Asub,xTest) - y)
                if residual < bestResidual:
                    bestResidual = residual
                    bestSubspace = subspace
                    bestxTest = xTest
        if foundNNSolution:
            x[list(bestSubspace)] = bestxTest
            break
    return x
    
if __name__ == '__main__':
    
    # Generate random problem instance
    n = 1000000
    m = 3
    showMatrices = False
    
    A = np.random.rand(n,m)
    if showMatrices:
        print("A:")
        print(A)
    
    y = np.dot(A,np.random.randn(m))
    if showMatrices:
        print("y:")
        print(y)
    
    start = time.time()
    x_NNLS = nnls(A, y)[0]    
    end = time.time()
    print("NNLS: " + str(end-start) + " Seconds")
    if showMatrices:
        print(x_NNLS)
    
    start = time.time()
    x_subspaceNNLS = subspaceNNLS(A, y)
    end = time.time()
    print("Subspace NNLS:" + str(end-start) + " Seconds")
    if showMatrices:
        print(x_subspaceNNLS)
    
