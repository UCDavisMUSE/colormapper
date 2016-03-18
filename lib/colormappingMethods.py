import numpy as np
import math
import scipy.optimize.nnls as nnls
from nonnegativeLeastSquares import *
from OpenCLGradProjNNLS import *

#import pysptools.abundance_maps.amaps as amaps
# This file contains various color mapping methods.
# Each of the methods is coded to take as input a numpy array of type uint8, 
# along with various parameters to produce an output that is a numpy array of type uint8.

# Notes:
# Norm: np.linalg.norm(x)
# Matrix Multiplication: np.dot(x,y)
# Matrix Transpose: x.transpose()
# Ones: ones((3,5),float)
# Elementwise Division: np.divide(x,y)
# Pseudoinverse: linalg.pinv(x)

def learnAffineColorspaceMap(X, Y):
    # Learn the affine colorspace map
    # y = Ax + c
    # from example data in the matrices X and Y
    
    tolerance = 1e-10 # Terminate when the norm of the gradient falls below this value
    
    (x1, x2) = X.shape
    (y1, y2) = Y.shape
  
    X = X.astype(float)
    Y = Y.astype(float)
    
    # Precompute quantities
    onesVect = np.ones((x2,1), float)
    XXT = np.dot(X, X.transpose())
    AX = Y
    cNew = np.dot((Y - AX), onesVect/x2)
    gradNorm = tolerance + 1
    while gradNorm > tolerance:
        # Minimize wrt c
        c = cNew
        # Minimize wrt A
        A = np.dot((Y - np.dot(c,onesVect.transpose())), np.linalg.pinv(X))
        AX = np.dot(A,X)
        # Compute gradient norm
        cNew = np.dot((Y - AX), onesVect/x2)
        gradNorm = np.linalg.norm(c - cNew)
           
    return (A,c)
    
def applyAffineColorspaceMap(X, A, c, method = 0, tileSize = (64, 64)):
    # Applies the affine colorspace map
    # y = Ax + c
    # to every pixel in the image X
    if method == 0:
        # Done using reshapes and matrix multiplication
        X = X.astype(float)
        (n1, n2, n3) = X.shape
        X = X.reshape(n1*n2,n3)
        X = np.dot(X,A.transpose()) + np.dot(np.ones((n1*n2,1),float),c.transpose())
        X = X.reshape(n1,n2,n3)
        # Truncate to [0,255]
        X[X < 0.0] = 0.0
        X[X > 255.0] = 255.0
        X = X.astype(np.uint8)
        return X

    elif method == 1:
        # Done using a for loop
        X = X.astype(float)
        (n1, n2, n3) = X.shape
        Y = np.empty((n1, n2, n3),float)
        for color in range(n3):
            Y[:,:,color] = A[color,0]*X[:,:,0] + A[color,1]*X[:,:,1] + A[color,2]*X[:,:,2] + c[color]
        Y[Y < 0.0] = 0.0
        Y[Y > 255.0] = 255.0
        Y = Y.astype(np.uint8)
        return Y

    elif method == 2:
        # Done using unrolled for loops, always assume 3 colors
        X = X.astype(float)
        Y = np.empty(X.shape, float)
        Y[:,:,0] = A[0,0]*X[:,:,0] + A[0,1]*X[:,:,1] + A[0,2]*X[:,:,2] + c[0]
        Y[:,:,1] = A[1,0]*X[:,:,0] + A[1,1]*X[:,:,1] + A[1,2]*X[:,:,2] + c[1]
        Y[:,:,2] = A[2,0]*X[:,:,0] + A[2,1]*X[:,:,1] + A[2,2]*X[:,:,2] + c[2]
        Y[Y < 0.0] = 0.0
        Y[Y > 255.0] = 255.0
        Y = Y.astype(np.uint8)
        return Y
        
    elif method == 3:
        # Done by processing a small tile at a time

        heightTiles = int(math.floor(1.0*X.shape[0]/tileSize[0]))
        widthTiles = int(math.floor(1.0*X.shape[1]/tileSize[1]))

        heightRemainder = X.shape[0] % tileSize[0]
        widthRemainder = X.shape[1] % tileSize[1]

        for widthTile in range(widthTiles + 1):
            for heightTile in range(heightTiles + 1):
             
                if heightTile < heightTiles and widthTile < widthTiles:
                    X[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                        widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:] = applyAffineColorspaceMap(
                        X[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                        widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:], A, c)
                elif heightTile < heightTiles and widthTile == widthTiles and widthRemainder != 0:
                    X[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                        widthTile*tileSize[1]:,:] = applyAffineColorspaceMap(
                        X[heightTile*tileSize[0]:(heightTile+1)*tileSize[0], 
                            widthTile*tileSize[1]:,:], A, c)
                elif heightTile == heightTiles and widthTile < widthTiles and heightRemainder != 0:
                    X[heightTile*tileSize[0]:,
                        widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:] = applyAffineColorspaceMap(
                        X[heightTile*tileSize[0]:,
                            widthTile*tileSize[1]:(widthTile+1)*tileSize[1],:], A, c)
                elif heightTile == heightTiles and widthTile == widthTiles and widthRemainder != 0 and heightRemainder !=0:
                    X[heightTile*tileSize[0]:, 
                        widthTile*tileSize[1]:,:] = applyAffineColorspaceMap(
                        X[heightTile*tileSize[0]:, 
                            widthTile*tileSize[1]:,:], A, c)
        return X
        
    else:
        print("Incorrect method parameter.")
        return
        
def learnLogisticColorspaceMap(X, Y):
    # Learn the logistic colorspace map
    # y = 255/(1 + exp(-(Ax + c)))
    # from example data in the matrices X and Y
    
    tolerance = 1e-10 # Terminate when the norm of the gradient falls below this value
    if Y.max() == 255:
        logepsilon = 1e-2 # Parameter to avoid singularities in the log term
    else:
        logepsilon = 0
    
    (x1, x2) = X.shape
    (y1, y2) = Y.shape
    
    X = X.astype(float)
    Y = Y.astype(float)
    
    X = X/255
    Y = Y/255

    Y = np.log(Y/(1 - Y + logepsilon))
    
    # Precompute quantities
    onesVect = np.ones((x2,1), float)
    XXT = np.dot(X, X.transpose())
    AX = Y
    cNew = np.dot((Y - AX), onesVect/x2)
    gradNorm = tolerance + 1
    while gradNorm > tolerance:
        # Minimize wrt c
        c = cNew
        # Minimize wrt A
        A = np.dot((Y - np.dot(c,onesVect.transpose())), np.linalg.pinv(X))
        AX = np.dot(A,X)
        # Compute gradient norm
        cNew = np.dot((Y - AX), onesVect/x2)
        gradNorm = np.linalg.norm(c - cNew)
           
    return (A,c) 
    
def learnLogisticColorspaceMapGradient(X, Y):
    # Learn the logistic colorspace map
    # y = 255/(1 + exp(-(Ax + c)))
    # from example data in the matrices X and Y
    # Using gradient descent with a step size derived from the largest 
    # eigenvalue of the Hessian matrix
    
    def sigma(a,c,x):
        return 1/(1 + np.exp( - (c + np.dot(a,x))))
    
    if Y.max() == 255:
        tolerance = 1e-3
    else:
        tolerance = 1e-5
    
    (x1, x2) = X.shape
    (y1, y2) = Y.shape
    
    X = X.astype(float)
    Y = Y.astype(float)
    
    X = X/255
    Y = Y/255
    
    normSum = 0.0
    for i in range(X.shape[1]):
        normSum += np.dot(X[:,i],X[:,i])

    # Bound on the Hessian, inverse of stepsize, should work better than below
    # This seems to work okay, keep for now.
    # Welp, doesn't work. Kill it.
    alphaA = normSum/4.0
    alphac = alphaA
    
    # Bound on the Hessian
    alphaA = 3/4.0*X.shape[1]
    alphac = alphaA    
    
    # Initialize A, c
    A = np.zeros((Y.shape[0], X.shape[0]), float)
    c = np.zeros((Y.shape[0],1), float)
    
    gradA = np.zeros((Y.shape[0], X.shape[0]), float)
    gradc = np.zeros((Y.shape[0],1), float)
    
    gradNorm = tolerance + 1
    while gradNorm > tolerance:
        # Compute Gradient
        gradA = 0.0*gradA
        gradc = 0.0*gradc
        for l in range(A.shape[0]):
            for i in range(X.shape[1]):
                precompute = sigma(A[l,:],c[l],X[:,i]) - Y[l,i]
                gradA[l,:] += precompute*X[:,i]
                gradc[l] += precompute            
            
        # Take Gradient Descent Step
        A = A - gradA/alphaA
        c = c - gradc/alphac
        
        # Compute gradient norm
        grad = np.hstack( (gradA.flatten(), gradc.flatten()))
        gradNorm = np.linalg.norm(grad)
#        print(gradNorm)
        
    return (A,c)
        
def applyLogisticColorspaceMap(X, A, c, method = 0, tileSize = (64, 64)):
    # Applies the affine colorspace map
    # y = Ax + c
    # to every pixel in the image X
    if method == 0:
        # Done using reshapes and matrix multiplication
        X = X.astype(float)
        X = X/255
        (n1, n2, n3) = X.shape
        X = X.reshape(n1*n2,n3)
        X = np.dot(X,A.transpose()) + np.dot(np.ones((n1*n2,1),float),c.transpose())
        X = 255/(1 + np.exp(-X))
        X = X.reshape(n1,n2,n3)
        X = X.astype(np.uint8)
        return X

def unmixAndRecolor(inputColors, outputColors, inputImage,verbose=False,method='OpenCLnnls'):

    inputImage = inputImage.astype(float)/255
    unmixMatrix = inputColors.astype(float)/255
    outputColors = outputColors.astype(float)/255
    outputColors = 1-outputColors

    unmixedImage = unmixImage(unmixMatrix, inputImage, verbose=verbose,method=method)

    outputImage = np.ones( (inputImage.shape[0], inputImage.shape[1], inputColors.shape[0]) )

    for i in range(inputColors.shape[1]):
        for color in range(outputColors.shape[0]):
            outputImage[:,:,color] *= np.exp( - outputColors[color,i]*unmixedImage[:,:,i] )

    outputImage *= 255
                
    return outputImage.astype(np.uint8)

def unmixImage(unmixMatrix, inputImage, verbose=False, method='OpenCLnnls'):

#     (n1, n2, n3) = inputImage.shape
#     inputImage = inputImage.reshape(n1*n2,n3)
#     k = unmixMatrix.shape[1]
    if method == 'nnls':
        unmixedImage = unmixParallelTileGradProjNNLS(inputImage, unmixMatrix, tolerance = 1e+1)
#        unmixedImage = NNLS(inputImage, unmixMatrix.transpose())
    elif method == 'ls':
        unmixedImage = unmixPinvLS(inputImage, unmixMatrix, threshold = True)
    elif method == 'OpenCLnnls':
        unmixedImage = OpenCLGradProjNNLS(inputImage, unmixMatrix, tolerance = 1e+1)
#        unmixedImage = LS(inputImage, unmixMatrix.transpose())
#     unmixedImage = unmixedImage.reshape(n1,n2,k)
    
#    print("Finished Unmixing!")
    
    # unmixedImage = np.zeros((inputImage.shape[0], inputImage.shape[1], unmixMatrix.shape[1]))
#        
#     
#     for i in range(inputImage.shape[0]):
#         for j in range(inputImage.shape[1]):
#             (unmixedImage[i,j,:], residual) = nnls(unmixMatrix,inputImage[i,j,:].astype(float))
#         if verbose:
#             print("Row: " + str(i))
#             
    return unmixedImage
    
def unmixAndRecolorFluorescent(inputColors, outputColors, inputImage,verbose=False,method='nnls'):

    inputImage = inputImage.astype(float)/255
    unmixMatrix = inputColors.astype(float)/255
    outputColors = outputColors.astype(float)/255

    unmixedImage = unmixImage(unmixMatrix, inputImage, verbose=verbose,method=method)

    outputImage = np.zeros( (inputImage.shape[0], inputImage.shape[1], inputColors.shape[0]) )

    for i in range(inputColors.shape[1]):
        for color in range(outputColors.shape[0]):
            outputImage[:,:,color] += outputColors[color,i]*unmixedImage[:,:,i]

    outputImage *= 255
    outputImage[outputImage > 255] = 255
    outputImage[outputImage < 0] = 0
                
    return outputImage.astype(np.uint8)    
    
def remixImage(x, B, thresh, alpha, gamma, method = 0):
    x = np.float64(x)
    B = np.float64(B) # Need to normalize
    thresh = np.float64(thresh)
    alpha = np.float64(alpha)
    gamma = np.float64(gamma)

    if method == 0:
        # Brightfield (Beer-Lambert)
        
        # Compliment colors
        B = 1 - B/255
        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Threshold low intensities
        for i in range(x.shape[2]):
            x[:,:,i] = x[:,:,i] - thresh[i]
        x[x < 0] = 0    

        outputImage = np.ones( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0.0:
                for color in range(B.shape[0]):
                    outputImage[:,:,color] *= \
                        np.exp( - \
                        alpha[i]*B[color,i]*(x[:,:,i].max()* \
                        (x[:,:,i]/x[:,:,i].max())**gamma[i]) )
        
        outputImage8Bit = 255*outputImage
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit
        
    elif method == 1:
        # Brightfield (Invert-Multiply)
        
        # Compliment colors
        B = 1 - B/255        
        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Threshold low intensities
        for i in range(x.shape[2]):
            x[:,:,i] = x[:,:,i] - thresh[i]
        x[x < 0] = 0    
        
        # Gamma and alpha
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0:
                x[:,:,i] = alpha[i]*x[:,:,i].max()*(x[:,:,i]/x[:,:,i].max())**gamma[i]
                
        
        outputImage = np.ones( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            for color in range(B.shape[0]):
                    tmp = 1 - B[color,i]*x[:,:,i]
                    tmp[tmp < 0] = 0
                    outputImage[:,:,color] *= tmp
        
        outputImage8Bit = 255*outputImage
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit

        
    elif method == 2:
        # Fluorescence

        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Threshold low intensities
        for i in range(x.shape[2]):
            x[:,:,i] = x[:,:,i] - thresh[i]
        x[x < 0] = 0    

        outputImage = np.zeros( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0.0:
                for color in range(B.shape[0]):
                    outputImage[:,:,color] += \
                        alpha[i]*B[color,i]*(x[:,:,i].max()* \
                        (x[:,:,i]/x[:,:,i].max())**gamma[i]) 

        outputImage8Bit = 255*outputImage
        outputImage8Bit[outputImage8Bit > 255] = 255        
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit
        
def remixImageBrightnessContrast(x, B, beta, alpha, gamma, method = 0):
    x = np.float64(x)
    B = np.float64(B) # Need to normalize
    beta = np.float64(beta)
    alpha = np.float64(alpha)
    gamma = np.float64(gamma)

    if method == 0:
        # Brightfield (Beer-Lambert)
        
        # Compliment colors
        B = 1 - B/255
        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Brightness and Contrast
        for i in range(x.shape[2]):
            x[:,:,i] = alpha[i]*(x[:,:,i] - beta[i])
        x[x < 0] = 0    

        outputImage = np.ones( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0.0:
                for color in range(B.shape[0]):
                    outputImage[:,:,color] *= \
                        np.exp( - 
                        B[color,i]*(x[:,:,i].max()* \
                        (x[:,:,i]/x[:,:,i].max())**gamma[i]) )
        
        outputImage8Bit = 255*outputImage
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit
        
    elif method == 1:
        # Brightfield (Invert-Multiply)
        
        # Compliment colors
        B = 1 - B/255        
        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Brightness and Contrast
        for i in range(x.shape[2]):
            x[:,:,i] = alpha[i]*(x[:,:,i] - beta[i])
        x[x < 0] = 0      
        
        # Gamma and alpha
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0:
                x[:,:,i] = x[:,:,i].max()*(x[:,:,i]/x[:,:,i].max())**gamma[i]
                
        
        outputImage = np.ones( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            for color in range(B.shape[0]):
                    tmp = 1 - B[color,i]*x[:,:,i]
                    tmp[tmp < 0] = 0
                    outputImage[:,:,color] *= tmp
        
        outputImage8Bit = 255*outputImage
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit

        
    elif method == 2:
        # Fluorescence

        # Normalize
        for i in range(B.shape[1]):
            B[:,i] = B[:,i]/np.sum(B[:,i])
    
        # Brightness and Contrast
        for i in range(x.shape[2]):
            x[:,:,i] = alpha[i]*(x[:,:,i] + beta[i])
        x[x < 0] = 0     

        outputImage = np.zeros( 
            (x.shape[0], x.shape[1], B.shape[0]),
            dtype = np.float64)
        for i in range(B.shape[1]):
            if x[:,:,i].max() > 0.0:
                for color in range(B.shape[0]):
                    outputImage[:,:,color] += \
                        B[color,i]*(x[:,:,i].max()* \
                        (x[:,:,i]/x[:,:,i].max())**gamma[i]) 

        outputImage8Bit = 255*outputImage
        outputImage8Bit[outputImage8Bit > 255] = 255        
        outputImage8Bit = outputImage8Bit.astype(np.uint8)          
        return outputImage8Bit

    
    
# Stolen NNLS method from pysptools    
def NNLS(M, U):
    """
    NNLS performs non-negative constrained least squares of each pixel
    in M using the endmember signatures of U.  Non-negative constrained least
    squares with the abundance nonnegative constraint (ANC).
    Utilizes the method of Bro.

    Parameters:
        M: `numpy array`
            2D data matrix (N x p).

        U: `numpy array`
            2D matrix of endmembers (q x p).

    Returns: `numpy array`
        An abundance maps (N x q).

    References:
        Bro R., de Jong S., Journal of Chemometrics, 1997, 11, 393-401.
    """
    import scipy.optimize as opt

    N, p1 = M.shape
    q, p2 = U.shape

    X = np.zeros((N, q), dtype=np.float32)
    MtM = np.dot(U, U.T)
    for n1 in xrange(N):
        # opt.nnls() return a tuple, the first element is the result
#        X[n1] = opt.nnls(MtM, np.dot(U, M[n1]))[0]
        
        X[n1] = opt.nnls(U.T, M[n1])[0]
    return X    
    
    
def LS(M, U):

    import numpy.linalg as lin
    
    X = np.dot(lin.pinv(U.T), M.T).T
    X[X < 0] = 0
        
    return X    
    
    
    
    
    