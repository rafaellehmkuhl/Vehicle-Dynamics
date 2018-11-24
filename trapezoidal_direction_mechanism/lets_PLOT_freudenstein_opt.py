from math import *
import numpy as np
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib import style

for i in range(1, 2):

    _radius = np.load('data/_radius_{}.npy'.format(i))
    _input = np.load('data/_input_{}.npy'.format(i))
    _ackerman = np.load('data/_ackerman_{}.npy'.format(i))
    _freudenstein = np.load('data/_freudenstein_{}.npy'.format(i))
    _error = np.load('data/_error_{}.npy'.format(i))
    _a = np.load('data/_a_{}.npy'.format(i))
    _b = np.load('data/_b_{}.npy'.format(i))
    _d = np.load('data/_d_{}.npy'.format(i))
    _beta = np.load('data/_beta_{}.npy'.format(i))
    _index = np.load('data/_index_{}.npy'.format(i))
    _big_error = np.load('data/_big_error_{}.npy'.format(i))

    fig = plt.figure()
    style.use('seaborn')

    plt.subplot(111)

    ackerman_plot, = plt.plot(np.degrees(_input), np.degrees(_radius))

    ackerman_plot.set_label('Ackerman')
    first_time = False

    freudenstein_plot, = plt.plot(np.degrees(_input), np.degrees(_freudenstein))
    # freudenstein_plot.set_label('β = {:.2f}'.format(degrees(beta)))

    # plt.subplot(312)
    # plt.ylim(0, 3*np.average(_big_error))
    # error_plot, = plt.plot(_index, _big_error, 'ro')

    # plt.subplot(313)
    # ax = fig.gca(projection='3d')
    # surf = ax.plot_surface(_a, _b, _d, linewidth=0, antialiased=False)

# plt.subplot(211)
# plt.title('Trapezoidal mechanism behaviour for variable β')
# plt.xlabel('Input angle - δi [deg]')
# plt.ylabel('Output angle - δo [deg]')
# plt.grid(True)

# plt.subplot(211)
plt.title('Input angle vs Radius')
plt.xlabel('Radius - R [m]')
plt.ylabel('Ackerman angle - δi [deg]')
plt.grid(True)

# plt.subplot(212)
# plt.title('Error over time')
# plt.xlabel('Cumulated error')
# plt.ylabel('Index')
# plt.grid(True)

# plt.subplots_adjust(hspace=0.6)
plt.show()

