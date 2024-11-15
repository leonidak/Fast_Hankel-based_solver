## simul_demo


This scripts illustrates the work of the function **fast_inverse_mod()**
with simulated data.

The data is read from the file **measurements_1_sec.npy**

These data have been simulated, using the image contained in
the file **ground_truth.npy** using a spectral FFT solver.

The radius of the domain and the speed of sound are both 1.

The simulated measurements run for one unit of time.
This is too short of a time. As a result, there is a very
large artifact at the center ofthe reconstructed image.

The number of simulated detectors is 512; they are uniformly
spread over a unit circle.

Parameter **lhalf** is set to 0, so no additional correction
is done.

The resulting image is stored in the file **reconstruction.npy**



