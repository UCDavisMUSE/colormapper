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

def unmixGradProjMatrixNNLS(image, A, tolerance=1e-4):
    """
    Performs NNLS via Gradient Projection of the primal problem.
    Terminates when duality gap falls below tolerance
    """
    if image.ndim == 2:
        (n1, n3) = image.shape
        n2 = 1;
    elif image.ndim == 3:
        (n1, n2, n3) = image.shape
    
    k = A.shape[1]
    # Reshape to n3 x n1*n2 matrix
    image = image.reshape(n1*n2,n3).T
    # Precompute Quantities
    ATA = np.dot(A.T,A)
    pinvA = np.linalg.pinv(A)
    ATimage = np.dot(A.T,image)
    alpha = np.linalg.norm(ATA,ord=2)
    # Start with thresholded pseudo-inverse
    X = np.dot(pinvA, image)
    X[X < 0] = 0
    # See if meets convergence criterion
    grad = np.dot(ATA,X) - ATimage
    gradthresh = np.array(grad)
    gradthresh[gradthresh < 0] = 0
    gap = np.tensordot(X, gradthresh)/(n1*n2*k)
    iter = 0
    while gap > tolerance:
        iter += 1
        # Gradient Step
        X = X - grad/alpha
        # Projection
        X[X < 0] = 0
        # See if meets convergence criterion
        grad = np.dot(ATA,X) - ATimage
        gradthresh = np.array(grad)
        gradthresh[gradthresh < 0] = 0
        gap = np.tensordot(X, gradthresh)/(n1*n2*k)

    # Reshape back to n1 x n2 x k image
    X = X.T.reshape(n1,n2,k)
    return X            
   
def unmixGradProjMatrixMinArcNNLS(image, A, tolerance=1e-4):
    """
    Performs NNLS via Gradient Projection of the primal problem.
    Includes minimization along projection arc
    Terminates when duality gap falls below tolerance
    """
    if image.ndim == 2:
        (n1, n3) = image.shape
        n2 = 1;
    elif image.ndim == 3:
        (n1, n2, n3) = image.shape
    
    k = A.shape[1]
    # Reshape to n3 x n1*n2 matrix
    image = image.reshape(n1*n2,n3).T
    # Precompute Quantities
    ATA = np.dot(A.T,A)
    pinvA = np.linalg.pinv(A)
    ATimage = np.dot(A.T,image)
    alpha = np.linalg.norm(ATA,ord=2)
    # Start with thresholded pseudo-inverse
    X = np.dot(pinvA, image)
    X[X < 0] = 0
    # See if meets convergence criterion
    grad = np.dot(ATA,X) - ATimage
    gradthresh = np.array(grad)
    gradthresh[gradthresh < 0] = 0
    gap = np.tensordot(X, gradthresh)
    while gap > tolerance:
        # Gradient Step
        Xproj = X - grad/alpha
        # Projection
        Xproj[Xproj < 0] = 0

        # Minimize along projection arc
        residual = np.dot(A,X)
        Adiff = np.dot(A,X - Xproj)
        step = np.tensordot(residual,Adiff)/(np.linalg.norm(Adiff,ord='fro')**2)
        if step > 1:
            X = Xproj
        elif step < 0:
            X = X
        else:
            X = (1-step)*X + step*Xproj
        
        # See if meets convergence criterion
        grad = np.dot(ATA,X) - ATimage
        gradthresh = np.array(grad)
        gradthresh[gradthresh < 0] = 0
        gap = np.tensordot(X, gradthresh)

    # Reshape back to n1 x n2 x k image
    X = X.T.reshape(n1,n2,k)
    return X   
    
def unmixIntensityPreservingPinvLS(image, A, threshold = True):
    """
    Performs Least Squares Unmixing via least-squares by using
    the psuedoinverse of the unmixing matrix. The solution is 
    subsequently adjusted so that the total intensity is preserved.
    This result is the solution of a least-squares minimization
    with a total intensity preservation constraint.
    Subsequently sets all negative values to zero.    
    """
    # Get dimensions of input image and matrix
    (n1, n2, n3) = image.shape
    k = A.shape[1]
    # Reshape to n3 x n1*n2 matrix
    image = image.reshape(n1*n2,n3).T
    # Pre-calculate pinv
    pinvA = lin.pinv(A)
    ATones = A.sum(0)
    # Least-squares via pinv
    XLS = np.dot(pinvA, image)
    # Intensity preservation adjustment
    whiteUnmix = pinvA.sum(1)
    weights = (image.sum(0) - np.dot(ATones, XLS))/np.inner(ATones, whiteUnmix)
    X = XLS + np.outer(whiteUnmix,weights)
    # Reshape back to n1 x n2 x k image
    X = X.T.reshape(n1,n2,k)
    # Set negative values to zero
    if threshold:
        X[X < 0] = 0
    return X

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
    results = Parallel(n_jobs=4)(delayed(unmixSerialVectorNNLS)(image[:,j,:], A)
        for j in range(image.shape[1]))
    X = np.array(results).reshape(image.shape[1], image.shape[0], -1).transpose(1, 0, 2)
    
    return X
    
def unmixParallelRowNNLS(image, A):
    """
    Performs Parallel Row-wise NNLS unmixing.
    """
    results = Parallel(n_jobs=4)(delayed(unmixSerialVectorNNLS)(image[i,:,:], A)
        for i in range(image.shape[0]))
    X = np.array(results).reshape(image.shape[0], image.shape[1], -1)
    
    return X
    
def unmixParallelColGradProjNNLS(image, A, tolerance = 1e-4):
    """
    Performs Parallel Column-wise NNLS unmixing using Gradient Projection NNLS.
    """
    results = Parallel(n_jobs=4)(delayed(unmixGradProjMatrixNNLS)(image[:,j,:], A, tolerance)
        for j in range(image.shape[1]))
    X = np.array(results).reshape(image.shape[1], image.shape[0], -1).transpose(1, 0, 2)
    
    return X
        
def unmixParallelRowGradProjNNLS(image, A, tolerance = 1e-4):
    """
    Performs Parallel Row-wise NNLS unmixing using Gradient Projections NNLS.
    """
    results = Parallel(n_jobs=4)(delayed(unmixGradProjMatrixNNLS)(image[i,:,:], A, tolerance)
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
    
def unmixPinvLS(image, A, threshold = True):
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
    if threshold:
        X[X < 0] = 0
    return X
    
# Function tests and benchmarks
if __name__=='__main__':
    # Perform Tests
    # Image is an n1 x n2 x 3 numpy array,
    # unmixing matrix A is 3 x k, where k is the number of components,
    # unmixed results should be n1 x n2 x k.

    showPlots = False
    threshold = True
    example = 1
    
    if example == 1:
        # Example unmixing matrix
        A = np.array([ [ 228, 244],
                       [ 250, 205],
                       [ 166, 100] ])
        # Test image (Convert to RGB)
        image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
        image = image[::1,::1,:]
    elif example == 2:
        # Example unmixing matrix
        A = np.array([ [   0,   0],
                       [ 255,   0],
                       [ 255, 255] ])
        # Test image (Convert to RGB)
        image = cv2.imread("testImages/Unmix Phantom.png")
    elif example == 3:
        # Example unmixing matrix
        A = np.array([ [127,   0],
                       [127, 127],
                       [  0, 127] ])
        # Test image (Convert to RGB)
        image = cv2.imread("testImages/SpectralQuadrant.png")
        
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    print("For a " + str(image.shape[0]) + " by " + str(image.shape[1]) + " image:")
  
#   Method: unmixGradProjMatrixMinArcNNLS
    start = time.time()
    X_unmixGradProjMatrixMinArcNNLS = unmixGradProjMatrixMinArcNNLS(image, A, tolerance=1e1)
    end = time.time()
    print("unmixGradProjMatrixMinArcNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixGradProjMatrixMinArcNNLS.shape[0]) + " by " + 
        str(X_unmixGradProjMatrixMinArcNNLS.shape[1]) + " by " + 
        str(X_unmixGradProjMatrixMinArcNNLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixGradProjMatrixMinArcNNLS.shape[2]):
            plt.imshow(X_unmixGradProjMatrixMinArcNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()    
    
#   Method: unmixGradProjMatrixNNLS
    start = time.time()
    X_unmixGradProjMatrixNNLS = unmixGradProjMatrixNNLS(image, A, tolerance=1e1)
    end = time.time()
    print("unmixGradProjMatrixNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixGradProjMatrixNNLS.shape[0]) + " by " + 
        str(X_unmixGradProjMatrixNNLS.shape[1]) + " by " + 
        str(X_unmixGradProjMatrixNNLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixGradProjMatrixNNLS.shape[2]):
            plt.imshow(X_unmixGradProjMatrixNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()    
            
    diff = X_unmixGradProjMatrixNNLS - X_unmixGradProjMatrixMinArcNNLS
    print('Max difference between Grad Proj NNLS and Grad Proj Min Arc NNLS: %8.3e' % abs(diff).max())
                
            
#   Method: unmixParallelRowGradProjNNLS
    start = time.time()
    X_unmixParallelRowGradProjNNLS = unmixParallelRowGradProjNNLS(image, A, tolerance=1e1)
    end = time.time()
    print("unmixParallelRowGradProjNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParallelRowGradProjNNLS.shape[0]) + " by " + 
        str(X_unmixParallelRowGradProjNNLS.shape[1]) + " by " + 
        str(X_unmixParallelRowGradProjNNLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixParallelRowGradProjNNLS.shape[2]):
            plt.imshow(X_unmixParallelRowGradProjNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()

#   Method: unmixParallelColGradProjlNNLS
    start = time.time()
    X_unmixParallelColGradProjNNLS = unmixParallelColGradProjNNLS(image, A, tolerance=1e1)
    end = time.time()
    print("unmixParallelColGradProjNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParallelColGradProjNNLS.shape[0]) + " by " + 
        str(X_unmixParallelColGradProjNNLS.shape[1]) + " by " + 
        str(X_unmixParallelColGradProjNNLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixParallelColGradProjNNLS.shape[2]):
            plt.imshow(X_unmixParallelColGradProjNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()


            
    
#   Method: unmixIntensityPreservingPinvLS
    start = time.time()
    X_unmixIntensityPreservingPinvLS = unmixIntensityPreservingPinvLS(image, A, threshold=threshold)
    end = time.time()
    print("unmixIntensityPreservingPinvLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixIntensityPreservingPinvLS.shape[0]) + " by " + 
        str(X_unmixIntensityPreservingPinvLS.shape[1]) + " by " + 
        str(X_unmixIntensityPreservingPinvLS.shape[2]) + " matrix.")
    if showPlots:        
        for i in range(X_unmixIntensityPreservingPinvLS.shape[2]):
            plt.imshow(X_unmixIntensityPreservingPinvLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()
    
#   Method: unmixPinvLS:
    start = time.time()
    X_unmixPinvLS = unmixPinvLS(image, A, threshold=threshold)
    end = time.time()
    print("unmixPinvLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixPinvLS.shape[0]) + " by " + 
        str(X_unmixPinvLS.shape[1]) + " by " + 
        str(X_unmixPinvLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixPinvLS.shape[2]):
            plt.imshow(X_unmixPinvLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
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
            plt.imshow(X_unmixSerialNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()
            
#   Method: unmixParallelRowNNLS
    start = time.time()
    X_unmixParallelRowNNLS = unmixParallelRowNNLS(image, A)
    end = time.time()
    print("unmixParallelRowNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParallelRowNNLS.shape[0]) + " by " + 
        str(X_unmixParallelRowNNLS.shape[1]) + " by " + 
        str(X_unmixParallelRowNNLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixParallelRowNNLS.shape[2]):
            plt.imshow(X_unmixParallelRowNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()

#   Method: unmixParallelCollNNLS
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
            plt.imshow(X_unmixParallelColNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
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
#             plt.imshow(X_unmixParallelNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
#             plt.xticks([]), plt.yticks([])
#             plt.show()


    # Kill this before next commit            
    diff = X_unmixSerialNNLS - X_unmixParallelColGradProjNNLS
    print('Max difference between serial NNLS and Parallel Col GradProj NNLS: %8.3e' % abs(diff).max())
    diff = X_unmixSerialNNLS - X_unmixParallelRowGradProjNNLS
    print('Max difference between serial NNLS and Parallel Row GradProj NNLS: %8.3e' % abs(diff).max())
    diff = X_unmixSerialNNLS - X_unmixGradProjMatrixNNLS
    print('Max difference between serial NNLS and GradProj NNLS: %8.3e' % abs(diff).max())

    for i in range(diff.shape[2]):
        plt.imshow(abs(diff[:,:,i]), interpolation = "nearest", cmap = plt.get_cmap("gray"))
        plt.xticks([]), plt.yticks([])
        plt.show()

    diff = X_unmixGradProjMatrixNNLS - X_unmixPinvLS
    for i in range(diff.shape[2]):
        plt.imshow(abs(diff[:,:,i]), interpolation = "nearest", cmap = plt.get_cmap("gray"))
        plt.xticks([]), plt.yticks([])
        plt.show()
