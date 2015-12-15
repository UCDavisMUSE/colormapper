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

# results = Parallel(n_jobs=10)(delayed(nnls)(A, b_array[:,i,j])[0]
#              for i, j in product(range(100), range(100)))
# x_array = np.array(results).reshape(100, 100, -1).transpose(2, 0, 1)

def parallelEx():
    results = Parallel(n_jobs=4)(delayed(math.sqrt)(i*j)
        for i, j in product(range(10), range(10)))
    return results

def dummy(A, x):
    return nnls(A, x)[0]
#    return np.dot(A.T, x)

    
def unmixParallelNNLS(image, A):
    """
    Performs Nonnegative Least Squares Unmixing via NNLS by
    parallel looping over the pixels in the image.
    """
    # Both Versions seem to perform about the same
    
# Version 1
#     image = image.transpose(2, 0, 1)
#     results = Parallel(n_jobs=4)(delayed(dummy)(A, image[:,i,j])
#         for i, j in product(range(image.shape[1]), range(image.shape[2])))
#     X = np.array(results).reshape(image.shape[1], image.shape[2], -1)

# Version 2
    results = Parallel(n_jobs=4)(delayed(dummy)(A, image[i,j,:])
        for i, j in product(range(image.shape[0]), range(image.shape[1])))
    X = np.array(results).reshape(image.shape[0], image.shape[1], -1)
    
    return X

def dummyCol(A, X):
    Z = np.zeros((X.shape[0],A.shape[1]), dtype=np.float)
    for i in range(X.shape[0]):
        Z[i,:] = nnls(A, X[i,:])[0]
    return Z
    
def unmixParallelColNNLS(image, A):
    """
    Performs NNLS Column-wise
    """
    results = Parallel(n_jobs=4)(delayed(dummyCol)(A, image[:,j,:])
        for j in range(image.shape[1]))
    X = np.array(results).reshape(image.shape[1], image.shape[0], -1).transpose(1, 0, 2)
    
    return X
    
def unmixParallelRowNNLS(image, A):
    """
    Performs NNLS Row-wise
    """
    results = Parallel(n_jobs=4)(delayed(dummyCol)(A, image[i,:,:])
        for i in range(image.shape[0]))
    X = np.array(results).reshape(image.shape[0], image.shape[1], -1)
    
    return X
        
        
        






### --- Clean from here down ---

def unmixSerialNNLS(image, A):
    """
    Performs Nonnegative Least Squares Unmixing via NNLS by 
    looping over the pixels in the image.
    """
    # Allocate output matrix   
    X = np.zeros((image.shape[0], image.shape[1], A.shape[1]), dtype=np.float32)
    # Loop over all pixels
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            # Unmix via NNLS
            X[i,j,:] = nnls(A, image[i,j,:])[0]
    return X
    
def unmixPinvLS(image, A):
    """
    Performs Least Squares Unmixing via least-squares by using
    the psuedoinverse of the unmixing matrix.
    Subsequently sets all negative values to zero.    
    """
    # Get dimensions of input image and matrix
    (n1, n2, n3) = image.shape
    k = A.shape[1]
    # Reshape to n3 x n1*n2 matrix
    image = image.reshape(n1*n2,n3).T
    # Least-squares via pinv
    X = np.dot(lin.pinv(A), image)
    # Reshape back to n1 x n2 x k image
    X = X.T.reshape(n1,n2,k)
    # Set negative values to zero
    X[X < 0] = 0
    return X


if __name__=='__main__':
    # Perform Tests
    # Image is an n1 x n2 x 3 numpy array,
    # unmixing matrix A is 3 x k, where k is the number of components,
    # unmixed results should be n1 x n2 x k.

    showPlots = False
    
    # Example unmixing matrix
    A = np.array([ [ 228, 244],
                   [ 250, 205],
                   [ 166, 100] ])

    # Test image (Convert to RGB)
    image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
#    image = image[0:400,0:300,:]
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    print("For a " + str(image.shape[0]) + " by " + str(image.shape[1]) + " image:")

#    print(parallelEx())

#   Method: unmixParalleRowNNLS
    start = time.time()
    X3 = unmixParallelRowNNLS(image, A)
    end = time.time()
    print("unmixParallelRowNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X3.shape[0]) + " by " + 
        str(X3.shape[1]) + " by " + 
        str(X3.shape[2]) + " matrix.")
    for i in range(X3.shape[2]):
        plt.imshow(X3[:,:,i], interpolation = "bicubic")
        plt.xticks([]), plt.yticks([])
        if showPlots:
            plt.show()

#   Method: unmixParalleCollNNLS
    start = time.time()
    X1 = unmixParallelColNNLS(image, A)
    end = time.time()
    print("unmixParallelColNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X1.shape[0]) + " by " + 
        str(X1.shape[1]) + " by " + 
        str(X1.shape[2]) + " matrix.")
    for i in range(X1.shape[2]):
        plt.imshow(X1[:,:,i], interpolation = "bicubic")
        plt.xticks([]), plt.yticks([])
        if showPlots:
            plt.show()
                
#   Method: unmixParallelNNLS
#   Too slow!!
#     start = time.time()
#     X2 = unmixParallelNNLS(image, A)
#     end = time.time()
#     print("unmixParallelNNLS Time: " + str(end-start) + " seconds.")
#     print("Result is an " + 
#         str(X2.shape[0]) + " by " + 
#         str(X2.shape[1]) + " by " + 
#         str(X2.shape[2]) + " matrix.")
#     for i in range(X2.shape[2]):
#         plt.imshow(X2[:,:,i], interpolation = "bicubic")
#         plt.xticks([]), plt.yticks([])
#         if showPlots:
#             plt.show()

 
#   Method: unmixSerialNNLS
    start = time.time()
    X = unmixSerialNNLS(image, A)
    end = time.time()
    print("unmixSerialNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X.shape[0]) + " by " + 
        str(X.shape[1]) + " by " + 
        str(X.shape[2]) + " matrix.")
        
    for i in range(X.shape[2]):
        plt.imshow(X[:,:,i], interpolation = "bicubic")
        plt.xticks([]), plt.yticks([])
        if showPlots:
            plt.show()


        
    diff = abs(X - X1)
    print(diff.max())
    
#     diff = abs(X - X2)
#     print(diff.max())
    
    diff = abs(X - X3)
    print(diff.max())
      
        
#   Method: unmixPinvLS:
    start = time.time()
    X = unmixPinvLS(image, A)
    end = time.time()
    print("unmixPinvLSLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X.shape[0]) + " by " + 
        str(X.shape[1]) + " by " + 
        str(X.shape[2]) + " matrix.")
    
    for i in range(X.shape[2]):
        plt.imshow(X[:,:,i], interpolation = "bicubic")
        plt.xticks([]), plt.yticks([])
        if showPlots:
            plt.show()    
    