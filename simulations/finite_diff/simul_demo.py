#----------------------------------------
# This is a demo file illustrating the use of the "fast inverse" module
# in simulations
#
#-----------------------------------------------------------------------------------------------
import sys
sys.path.append("../")
import numpy as np
from utils import npyread
from fastmod import fast_inverse_mod


#-----------------------------------------------------------------------------------------------------
# Main program starts here
#-----------------------------------------------------------------------------------------------------


print(' ')
print('**********')
print('Simul demo')
print('**********')
print(' ')

#---- data parameters:

detector_radius = 0.0405    # in meters
speed_of_sound  = 1515.      # meters per second
sampling_rate   = 40000000.     # samples per second
nsamples        = 3073
ndet      = 512      # in this examples there are 512 spaced over 360 degrees.

ndim = 257                  # desired grid size for the reconstructed image. Should be an odd number!
lhalf = 0                   # additional filtration to correct for absent detectors on the left

rad_corr = 1.0

print('rad_corr=',rad_corr)

time_step =      1./sampling_rate              # time step of measurements
t_measured      = time_step*(nsamples-1)        # this is total measurement time
print('t_measured = ',t_measured)


#----------------------------------------------- read the data
namedata = 'measurements_fdiff.npy'
data = npyread(namedata)
(nrow,ncol) = np.shape(data)

print(nrow,ncol)


if (nrow != nsamples):
    print('Wrong times !')
    quit()

if (ncol != ndet):
    print('Wrong number of detectors !')
    quit()

#--------------------------- call the module to reconstruct the image from the finite differences solver data ---------------

image = fast_inverse_mod(data,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('reconstruction_fdiff.npy',image)


#----------------------------------------------- read the data
namedata = 'measurements_fft.npy'
data = npyread(namedata)
(nrow,ncol) = np.shape(data)

print(nrow,ncol)


if (nrow != nsamples):
    print('Wrong times !')
    quit()

if (ncol != ndet):
    print('Wrong number of detectors !')
    quit()

#--------------------------- call the module to reconstruct the image from the spectral solver data ---------------

image = fast_inverse_mod(data,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('reconstruction_fft.npy',image)



quit()

