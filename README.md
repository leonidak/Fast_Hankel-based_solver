# Module fastmod


This module reconstructs an image from thermoacoustic or
photoacoustic data given on a time/space cylinder. The
algorithm is fast; it takes, roughly speaking,  *O(n^2 log n)* flops for *( O(n)
x O(n))* data and *(n x n)* image.

The program implements both a traditional reconstruction, and the
microlocally accurate partial data reconstruction
( see   *M. Eller, P. Hoskins, and L. Kunyansky,*  Microlocally accurate solution of the inverse source problem of thermoacoustic tomography, *Inverse Problems* **36(8)**, 2020, 094004 )

-----------------------------------------------------------------------------

The module is called as follows:

### image = fast_inverse_mod(data, ndet, ntimes, detector_radius, t_measured, speed_of_sound, ndim, lhalf, rad_corr)

Parameters:

**data      : numpy.array**

This is input data, representing the trace of the solution of the wave
equation on a circle of radius **detector_radius**. The number of columns
corresponds to the number of the detectors **ndet**. Detectors are assumed
to be uniformly spaced over the circle. Detectors are numbered counter-
clockwise, with the first detector located at (1,0) (i.e. 3 pm position).
Each column represents a time series, with the first data correspondin
to *t=0*, and the last to *t=* **t_measured**. The time discretization is uniform.

**ndet     : int**

number of detectors and of the columns in data. If data only known on
a subset of a circle, zero data detectors should be added so that
detectors cover the circle uniformly.

**ntimes   : int**

number of time samples, the first at *t=0*, the last at *t=* **t_measured**

**detector_radius : float**

radius of the circles with the detectors

**t_measured :  float**

time interval where data are known; it is equal to *(* **ntimes** *-1) x* time step.

**speed_of_sound : float**

self-explanatory

**ndim : int, odd number!**

the image will be reconstructed on a square grid of size ndim x ndim,
corresponding to square *[-R,R]x[-R,R]*, where *R=* **detector_radius**.
Parameter **ndim** SHOULD BE ODD. This way there is a pixel at the position (0,0),
which is convenient. All the pixels outside of the circle of radius *R*
are set to 0.

**lhalf : int**, acceptable values: {0,1,2,3,4}

if all detectors on a circle are active (data is known), **lhalf** should be 0.
If a subset of detectors is absent (set to 0), one can invoke an
additional correction. An interesting property of the present algorithm is
that, when some detectors are missing, the corresponding error mostly
concentrates in a corresponding sector of the Fourier transform of the
reconstructed image. However, since the image is real-valued, there is a
redundancy in the Fourier transform. Non-zero lhalf eliminates one half of
the Fourier transform, and replaces it by the rotated and
complex-conjugated copy of the other half. This significantly reduces
the reconstruction error, if the total measurement scheme satisfies the
visibility condition (see
*M. Eller, P. Hoskins, and L. Kunyansky*,
Microlocally accurate solution of the inverse source problem
of thermoacoustic tomography, *Inverse Problems* **36(8)**, 2020, 094004)

The values of **lhalf** {1,2,3,4} determine which half is eliminated.
The easiest way to choose **lhalf** is to experiment.

**rad_corr : float**

a property of the algorithm is that the constant component of the
image may contain a noticeable error (depending on discretization
parameter). In order to correct that, the module will add or subtract a
constant in such a way that the average of the reconstructed image in a
narrow ring of relative radius **rad_corr** is equal to 0.
For example, if it is known that the correct image should vanish close to
the detectors' cicrcle, **rad_corr** should be set to 1.
If **rad_corr** is greater than 1 or less than 0, no constant will be
added.

### Output:

numpy.ndarray of size *(* **ndim** *x* **ndim** *)* representing the image
reconstructed within the circle of radius **detector_radius**.


### Recommended values:

*(* **ndim** *-1)* and **ndet** should ideally be FFT-friendly numbers, i.e., integers
that can be factoedr in small primes, i.e. 2^k^ or 3 x 2^k^, etc.
The value *t_rescaled* = **t_measured/detector_radius x speed_of_sound**
ideally should be greater than 2. Larger values can increase the accuracy
of lower spatial frequences in the image, if data are accurate. If data are
noisy, longer measurement time does not help much.
If *t_rescaled* is less than 2, there may be striking circular artifacts in
the image...

### Peculiarities of implementation

Inside the module, array **hankels** is defined as a global variable.
The first time the module is called, it precomputes **hankels** and does
the image reconstruction. On consecutive runs, the previously computed
version of **hankels** is used, which speeds up the computation.
However, if on a consecutive run the geometry of the problem is changed,
the computation will not be correct. So, calling the module within the same
script with different geometry parameters is disallowed.


### Examples

There are several examples of the use of the module, presented in the
subfolders.

Subfolder \simulations has five subfolders with reconstructions from simulated
data. See README files in these subfolders.

Subfolder \mouse contains an image reconstruction from real data courtesy
of CRUK (thanks to Janek Grohl). The data corresponds to a section of a mouse
body. See README in that folder for the details.



