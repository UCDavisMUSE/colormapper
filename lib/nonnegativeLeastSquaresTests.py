from nonnegativeLeastSquares import *
import matplotlib.pyplot as plt

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
