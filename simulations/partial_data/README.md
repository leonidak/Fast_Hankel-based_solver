## simul_demo


This scripts illustrates the work of the function **fast_inverse_mod()**
with simulated data.

The data is read from the file **partial_measmnts.npy**

These data have been simulated, using the image contained in
the file **ground_truth.npy** using a spectral FFT solver.

The radius of the domain and the speed of sound are both 1.

The simulated measurements run for 6 units of time.

The number of simulated detectors is 1024; they are uniformly
spread over a unit circle. However, the values over about
a quarter of a circle on the bottom a set to 0,
simulating an incomplete circle of the detectors.
The transition to 0 is made smooth.

There are two calls to the module **fast_inverse_mod()**

For the first call, parameter **lhalf** is set to 0, so no
additional correction is performed. The reconstructed image contains
strong artifacts. The resulting image is stored in the file
**reconstruction_no_correction.npy**



For the second call, parameter **lhalf** is set to 2,
thus removing one half of the Fourier transform of the image.
The resulting image is stored in the file
**reconstruction_with_corrections.npy**


If everything is working properly, the maximum difference between
the images in **reconstruction_with_corrections.npy** and **ground_truth.npy**
should be about 5% in the *L_2* norm



