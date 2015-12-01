import numpy as np
import math
import scipy.optimize.nnls as nnls
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
    # Learn the affine colorspace map
    # y = 255/(1 + exp(-(Ax + c)))
    # from example data in the matrices X and Y
    
    tolerance = 1e-10 # Terminate when the norm of the gradient falls below this value
    logepsilon = 1e-2 # Parameter to avoid singularities in the log term
    
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
        print(X.min(),X.max())
        X = X.astype(np.uint8)
        return X

       
def unmixAndRecolor(inputColors, outputColors, inputImage,verbose=False):

    inputImage = inputImage.astype(float)/255
    unmixMatrix = inputColors.astype(float)/255
    outputColors = outputColors.astype(float)/255
    outputColors = 1-outputColors

    unmixedImage = unmixImage(unmixMatrix, inputImage, verbose=verbose)

    outputImage = np.ones( (inputImage.shape[0], inputImage.shape[1], inputColors.shape[0]) )

    for i in range(inputColors.shape[1]):
        for color in range(outputColors.shape[0]):
            outputImage[:,:,color] *= np.exp( - outputColors[color,i]*unmixedImage[:,:,i] )

    outputImage *= 255
                
    return outputImage.astype(np.uint8)

def unmixImage(unmixMatrix, inputImage, verbose=False):

    unmixedImage = np.zeros((inputImage.shape[0], inputImage.shape[1], unmixMatrix.shape[1]))
    
    for i in range(inputImage.shape[0]):
        for j in range(inputImage.shape[1]):
            (unmixedImage[i,j,:], residual) = nnls(unmixMatrix,inputImage[i,j,:].astype(float))
        if verbose:
            print("Row: " + str(i))
            
    return unmixedImage
    
    
    
    