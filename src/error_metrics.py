import numpy as np

def relative_l2_error(true, pred):
    return np.linalg.norm(true - pred, axis=0) / np.linalg.norm(true, axis=0)

def absolute_l2_error(true, pred):
    return np.linalg.norm(true - pred, axis=0)