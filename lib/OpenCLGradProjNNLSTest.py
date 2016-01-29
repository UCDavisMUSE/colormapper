if __name__ == "__main__":
    from nonnegativeLeastSquares import *
    from OpenCLGradProjNNLS import *
    import matplotlib.pyplot as plt
    
    # Perform Tests
    # Image is an n1 x n2 x 3 numpy array,
    # unmixing matrix A is 3 x k, where k is the number of components,
    # unmixed results should be n1 x n2 x k.
    
    showPlots = False
    tolerance = 1e-8
    maxiter = 100;
    
    # Example unmixing matrix
    A = np.array([ [ 228, 244],
                   [ 250, 205],
                   [ 166, 100] ])
    # Test image (Convert to RGB)
    image = cv2.imread("testImages/restored mouse liver-157151117-67.png")
    
     
    image = image[::1,::1,:]
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)
    
    print("For a " + str(image.shape[0]) + " by " + str(image.shape[1]) + " image:")
    if showPlots:
        plt.imshow(image, interpolation = "nearest")
        plt.xticks([]), plt.yticks([])
        plt.show()
    
    #   Method: unmixParallelTileGradProjNNLS
    start = time.time()
    X_unmixParallelTileGradProjNNLS = unmixParallelTileGradProjNNLS(image, A, tolerance = tolerance, maxiter = maxiter)
    end = time.time()
    print("unmixParallelTileGradProjNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixParallelTileGradProjNNLS.shape[0]) + " by " + 
        str(X_unmixParallelTileGradProjNNLS.shape[1]) + " by " + 
        str(X_unmixParallelTileGradProjNNLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixParallelTileGradProjNNLS.shape[2]):
            plt.imshow(X_unmixParallelTileGradProjNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()
            
    #   Method: unmixOpenCLGradProjNNLS
    start = time.time()
    X_unmixOpenCLGradProjNNLS = OpenCLGradProjNNLS(image, A, tolerance = tolerance, maxiter = maxiter, context = 1, lsize = (8,8))
    end = time.time()
    print("unmixOpenCLGradProjNNLS Time: " + str(end-start) + " seconds.")
    print("Result is an " + 
        str(X_unmixOpenCLGradProjNNLS.shape[0]) + " by " + 
        str(X_unmixOpenCLGradProjNNLS.shape[1]) + " by " + 
        str(X_unmixOpenCLGradProjNNLS.shape[2]) + " matrix.")
    if showPlots:
        for i in range(X_unmixOpenCLGradProjNNLS.shape[2]):
            plt.imshow(X_unmixOpenCLGradProjNNLS[:,:,i], interpolation = "nearest", cmap = plt.get_cmap("gray"))
            plt.xticks([]), plt.yticks([])
            plt.show()
            diff = X_unmixParallelTileGradProjNNLS[:,:,i] - X_unmixOpenCLGradProjNNLS[:,:,i]
            print('Max difference between Grad Proj NNLS and Open CL Grad Proj NNLS: %8.3e' % abs(diff).max())        
        



