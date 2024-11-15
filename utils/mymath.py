import numpy as np
import math


def t6hat(rmax,rmin,x):

    xx = np.abs(x)
    ones = np.ones_like(xx)
    xmax = rmax*ones
    xmin = rmin*ones

    xx1 = np.minimum(xx,xmax)
    xx2 = np.maximum(xx1,xmin)
    xx3 = (ones - (xx2 - rmin)/(rmax-rmin))*math.pi
    xx4 = sin6hat(xx3)
    return xx4


def sin6hat(x):
    res = np.sin(6.0*x)/3.0 - 3.0*np.sin(4.0*x)   + 15.0*np.sin(2.0*x) - 20.0*x
    res = -res/(20.0*math.pi)
    return res
