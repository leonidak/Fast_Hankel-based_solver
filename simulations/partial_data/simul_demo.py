# ----------------------------------------
#  This is a demo file illustrating the use of the "fast inverse" module
#   for reconstructing an image from a real mouse scan
#
# -----------------------------------------------------------------------------------------------
import sys
sys.path.append("../../")
import numpy as np
from utils import npyread
from fastmod import fast_inverse_mod

# -----------------------------------------------------------------------------------------------------
#  Main program starts here
# -----------------------------------------------------------------------------------------------------

print(' ')
print('**********')
print('Simul demo')
print('**********')
print(' ')

# ---- data parameters:

detector_radius = 1.    # in meters
speed_of_sound  = 1.      # meters per second
sampling_rate   = 768./6.     # samples per second
nsamples        = 769
ndet      = 1024       # in this examples there are 256 detectors spaced over 270 degrees. Will need to add more zero detectors to cover  360 degrees.

namedata  ='partial_measmnts.npy'   # file with the data

ndim = 257                  # desired grid size for the reconstructed image. Should be an odd number!

rad_corr = 1.

print('rad_corr=',rad_corr)

time_step =      1./sampling_rate              # time step of measurements
t_measured      = time_step*(nsamples-1)        # this is total measurement time


# ----------------------------------------------- read the mouse data and transpose the matrix
data = npyread(namedata)
(nrow,ncol) = np.shape(data)

print(nrow,ncol)


if (nrow != nsamples):
    print('Wrong times !')
    quit()

if (ncol != ndet):
    print('Wrong number of detectors !')
    quit()

# --------------------------- call the module to reconstruct the image ---------------

lhalf = 0                   # additional filtration to correct for absent detectors on the left (0 = none)

image = fast_inverse_mod(data,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('reconstruction_no_correction.npy',image)

lhalf = 2                   # additional filtration to correct for absent detectors on the left (0 = none)

image = fast_inverse_mod(data,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('reconstruction_with_corrections.npy',image)

quit()
