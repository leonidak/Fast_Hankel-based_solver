import numpy as np


def npyread(fpath):

    data = np.load(fpath)
    arr = np.zeros((2, 2))

    if type(data) != type(arr):
        print(fpath+'is not a 2D array !')
        print('Shutting down !')

    return data
