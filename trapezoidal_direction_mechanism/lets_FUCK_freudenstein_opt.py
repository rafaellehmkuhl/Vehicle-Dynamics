from math import *
import scipy.optimize as opt
from mpmath import cot, acot
import numpy as np

i = 0

def fuckin_freud(l, w, R, beta, dims):

    a, b, c, d = dims

    # print('a={}, b={}, c={} and d={}'.format(a, b, c, d))

    theta_input = float(atan(l/(R-w/2)))
    theta_output_ackerman = float(acot(cot(theta_input) + w/l))

    def freudenstein_eq(theta_input):

        theta_input_freud = (pi/2)-beta-theta_input

        J1 = d/a
        J2 = d/c
        J3 = (a**2 - b**2 + c**2 + d**2) / (2*a*c)

        A = J3 - J1 + (1-J2)*cos(theta_input_freud)
        B = -2*sin(theta_input_freud)
        C = J1 + J3 - (1+J2)*cos(theta_input_freud)

        theta_output_freud = float(2*atan((-B-sqrt(B**2-4*A*C))/(2*A)))

        return (pi/2)+beta-theta_output_freud

    theta_output_freud = freudenstein_eq(theta_input)
    error = (theta_output_freud-theta_output_ackerman)
    # print('Radius: {} / Ackerman: {:.5f} / Freudenstein: {:.5f} / Error: {:.5f}'.format(R, degrees(theta_output_ackerman), degrees(theta_output_freud), degrees(error)))

    return error, theta_input, theta_output_ackerman, theta_output_freud

def freud_opter(dims):

    global i
    i += 1

    a, beta, d = dims
    b = d-2*a*sin(beta)
    c = a

    l = 2.93
    w = 1.5

    _radius = []
    _input = []
    _ackerman = []
    _freudenstein = []
    _error = []

    _a = []
    _b = []
    _beta = []
    _d = []

    _index = []
    _big_error = []

    big_error = 0
    for radius in range(3, 201):
        error, theta_input, theta_output_ackerman, theta_output_freud = fuckin_freud(l, w, radius, beta, (a, b, c, d))

        _radius = np.append(_radius, radius)
        _input = np.append(_input, theta_input)
        _ackerman = np.append(_ackerman, theta_output_ackerman)
        _freudenstein = np.append(_freudenstein, theta_output_freud)
        _error = np.append(_error, error)

        _a = np.append(_a, a)
        _b = np.append(_b, b)
        _d = np.append(_d, d)
        _beta = np.append(_beta, beta)

        big_error = big_error + (error)**2

    print('For a={:.7f}, b={:.7f}, c={:.7f} and d={:.7f}, beta={:.7f}, error={:.5f}.'.format(a, b, c, d, beta, big_error))

    _index = np.append(_index, i)
    _big_error = np.append(_big_error, big_error)

    np.save('data/_radius_{}'.format(i), _radius)
    np.save('data/_input_{}'.format(i), _input)
    np.save('data/_ackerman_{}'.format(i), _ackerman)
    np.save('data/_freudenstein_{}'.format(i), _freudenstein)
    np.save('data/_error_{}'.format(i), _error)
    np.save('data/_a_{}'.format(i), _a)
    np.save('data/_b_{}'.format(i), _b)
    np.save('data/_d_{}'.format(i), _d)
    np.save('data/_beta_{}'.format(i), _beta)
    np.save('data/_index_{}'.format(i), _index)
    np.save('data/_big_error_{}'.format(i), _big_error)

    return big_error

a = 0.11
beta = 0.174
d = 1.45

bnds = ((0.1, 0.3), (0.05, 0.5), (1.3, 1.5))

res = opt.minimize(freud_opter, (a, beta, d), bounds=bnds, method='SLSQP')


