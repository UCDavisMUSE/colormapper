import pyopencl as cl
import os
import numpy as np

def OpenCLGradProjNNLS(image, A, tolerance = 1e-4, maxiter = 100, context = 0):
    # Create a compute context and define a command cue
    # I wish I could change this to 1 on the iMac (although it seems there's a bug).
    os.environ["PYOPENCL_CTX"] = str(context) 
    os.environ["PYOPENCL_COMPILER_OUTPUT"] = "0" # Suppress output
    ctx = cl.create_some_context()
    queue = cl.CommandQueue(ctx)

    # Define the OpenCL program
    f = open('GradProjNNLS.c','r')
    fstr = "".join(f.readlines())
    prg = cl.Program(ctx, fstr).build()

    # Things to precompute:
    ATA = np.dot(A.T,A)
    pinvA = np.linalg.pinv(A)
    alpha = np.linalg.norm(ATA,ord=2)

    # Copy items from host memory to graphics memory
    mf = cl.mem_flags
    image_g     = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = np.float64(image))
    A_g         = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = np.float64(A))
    ATA_g       = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = np.float64(ATA))
    pinvA_g     = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf = np.float64(pinvA))

    # Create a buffer for the result in the graphics memory
    X_unmixOpenCLGradProjNNLS = np.zeros((image.shape[0], image.shape[1], A.shape[1]),dtype = np.float64)
    X_unmixOpenCLGradProjNNLS_g = cl.Buffer(ctx, mf.WRITE_ONLY, X_unmixOpenCLGradProjNNLS.nbytes)

    # Execute the program, not sure what the 2nd and 3rd args are, but last 3 are the args of the program
    gsize = (image.shape[0],image.shape[1])
    lsize = (1,1)

    prg.GradProjNNLS(queue, gsize, lsize, image_g, A_g, ATA_g, pinvA_g,
                    np.int32(image.shape[0]), np.int32(image.shape[1]), np.int32(image.shape[2]),
                    np.int32(A.shape[1]), np.float64(tolerance), np.int32(maxiter), np.float64(alpha),
                    X_unmixOpenCLGradProjNNLS_g)

    # Copy from graphics memory to host memory
    cl.enqueue_copy(queue, X_unmixOpenCLGradProjNNLS, X_unmixOpenCLGradProjNNLS_g)
    
    return X_unmixOpenCLGradProjNNLS



    

