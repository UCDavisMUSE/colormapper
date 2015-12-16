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

# Function Definitions

def nnlsWrapper(A, x):
    return nnls(A, x)[0]
    
def unmixParallelNNLS(image, A):
    """
    Performs Nonnegative Least Squares Unmixing via NNLS by
    parallel looping over the pixels in the image.
    
    Note: This does not work well for large images due to
    multithreading overhead.
    """

    # Both Versions seem to perform about the same
    
    # Version 1
    # image = image.transpose(2, 0, 1)
    # results = Parallel(n_jobs=4)(delayed(nnlsWrapper)(A, image[:,i,j])
    #     for i, j in product(range(image.shape[1]), range(image.shape[2])))
    # X = np.array(results).reshape(image.shape[1], image.shape[2], -1)

    # Version 2
    results = Parallel(n_jobs=4)(delayed(nnlsWrapper)(A, image[i,j,:])
        for i, j in product(range(image.shape[0]), range(image.shape[1])))
    X = np.array(results).reshape(image.shape[0], image.shape[1], -1)
    
    return X

def unmixSerialVectorNNLS(vector, A):
    X = np.zeros((vector.shape[0],A.shape[1]), dtype=np.float)
    for i in range(vector.shape[0]):
        X[i,:] = nnls(A, vector[i,:])[0]
    return X    
    
def unmixParallelColNNLS(image, A):
    """
    Performs Parallel Column-wise NNLS unmixing.
    """
    results = Parallel(n_jobs=2)(delayed(unmixSerialVectorNNLS)(image[:,j,:], A)
        for j in range(image.shape[1]))
    X = np.array(results).reshape(image.shape[1], image.shape[0], -1).transpose(1, 0, 2)
    
    return X
    
def unmixParallelRowNNLS(image, A):
    """
    Performs Parallel Row-wise NNLS unmixing.
    """
    results = Parallel(n_jobs=2)(delayed(unmixSerialVectorNNLS)(image[i,:,:], A)
        for i in range(image.shape[0]))
    X = np.array(results).reshape(image.shape[0], image.shape[1], -1)
    
    return X

def unmixSerialNNLS(image, A):
    """
    Performs Nonnegative Least Squares Unmixing via NNLS by 
    looping over the pixels in the image.
    """
    # Allocate output matrix   
    X = np.zeros((image.shape[0], image.shape[1], A.shape[1]), dtype=np.float)
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
    
# Function tests and benchmarks
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
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    print("For a " + str(image.shape[0]) + " by " + str(image.shape[1]) + " image:")
    
#   Method: unmixPinvLS:
    start = time.time()
    X_unmixPinvLS = unmixPinvLS(image, A)
    end = time.time()
    print("unmixPinvLSLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixPinvLS.shape[0]) + " by " + 
        str(X_unmixPinvLS.shape[1]) + " by " + 
        str(X_unmixPinvLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixPinvLS.shape[2]):
            plt.imshow(X_unmixPinvLS[:,:,i], interpolation = "bicubic")
            plt.xticks([]), plt.yticks([])
            plt.show()    
    
#   Method: unmixSerialNNLS
    start = time.time()
    X_unmixSerialNNLS = unmixSerialNNLS(image, A)
    end = time.time()
    print("unmixSerialNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixSerialNNLS.shape[0]) + " by " + 
        str(X_unmixSerialNNLS.shape[1]) + " by " + 
        str(X_unmixSerialNNLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixSerialNNLS.shape[2]):
            plt.imshow(X_unmixSerialNNLS[:,:,i], interpolation = "bicubic")
            plt.xticks([]), plt.yticks([])
            plt.show()

#   Method: unmixParalleRowNNLS
    start = time.time()
    X_unmixParalleRowNNLS = unmixParallelRowNNLS(image, A)
    end = time.time()
    print("unmixParallelRowNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParalleRowNNLS.shape[0]) + " by " + 
        str(X_unmixParalleRowNNLS.shape[1]) + " by " + 
        str(X_unmixParalleRowNNLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixParalleRowNNLS.shape[2]):
            plt.imshow(X_unmixParalleRowNNLS[:,:,i], interpolation = "bicubic")
            plt.xticks([]), plt.yticks([])
            plt.show()

#   Method: unmixParalleCollNNLS
    start = time.time()
    X_unmixParallelColNNLS = unmixParallelColNNLS(image, A)
    end = time.time()
    print("unmixParallelColNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParallelColNNLS.shape[0]) + " by " + 
        str(X_unmixParallelColNNLS.shape[1]) + " by " + 
        str(X_unmixParallelColNNLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixParallelColNNLS.shape[2]):
            plt.imshow(X_unmixParallelColNNLS[:,:,i], interpolation = "bicubic")
            plt.xticks([]), plt.yticks([])
            plt.show()

#   Method: unmixParallelNNLS
#   This method is too slow for large images
#     start = time.time()
#     X_unmixParallelNNLS = unmixParallelNNLS(image, A)
#     end = time.time()
#     print("unmixParallelNNLS Time: " + str(end-start) + " seconds.")
#     print("Result is an " + 
#         str(X_unmixParallelNNLS.shape[0]) + " by " + 
#         str(X_unmixParallelNNLS.shape[1]) + " by " + 
#         str(X_unmixParallelNNLS.shape[2]) + " matrix.")
#     if showPlots:
#         for i in range(X_unmixParallelNNLS.shape[2]):
#             plt.imshow(X_unmixParallelNNLS[:,:,i], interpolation = "bicubic")
#             plt.xticks([]), plt.yticks([])
#             plt.show()
