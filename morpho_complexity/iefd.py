import numpy as np
import scipy


input_fft = output = (
    (1.0000000e+00,  1.4092754e-17, -5.8172750e-17,  2.1548833e-01),
    (1.0086234e-03, -8.3698195e-03, -2.0331539e-02,  4.0703919e-02),
    (9.9645218e-02,  4.3252546e-03,  2.0216971e-02,  4.6336544e-02),
    (-3.9631247e-03, -4.3050886e-03, -6.7965237e-03,  1.6009844e-02))

output = np.fft.ifft2(input_fft)


def X_t(A, B, t, T):
    """
    A is list of a_n coeficents
    B ``
    """

    def X_n(a_n, b_n, n):
        return a_n * np.cos((np.pi * 2 * n * t) / T) + b_n * np.sin((np.pi * 2 * n * t) / T)

    vX_n = np.vectorize(X_n)
    X_vals = vX_n(A, B, range(len(A)))
    return sum(X_vals)


def X(A, B, T, dT):
    return [X_t(A, B, dT*i, T) for i in xrange(int(T/dT))]


def Y_t(C, D, t, T):
    """
    C is list of c_n coeficents
    D ``
    """

    def Y_n(c_n, d_n, n):
        return c_n * np.cos((np.pi * 2 * n * t)/T) + d_n * np.sin((np.pi * 2 * n * t)/T)

    vY_n = np.vectorize(Y_n)
    Y_vals = vY_n(C, D, range(len(C)))
    return sum(Y_vals)


def Y(C, D, T, dT):
    return [Y_t(C, D, dT*i, T) for i in xrange(int(T/dT))]


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

    X_vals = X(A, B, T, dt)
    Y_vals = Y(C, D, T, dt)

    xy_vals = XY(X_vals, Y_vals)
    return xy_vals


if __name__ == "__main__":
    comp_in = map(lambda x: (x[0] + j*x[1], x[2] + j*x[3]), input_fft)
    coef = np.fft.ifft2(comp_in)
    coef_out = map(lambda x: (x[0].real + x[1], x[2] + j*x[3]), input_fft)

    from pprint import pprint
    pprint(main(coef))
