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
#     f = open('GradProjNNLS.c','r')
#     fstr = "".join(f.readlines())
#     prg = cl.Program(ctx, fstr).build()
    prg = cl.Program(ctx, 
    """
    __kernel void GradProjNNLS( __global const double *image, __global const double *A,
                                __global const double *ATA, __global const double *pinvA,
                                long n1, long n2, long n3, long k, 
                                double tolerance, long maxiter, double alpha,
                                __global double *X) {
    int i = get_global_id(0);
    int j = get_global_id(1);

    // Declare aux variables
    double ATimage[k];
    double grad[k];
    double gradthresh[k];
    double gap = 0.0;
    long iter = 0;


    // Pre-compute ATimage
    for (int component = 0; component < k; ++component)
    {
        ATimage[component] = 0.0;
        for (int wavelength = 0; wavelength < n3; ++wavelength)
        {
            ATimage[component] += A[k*wavelength + component]*image[n2*n3*i + n3*j + wavelength];
        }
    }

    // Initialize with thresholded pseudo-inverse (if nonnegative, this is optimal)
    for (int component = 0; component < k; ++component)
    {
        X[n2*k*i + k*j + component] = 0.0;
        for (int wavelength = 0; wavelength < n3; ++wavelength)
        {
            X[n2*k*i + k*j + component] += pinvA[n3*component + wavelength]*image[n2*n3*i + n3*j + wavelength];
        }
        if (X[n2*k*i + k*j + component] < 0.0)
        {
            X[n2*k*i + k*j + component] = 0.0;
        }
    }

    // Compute gradient, check if convergence criterion is satisfied
    for (int component = 0; component < k; ++component)
    {
        grad[component] = 0.0;
        for (int component2 = 0; component2 < k; ++component2)
        {
            grad[component] += ATA[k*component + component2]*X[n2*k*i + k*j + component2];
        }
        grad[component] -= ATimage[component];

        if (grad[component] < 0.0)
        {
            gradthresh[component] = 0.0;
        }
        else
        {
            gradthresh[component] = grad[component];
        }
    }

    // See if meets convergence criterion (duality gap)
    for (int component = 0; component < k; ++component)
    {
        gap += gradthresh[component]*X[n2*k*i + k*j + component];
    }

    // Main algorithm loop
    while (gap > k*tolerance && iter < maxiter)
    {
        iter += 1;

        // Gradient Projection
        for (int component = 0; component < k; ++component)
        {
            // Gradient Step
            X[n2*k*i + k*j + component] -= grad[component]/alpha;
            // Project
            if (X[n2*k*i + k*j + component] < 0.0)
            {
                X[n2*k*i + k*j + component] = 0.0;
            }        
        }

        // Compute Gradient
        for (int component = 0; component < k; ++component)
        {
            grad[component] = 0.0;
            for (int component2 = 0; component2 < k; ++component2)
            {
                grad[component] += ATA[k*component + component2]*X[n2*k*i + k*j + component2];
            }
            grad[component] -= ATimage[component];

            if (grad[component] < 0.0)
            {
                gradthresh[component] = 0.0;
            }
            else
            {
                gradthresh[component] = grad[component];
            }
        }

        // See if meets convergence criterion (duality gap)
        gap = 0.0;
        for (int component = 0; component < k; ++component)
        {
            gap += gradthresh[component]*X[n2*k*i + k*j + component];
        }
    }
    }
    """).build()

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



    

