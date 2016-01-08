import math
import numpy as np
import numpy.linalg as lin
import scipy.optimize.nnls as nnls
import scipy.optimize as opt
import cv2
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
    
def unmixParallelTileGradProjNNLS(image, A, tolerance = 1e-4, tileSize = (64, 64)):
    """
    Performs Parallel Tile-wise NNLS unmixing using Gradient Projection NNLS.
    
    To Do: Determine the optimal tile size for a typical image.
    """
    (height, width, colors) = image.shape
    heightTiles = int(math.ceil(1.0*height/tileSize[0]))
    widthTiles = int(math.ceil(1.0*width/tileSize[1]))
        
    results = Parallel(n_jobs=4)(delayed(unmixGradProjMatrixNNLS)(image[tileSize[0]*i:tileSize[0]*(i+1),tileSize[1]*j:tileSize[1]*(j+1),:], A, tolerance)
        for i,j in product(range(heightTiles), range(widthTiles)))
        
    # Reassemble results
    X = np.zeros((image.shape[0], image.shape[1], A.shape[1]), dtype = float)
    for i,j in product(range(heightTiles), range(widthTiles)):
        X[tileSize[0]*i:tileSize[0]*(i+1),
          tileSize[1]*j:tileSize[1]*(j+1),:] = np.array(results[j + widthTiles*i])
    
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
    