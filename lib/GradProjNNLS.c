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