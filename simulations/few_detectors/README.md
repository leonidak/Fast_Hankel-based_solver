## simul_demo


This scripts illustrates the work of the function **fast_inverse_mod()**
with simulated data.

The data is read from the file **measurements_few.npy**

These data have been simulated, using the image contained in
the file **ground_truth.npy** using a spectral FFT solver.

The radius of the domain and the speed of sound are both 1.

The simulated measurements run for 6 units of time.

The number of simulated detectors is 64; they are uniformly
spread over a unit circle. Such number of detectors is suboptimal
(too few). This results in noticeable artifacts in the reconstructed image.

Parameter **lhalf** is set to 0, so no additional correction
is done.

The resulting image is stored in the file **reconstruction.npy**

If everything is working properly, the maximum difference between
the images in **reconstruction.npy** and **ground_truth.npy**
should be about 14% in the relative *L_2* norm



