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
from sklearn.decomposition import NMF
from colormappingMethods import unmixAndRecolor
from nonnegativeLeastSquares import unmixParallelColNNLS


outputColors = np.array([ [ 70, 230],
                       [ 30, 160],
                       [150, 200] ])
               
showPlots = True
cps = True
# Test image (cv2 is in BGR)
image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
#image = cv2.imread("testImages/AVG_Stack-9.jpg")
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
image = image[::2,::2,:]
(n1,n2,n3) = image.shape
Y = image.reshape(n1*n2,n3)

k=2
alpha = 20
l1_ratio = 1
init = 'random'#'nndsfda'
model = NMF(n_components=k, init=init, l1_ratio = l1_ratio, alpha = alpha ,tol = 1e-3)
model.fit(Y)
A = model.components_.T
X = model.transform(Y)
ximage = X.reshape(n1,n2,k)


if showPlots:        
    for i in range(ximage.shape[2]):
        plt.imshow(ximage[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
        plt.title("NMF Unmixing")
        plt.xticks([]), plt.yticks([])
        plt.show()

# If we assume that bluest spectra contains the nuclei, put in first column
if A[2,1] > A[2,1]:
    A[:,0], A[:,1] = A[:,1], A[:,0]

# Normalize columns    
A[:,0] = A[:,0]/np.sum(A[:,0])
A[:,1] = A[:,1]/np.sum(A[:,1])    
    

imageHE = unmixAndRecolor(255*A, outputColors, image,verbose=False,method='nnls')

if showPlots:
        plt.imshow(imageHE, interpolation = "nearest")
        plt.title("HE Conversion")
        plt.xticks([]), plt.yticks([])
        plt.show()

        
if cps:
    # Compute Pure spectra
    alpha = A[:,1]/A[:,0]
    alpha = alpha.min()
    A[:,1] = A[:,1] - alpha*A[:,0]
    A[:,1] = A[:,1]/np.sum(A[:,1])

    xpure = unmixParallelColNNLS(image, 255*A)
    print((xpure[:,:,0]).max())
    print((xpure[:,:,1]).max())

    if showPlots:        
        for i in range(xpure.shape[2]):
            plt.imshow(xpure[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.title("Pure Spectra NNLS Unmixing")
            plt.xticks([]), plt.yticks([])
            plt.show()

    pureimageHE = unmixAndRecolor(255*A, outputColors, image,verbose=False,method='nnls')

    if showPlots:
            plt.imshow(pureimageHE, interpolation = "nearest")
            plt.title("Pure Spectra HE Conversion")
            plt.xticks([]), plt.yticks([])
            plt.show()    