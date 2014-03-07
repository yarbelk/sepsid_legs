import numpy as np
import scipy
import parseEfd
import sys


def X_n(a, b, n, T):
    """
    For a given n, return X(t)
    """
    def X(t):
        return a * np.cos((np.pi * 2 * n * t) / T) + b * np.sin((np.pi * 2 * n * t) / T)
    return X


def XY(x, y):
    """
    :param x: list of all x points
    :param y: list of all y points
    :returns: list of (x,y) points
    """
    return map(lambda a, b: (a, b), x, y)


def main(coeficents, T=1000.0, dt=0.1):
    A = map(lambda x: x[0], coeficents)
    B = map(lambda x: x[1], coeficents)
    C = map(lambda x: x[2], coeficents)
    D = map(lambda x: x[3], coeficents)

    Xn_funcs = [X_n(A[n], B[n], n, T) for n in xrange(len(A))]
    Yn_funcs = [X_n(C[n], D[n], n, T) for n in xrange(len(A))]

    dts = [dt * k for k in xrange(int(T / dt))]

    X_vals = [sum([Xn(t) for Xn in Xn_funcs]) for t in dts]
    Y_vals = [sum([Yn(t) for Yn in Yn_funcs]) for t in dts]

    xy_vals = XY(X_vals, Y_vals)
    return xy_vals


if __name__ == "__main__":
    input_fft = parseEfd.split_on_names(sys.argv[1])
    from pprint import pprint
    pprint(main(input_fft))
