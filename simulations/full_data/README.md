## Mouse_demo


This scripts illustrates the work of the function **fast_inverse_mod()**

The data is read from the file **mouse_data_real.npy**

These data have been acquired by a photoacoustic scanner MSOT inVision-256TF,
scanning a section of a live mouse. Data courtesy of Cancer Research UK Cambridge Institute.


The scanner has 256 detectors uniformly spread over 270 degrees arc of
a circle of radius 40.5 mm.  In order to supply a full circle of detectors
required by the algorithm, the data are zero-paded by additional zero-value
"detectors" to the total number of 340 detectors. Additionaly, the detectors
are rotated, so that the "zero" gap is centered on the left of the
reconstruction domain (i.e. at 9pm). This allows for image correction
with **lhalf** = 4.


The total acquisition time is shorter than ideal. When rescaled
to the problem with sound speed one on a unit circle, the rescaled
time interval is 1.91. Ideally it should be greater than 2.
This leads to circular artifacts on the periphery of the reconstructed
*(759 x 759)* image. However, since it is apriory knownthat the mouse occupies
only the center of the image, a smaller sub-image of size *(300 x 300)*
is extracted and used.

In this demo, the **fast_inverse_mod()** is called three times
with the same data, for timing purposes. During the first call,
a global variable **hankels** is pre-computed, containing a set of
values of Hankel functions. On the two consecutive runs,
the module re-uses the previously computed values, which results
in faster computation times.





