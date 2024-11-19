## simul_demo


This scripts illustrates the work of the function **fast_inverse_mod()**
with simulated data.

There are two files with simulated data in this folder: **measurements_fft.npy** and **measurements_fdiff.npy**

The former file with data have been simulated using the image contained in
the file **ground_truth.npy** with the help of a spectral FFT solver.
The second data file was obtained using a finite-difference solver, based
on the same initial data. We used the second order accurate leap-frog scheme.

The parameters of the domain imitate the realistic scenario similar
to the real mouse measurements presented elsewhere in this project.

The radius of the domain is 40.5 mm and the speed of sound
is 1515 meters per second.

The signal is modeled as being sampled at the rate of 40 million
samples per second. Total number of time samples is 3073.

The number of simulated detectors is 512; they are uniformly
spread over a unit circle.

Parameter **lhalf** is set to 0, so no additional correction
is done.

The resulting images are  stored in the files **reconstruction_fft.npy**
and **reconstruction_fdiff.npy**

If everything is working properly, the image reconstructed from the
spectral FFT data is very close to the ground truth, with L2 relative
error being under 9.8%.

The image reconsrtucted from finite difference data has noticeable
artifacts, consistent with the lower accuracy of the second order
finite difference scheme used to model the forward problem.





