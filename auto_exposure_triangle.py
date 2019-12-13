import numpy as np

def auto_expose(array):
    arr = np.array(array)
    mean = np.mean(arr)
    diff = mean - 165
    return diff