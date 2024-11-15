#----------------------------------------
#  This is a demo file illustrating the use of the "fast inverse" module
#   for reconstructing an image from a real mouse scan
#
#-----------------------------------------------------------------------------------------------
import sys
sys.path.append("..")
import numpy as np
from utils import npyread
from fastmod import fast_inverse_mod


#-----------------------------------------------------------------------------------------------------
#  Main program starts here
#-----------------------------------------------------------------------------------------------------


print(' ')
print('**********')
print('Mouse demo')
print('**********')
print(' ')

#---- data parameters:

detector_radius = 0.0405    # in meters
speed_of_sound  = 1535      # meters per second
sampling_rate   = 4.e+7     # samples per second
nsamples        = 2030
ndet_exist      = 256       # in this examples there are 256 detectors spaced over 270 degrees. Will need to add more zero detectors to cover  360 degrees.

namedata  ='mouse_data_real.npy'   # file with the data

ndim = 759                  # desired grid size for the reconstructed image. Should be an odd number!
ndimsmall = 300             # extract a smaller (but concentric) image
lhalf = 4                   # additional filtration to correct for absent detectors on the left

rad_corr = ndimsmall/ndim

print('rad_corr=',rad_corr)

time_step = 1./sampling_rate              # time step of measurements
t_measured      = time_step*(nsamples-1)        # this is total measurement time

t_rescaled = t_measured/detector_radius*speed_of_sound  #


print (' t_rescaled = ',t_rescaled, t_rescaled*3073/2030)

#----------------------------------------------- read the mouse data and transpose the matrix
data = npyread(namedata)

(nrow,ncol) = np.shape(data)

#print(ncol,nrow)


if (nrow != nsamples):
    print('Wrong times !')
    quit()

if (ncol != ndet_exist):
    print('Wrong number of detectors !')
    quit()

#---------------------------------------------- introduce new "zero" detectors to cover the whole circle


det_step =  270./(ndet_exist-1)
ndet = round(360./det_step)
print('ndet = ',ndet)
added = ndet -ndet_exist                      # this is how many fake detectors one need to add to cover the whole circle
print('added det positions = ',added)

datanew = np.zeros((nsamples,ndet))
datanew[:,:ndet_exist] = np.copy(data)

datanew = np.roll(np.copy(datanew),-round(added/2) -85,1)    # detectors are rotated so that "the gap" is on the left

np.save('mouse_data_modified.npy',datanew)   # just for debugging purposes
#--------------------------------------------------------------------------------------------------

ioffset = round((ndim-ndimsmall)/2)


#--------------------------- call the module  ---------------

print("----------------------------------------")
image = fast_inverse_mod(datanew,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('fast_inv1.npy',image)

imagesmall = np.copy(image[ioffset:ioffset+ndimsmall,ioffset:ioffset+ndimsmall])
np.save('fast_small_inv1.npy',imagesmall)



#--------------------------- call the module again ---------------
print("----------------------------------------")


image = fast_inverse_mod(datanew,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('fast_inv2.npy',image)

imagesmall = np.copy(image[ioffset:ioffset+ndimsmall,ioffset:ioffset+ndimsmall])
np.save('fast_small_inv2.npy',imagesmall)



#--------------------------- call the module again ---------------
print("----------------------------------------")


image = fast_inverse_mod(datanew,ndet,nsamples,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr)
np.save('fast_inv3.npy',image)

imagesmall = np.copy(image[ioffset:ioffset+ndimsmall,ioffset:ioffset+ndimsmall])
np.save('fast_small_inv3.npy',imagesmall)







quit()

