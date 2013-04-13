import numpy as np
import scipy

def chaincode_timestep(code):
    return (1 + (np.sqrt(2)-1)/2 * (1 - (-1)^ code))

vtime_steps = np.vectorize(chaincode_timestep)

def sgn(x):
    if x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return 1


def delta_x(code):
    return sgn(6- code)*sgn(2-code)

def delta_y(code):
    return sgn(4 -code) * sgn(code)

vdelta_x = np.vectorize(delta_x)
vdelta_y = np.vectorize(delta_y)


def get_x(delta_xs, p):
    return np.sum(delta_xs[:p])

def get_y(delta_ys, p):
    return np.sum(delta_ys[:p])


def get_timeseries(chaincode):
    time_steps = vtime_steps(chaincode)
    period = 1/np.sum(time_steps)
    delta_xs = vdelta_x(chaincode)
    delty_ys = vdelta_y(coaincode)
