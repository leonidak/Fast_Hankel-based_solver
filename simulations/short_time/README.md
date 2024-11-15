## simul_demo


This scripts illustrates the work of the function **fast_inverse_mod()**
with simulated data.

The data is read from the file **measurements_short.npy**

These data have been simulated, using the image contained in
the file **ground_truth.npy** using a spectral FFT solver.

The radius of the domain and the speed of sound are both 1.

The simulated measurements run for 1.5625 units of time.
This is too short of a time. As a result, there are visible
circular artifacts in the reconstructed image.

The number of simulated detectors is 512; they are uniformly
spread over a unit circle.

Parameter **lhalf** is set to 0, so no additional correction
is done.

The resulting image is stored in the file **reconstruction.npy**

If everything is working properly, the maximum difference between
the images in **reconstruction.npy** and **ground_truth.npy**
should be about 10% in the *L_2* norm



