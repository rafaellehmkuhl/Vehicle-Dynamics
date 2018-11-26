from math import *
import scipy.optimize as opt
from mpmath import cot, acot
import numpy as np
import pandas as pd

df = pd.DataFrame()

_index = []
_radius = []
_input = []
_ackerman = []
_freudenstein = []
_error = []
_a = []
_b = []
_beta = []
_d = []
_big_error = []

i = 0

def fuckin_freud(l, w, R, beta, dims):

    a, b, c, d = dims

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

    return error, theta_input, theta_output_ackerman, theta_output_freud

def freud_opter(dims):

    global _index
    global _radius
    global _input
    global _ackerman
    global _freudenstein
    global _error
    global _a
    global _b
    global _beta
    global _d
    global _big_error

    global i
    i += 1

    a, beta, d = dims
    b = d-2*a*sin(beta)
    c = a

    l = 2.93
    w = 1.5

    _radius_inst = []
    _input_inst = []
    _ackerman_inst = []
    _freudenstein_inst = []
    _error_inst = []

    big_error = 0
    for radius in range(3, 201):
        error, theta_input, theta_output_ackerman, theta_output_freud = fuckin_freud(l, w, radius, beta, (a, b, c, d))

        _radius_inst.append(radius)
        _input_inst.append(theta_input)
        _ackerman_inst.append(theta_output_ackerman)
        _freudenstein_inst.append(theta_output_freud)
        _error_inst.append(error)

        big_error = big_error + (error)**2

    print('For a={:.7f}, b={:.7f}, c={:.7f} and d={:.7f}, beta={:.7f}, error={:.5f}.'.format(a, b, c, d, beta, big_error))

    _radius.append(_radius_inst)
    _input.append(_input_inst)
    _ackerman.append(_ackerman_inst)
    _freudenstein.append(_freudenstein_inst)
    _error.append(_error_inst)

    _a.append(a)
    _b.append(b)
    _d.append(d)
    _beta.append(beta)

    _index.append(i)
    _big_error.append(big_error)

    return big_error

a = 0.20
beta = 0.43
d = 1.45

bnds = ((0.05, 0.3), (0.05, 0.5), (1.3, 1.5))

res = opt.minimize(freud_opter, (a, beta, d), bounds=bnds, method='SLSQP')
