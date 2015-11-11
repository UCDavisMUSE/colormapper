import numpy as np
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
    
def applyAffineColorspaceMap(X, A, c):
    # Applies the affine colorspace map
    # y = Ax + c
    # to every pixel in the image X
    X = X.astype(float)
    (n1, n2, n3) = X.shape
    X = X.astype(float)
    X = X.reshape(n1*n2,n3)
    X = np.dot(X,A.transpose()) + np.dot(np.ones((n1*n2,1),float),c.transpose())
    X = X.reshape(n1,n2,n3)
    # Truncate to [0,255]
    X[X < 0.0] = 0.0
    X[X > 255.0] = 255.0
    X = X.astype(np.uint8)
    return X
    
    
    
    