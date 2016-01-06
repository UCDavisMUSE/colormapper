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
from sklearn.cluster import KMeans


# Parameters
showPlots = True
cps = True

# Test image (cv2 is in BGR)
image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
#image = cv2.imread("testImages/AVG_Stack-9.jpg")
image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
image = image[::2,::2,:]
(n1,n2,n3) = image.shape
Y = image.reshape(n1*n2,n3)

if showPlots:        
    plt.imshow(image, interpolation = "nearest")
    plt.title("Original Image")
    plt.xticks([]), plt.yticks([])
    plt.show()

# Method 0: Unmix and recolor using (unnormalized) spectra calculated from Nuance
Anuance = np.array([[  0, 212],
                    [ 25, 188],
                    [ 34,  90]])
outputColors = np.array([   [ 70, 230],
                            [ 30, 160],
                            [150, 200] ])
imageHEnuance = unmixAndRecolor(Anuance, outputColors, image, verbose = False, method = "nnls")

if showPlots:
    plt.imshow(imageHEnuance, interpolation = "nearest")
    plt.title("HE Conversion - Unmix with spectra from Nuance")
    plt.xticks([]), plt.yticks([])
    plt.show()



# Method 1: Unmix and recolor using k-means cluster centers
model = KMeans(n_clusters=2, init='k-means++', n_init=10, max_iter=300, tol=0.0001, 
    precompute_distances='auto', verbose=0, random_state=None, copy_x=True, n_jobs=1)
model.fit(Y)
A = model.cluster_centers_.T

imageHEkmeans = unmixAndRecolor(A, outputColors, image, verbose = False, method = "nnls")
A[:,0], A[:,1] = A[:,1], A[:,0]
imageHEkmeansSwap = unmixAndRecolor(A, outputColors, image, verbose = False, method = "nnls")

if showPlots:
    plt.imshow(imageHEkmeans, interpolation = "nearest")
    plt.title("HE Conversion - Unmix with k-means")
    plt.xticks([]), plt.yticks([])
    plt.show()
    
    plt.imshow(imageHEkmeansSwap, interpolation = "nearest")
    plt.title("HE Conversion - Unmix with k-means (swapped columns)")
    plt.xticks([]), plt.yticks([])
    plt.show()
    

# Method 2: Unmix and recolor using k-means cluster centers on reduced image
threshold = 200
Ysum = np.sum(Y,1)
Y = Y[Ysum > threshold,:]
model.fit(Y)
A = model.cluster_centers_.T

imageHEkmeans = unmixAndRecolor(A, outputColors, image, verbose = False, method = "nnls")
A[:,0], A[:,1] = A[:,1], A[:,0]
imageHEkmeansSwap = unmixAndRecolor(A, outputColors, image, verbose = False, method = "nnls")

if showPlots:
    plt.imshow(imageHEkmeans, interpolation = "nearest")
    plt.title("HE Conversion - Unmix with reduced dataset k-means")
    plt.xticks([]), plt.yticks([])
    plt.show()
    
    plt.imshow(imageHEkmeansSwap, interpolation = "nearest")
    plt.title("HE Conversion - Unmix with reduced dataset k-means (swapped columns)")
    plt.xticks([]), plt.yticks([])
    plt.show()

exit()


# Normalize columns, first eliminate all zeros, then normalize. 
# Could also eliminate columns that are low energy, say sum less than 20
Ysum = np.sum(Y,1)
print("Ysum.shape")
print(Ysum.shape)

threshold = 40
Y = Y[Ysum > threshold,:]
Y = Y.astype(float)

print("Y.shape")
print(Y.shape)


Ysum = np.sum(Y,1)

for color in range(3):
    Y[:,color] = Y[:,color]/Ysum


print(Y.shape)
model.fit(Y)
Anorm = model.cluster_centers_.T
print(255*Anorm)



# Normalize columns    
A[:,0] = A[:,0]/np.sum(A[:,0])
A[:,1] = A[:,1]/np.sum(A[:,1])    

# If we assume that bluest spectra contains the nuclei, put in first column
if A[2,1] > A[2,0]:
    A[:,0], A[:,1] = A[:,1], A[:,0]



imageHE = unmixAndRecolor(255*A, outputColors, image,verbose=False,method='nnls')

# Normalize columns    
Anorm[:,0] = Anorm[:,0]/np.sum(Anorm[:,0])
Anorm[:,1] = Anorm[:,1]/np.sum(Anorm[:,1])    

# If we assume that bluest spectra contains the nuclei, put in first column
if Anorm[2,1] > Anorm[2,0]:
    Anorm[:,0], Anorm[:,1] = Anorm[:,1], Anorm[:,0]





imageHEnorm = unmixAndRecolor(255*Anorm, outputColors, image, verbose=False, method = "nnls")

if showPlots:        
        plt.imshow(image, interpolation = "nearest")
        plt.title("Original Image")
        plt.xticks([]), plt.yticks([])
        plt.show()

        plt.imshow(imageHE, interpolation = "nearest")
        plt.title("K-means HE Conversion")
        plt.xticks([]), plt.yticks([])
        plt.show()
        
        plt.imshow(imageHEnorm, interpolation = "nearest")
        plt.title("Normalized K-means HE Conversion")
        plt.xticks([]), plt.yticks([])
        plt.show()
        
