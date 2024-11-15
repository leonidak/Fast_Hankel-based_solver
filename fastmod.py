import sys
import numpy as np
import scipy as sp
import math
import time
from utils import t6hat, sin6hat

# --------- define polar coordinate transformation, readgeom, readinverse and prepare_hankels routines

def cart_to_polar_coor(xx,yy):               # ------------------------- begin cart_to_polar
# =============================
   rad = np.sqrt( xx*xx + yy*yy  )
   angle = np.arccos(xx/(rad+1.e-300))
   angle[yy < 0.] = 2.* math.pi - angle[yy < 0.]

   return rad, angle                          # ------------------------- end cart_to_polar


def prepare_hankels(ndet,numfreq,freq_rad):     # ---------------------- begin prepare_hankels
# ==========================================
   global hankels

   if('hankels' in globals()):
       print('hankels have been precomputed previously')
   else:
       print('precomputing hankels')
       midk = round(ndet/2)


       ind_grid  = np.array(range(midk))

       indices, frequencies = np.meshgrid( ind_grid, freq_rad  )

       hank_temp = sp.special.hankel1(indices, frequencies)*frequencies

       large_number = 1.e+30

       hank_temp[ np.isnan(hank_temp)] = large_number
       hank_temp[ abs(hank_temp) > large_number ] = large_number

       hank_flip = hank_temp[:, ::-1 ]


       hankels = np.zeros((numfreq,ndet), dtype='complex')

       hankels[1:, midk: ]  = np.copy(hank_temp)
       hankels[1:, 1:midk] = np.copy(hank_flip[:,0:midk-1])

       hankels[0,:]  =   large_number
       hankels[:,0] = large_number

   #return hankels                                # --------------------- end prepare hankels


def find_good_ntimes(ngood):

   numint = np.array(range(18))
   num2pow = 16*(2**numint)
   num2pow3 = num2pow*3//2

   index = 1 + np.array(range(18))
   goodnumbers = np.insert(num2pow, index, num2pow3)

   for j in goodnumbers:
       if j > ngood:
          break

   newtimes = j+1

   return newtimes

def fast_inverse_mod(data,ndet,ntimes,detector_radius,t_measured,speed_of_sound,ndim,lhalf,rad_corr):      # ================= T H I S    I S    T H E    M A I N     F U N C T I O N  ======================
# ====================================================================================================        --------------------------------------------------------------------------------------------------
    global hankels

    start_time = time.time()

    if(ndim % 2 == 0):
       print('ndim = ', ndim,' We want an odd ndim !')
       exit()


    tmax = t_measured/detector_radius*speed_of_sound          #  this is Tmax scaled to a problem with R = 1, speed_of_sound = 1
    tstep = tmax / (ntimes - 1)

    ngood = 3.1 / tstep +1

    newtimes = find_good_ntimes(ngood)

    tmax = (newtimes-1) * tstep

    print('--------- newtimes = ',newtimes,'  new tmax = ',tmax)

    datanew = np.zeros((newtimes,ndet))

    if(newtimes > ntimes):
        datanew[0:ntimes, :] = np.copy(data)
    else:
        if(newtimes < ntimes):
           datanew = np.copy(data[0:newtimes,:])
        else:
           datanew = data


    data = datanew
    ntimes = newtimes

    halfsize = 1.0                     #------------- reconstructed image geometry
    med = round((ndim+1))

    spatial_freq_step = 2.0*math.pi/(2.*halfsize)             #------- image 2D Fourier transform geometry
    spatial_freq_max =  spatial_freq_step * (ndim-1)/2


    det_angle_ext = np.linspace(0.,2*math.pi,ndet+1)    #---------- detector geometry
    det_angle = np.copy(det_angle_ext[0:ndet])


    times = np.linspace(0.,tmax,ntimes)            #-------------- time grid
    #tstep = times[1]-times[0]

    nfft_points = ntimes -1                        #------------- time Fourier transform geometry
    print('nfft_points = ',nfft_points)
    freqstep = 2.0*math.pi/tmax
    ldrad = nfft_points
    numfreq = round(nfft_points/2)
    time_freq_scale = freqstep*np.array(range(numfreq))

    freq_rad  = time_freq_scale[1:]        # intentionally skiping zero frequency



    # ----------------------- make a smooth cut of the input data ------------------------
    #tcut = 0.9*tmax
    #hat = t6hat(tmax/l,tcut/l,times)
    #hat = hat[0:nfft_points]

    cdata = np.zeros((nfft_points, ndet), dtype='complex')

    for j in range(ndet):
       cdata[:,j] = np.copy(data[0:nfft_points,j]) #*hat

    print(np.shape(cdata))
    # -------------------------- prepare Hankel functions -------------------------------------

    prepare_hankels(ndet,numfreq,freq_rad)

    hankel_time = time.time()
    print('Preparing Hankel functions','{:05.2f}'.format(hankel_time - start_time),' sec')

    # ----------------------- fft in time and in angle ----

    ctemp_fourier =  sp.fft.fftshift( sp.fft.ifft2(cdata), [1])
    cfourier = ctemp_fourier[0:numfreq]

    time_fft = time.time()
    print('FFT data in time and angle  ','{:05.2f}'.format(time_fft - hankel_time),' sec')

    # --------------------------- multiplying by (-i)^k ---------------------------------------
    midk = round(ndet/2)

    for kk in range(ndet):
       k = abs(kk-midk)
       coef = ( -1j )**k
       cfourier[:,kk] = cfourier[:,kk]/coef    # divide or multiply ?


    # ----------------------------- divide Fourier transform by Hankels --------------------------------

    cfourier_new = cfourier/hankels

    # ------------------------------------ Finding the DC number by integrating the zero harmonics -----

    czero_harm = np.copy(cfourier_new[:,midk])

    j1 =  np.real(hankels[:,midk+1])
    csum = np.sum(czero_harm[1:]*j1[1:]/freq_rad)*freqstep  # *2/math.pi

    # ----------------------------- inverse Fourier transform in angle ---------------------------------

    ctran =  sp.fft.fft(   sp.fft.fftshift( cfourier_new, [1]),axis = 1)

    ctran[0,:] = np.real(csum)           #---- using the DC number computed above

    time_fft = time.time()
    print('Inverse Fourier in angle','{:05.2f}'.format(time_fft - hankel_time ),' sec')

    # ------------------------ interpolate from the polar grid to Cartesian in the Fourier domain ------


    freq_scale =  np.linspace(-spatial_freq_max,spatial_freq_max,ndim)
    ksi1, ksi2 = np.meshgrid(freq_scale,freq_scale)


    freq_rho,freq_teta = cart_to_polar_coor(ksi1,ksi2)

    ctran_ext = np.zeros((numfreq,ndet+1), dtype= 'complex')
    ctran_ext[:,0:ndet] = np.copy(ctran)
    ctran_ext[:,ndet] = np.copy(ctran_ext[:,0])


    start_spline_time = time.time()

    interp_spline_r = sp.interpolate.RectBivariateSpline(time_freq_scale,det_angle_ext,np.real(ctran_ext),kx=3,ky=3)
    interp_spline_i = sp.interpolate.RectBivariateSpline(time_freq_scale,det_angle_ext,np.imag(ctran_ext),kx=3,ky=3)

    cart_transform = interp_spline_r.ev(freq_rho,freq_teta) + 1j * interp_spline_i.ev(freq_rho,freq_teta)

    spline_time = time.time()

    print('Interpolation to Cartesian grid ','{:05.2f}'.format(spline_time - start_spline_time),' sec')
    # ------------------------- cut off redundant frequencies -------------------------------------------
    if(lhalf == 1):
       mcenter = round((ndim-1)/2)
       cart_transform[0:mcenter,:] = np.conj(np.copy(np.flip(cart_transform[mcenter+1:,:],[0,1])))
    if(lhalf == 2):
       mcenter = round((ndim-1)/2)
       cart_transform[mcenter+1:,:] = np.conj(np.copy(np.flip(cart_transform[
    0:mcenter,:],[0,1])))


    # ------------------------- inverse 2D Fourier transform to obtain the image ------------------------
    coefficient = tmax  # ------ why?

    image =  coefficient* np.real( sp.fft.fftshift( sp.fft.fft2(   sp.fft.fftshift( cart_transform[0:ndim-1,0:ndim-1], [0,1])), [0,1] )   )
    image_ext = np.zeros((ndim,ndim))
    image_ext[0:ndim-1,0:ndim-1] = image

    fft_time = time.time()

    print('2D inverse FFT ','{:05.2f}'.format(fft_time - spline_time),' sec')

    # -------------------------- additional correction for zero boundary conditions ----------------------

    xx = np.linspace(-halfsize,halfsize,ndim)
    xstep = xx[1]-xx[0]
    xxx,yyy = np.meshgrid(xx,xx)
    rad = np.sqrt(xxx*xxx+yyy*yyy)

    if(rad_corr <= 1. and rad_corr > 0.):
       aaa = np.zeros((ndim,ndim))
       aaa[rad > rad_corr - 2.*xstep] = 1.
       aaa[rad > rad_corr] = 0.

       number_of_pixels = np.sum(aaa)
       average  = np.sum(aaa*image_ext)/number_of_pixels

       image_ext = image_ext - average
       print('average = ', average)


    image_ext[rad >= 1.] = 0.      # set to 0 outside of the unit circle

    # -------------------------------- done --------------------------------------------------------------

    final_time = time.time()

    print('Total time ','{:05.2f}'.format(final_time - start_time),' sec')

    return image_ext


if __name__ == "__main__":
    print('Stop this!')
    print('This is a subroutine, not the main program!')




