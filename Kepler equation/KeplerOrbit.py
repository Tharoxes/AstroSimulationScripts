#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      10 October, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      2
   Thema:     Keplergleichung
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import animation
mpl.rcParams['animation.ffmpeg_path'] = r'C:\\Users\\tharo\\ffmpeg-2021\\bin\\ffmpeg.exe'


def kepler_equation(mean_anomaly, eccentric_anomaly, eccentricity):
    return mean_anomaly - eccentric_anomaly - eccentricity * np.sin(eccentric_anomaly)


def dkepler_equation(eccentric_anomaly, eccentricity):
    return 1 - eccentricity * np.cos(eccentric_anomaly)


def newton_method(func, dfunc, x, eccentricity, t, tol=1e-10, dmin=1e-12, maxN=50):
    if not isinstance(x, float):
        return None
    n = 0
    while n < maxN:
        dfx = dfunc(x, eccentricity)
        if dmin > dfx:
            AssertionError("Function is diverging.")
            return None
        else:
            x = x - func(x, t, eccentricity) / dfx
            if abs(func(x, t, eccentricity)) <= tol * x:
                # print(x % (np.tau))
                return x % (2 * np.pi)
            n += 1
    AssertionError("> maxN")
    print("> maxN")
    return None


def get_x_coord(eccentric_anomaly, a1):
    return a1 * np.cos(eccentric_anomaly)


def get_y_coord(eccentric_anomaly, a1, eccentricity):
    return a1 * np.power(1 - np.power(eccentricity, 2), 0.5) * np.sin(eccentric_anomaly)


def mean_anomaly(times, period):
    return (2 * np.pi / period) * times


def get_a_from_T(period):
    return np.pow(period, 2 / 3)


def valid_newton_approximation(array, a, eccentricity, E=0.0):
    time = array  # np.arange(0.0, 0.1, 0.01)
    current_x = 0.0
    x = []
    y = []
    E_data = []
    for i in time:
        anomaly = newton_method(kepler_equation, dkepler_equation, E, eccentricity, t=i)
        if not isinstance(anomaly, float):
            E = np.arccos(current_x / a) + 1e-2
            continue
        x.append(get_x_coord(anomaly, a))
        y.append(get_y_coord(anomaly, a, eccentricity))
        E_data.append(anomaly)
    return x, y, E_data

# Start


def main():
    # Call a function
    # setup
    E = 0.0
    eccentricity = 0.5
    period = 1
    a = 1
    t = 0
    dt = 0.01
    rotation = 2 * np.pi

    fig, ax = plt.subplots()

    x_data, y_data, data_E = valid_newton_approximation(np.arange(0.0, 2 * np.pi, 0.09), a=a, eccentricity=eccentricity)
    print(y_data)
    print(x_data)
    m = plt.plot(x_data, y_data, 'bo')

    ax = plt.axis([-2, 2, -2, 2])

    sun, = plt.plot([a * eccentricity], [newton_method(kepler_equation, dkepler_equation, E, eccentricity=eccentricity, t=0)], 'yo')

    redDot, = plt.plot([0], [newton_method(kepler_equation, dkepler_equation, E, eccentricity=eccentricity, t=0)], 'ro')

    def animate(i):
        redDot.set_data(get_x_coord(i, a), get_y_coord(i, a, eccentricity=eccentricity))
        return redDot,

    myAnimation = animation.FuncAnimation(fig, animate, frames=data_E, interval=500, blit=True,
                                          repeat=True)

    f1 = r"c://Users/tharo/Desktop/KeplerOrbit.gif"
    writergif = animation.PillowWriter(fps=10)
    myAnimation.save(f1, writer=writergif)

    f2 = r"c://Users/tharo/Desktop/KeplerOrbit.mp4"
    writervideo = animation.FFMpegWriter(fps=8)
    myAnimation.save(f2, writer=writervideo)

    plt.show()
    # End



# Main__________________________________________________________________________

if __name__== "__main__":
    main()


###############################################################################################################
# note: Below was only testing and figuring the idea out
# You may read the code below, thinking how frustating it can be, but it is part of the exciting experience :')


"""
x_data = []
y_data = []

fig = plt.figure()
ax = plt.axes(xlim=(-7, 7), ylim=(-3, 3))
line, = ax.plot([], [], lw=2)


def init():
    line.set_data([], [])
    return line,



def animate(i):
    x = np.linspace(0, np.pi, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line.set_data(x, y)
    return line,




def animate(i):
    x = np.linspace(0, np.pi, 1000)
    E = newton_method(kepler_equation, dkepler_equation, E, t=x)
    if not isinstance(E, float):
        E = np.arccos(x/a) + eccentricity
        continue
    y = newton_method(kepler_equation, dkepler_equation, E, t=x)
    line.set_data(x, y)
    return line,


anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=200, interval=20, blit=True)

plt.show()
"""

"""
x = np.linspace(0, np.pi, 50)
print(type(x))
print(np.linspace(0, np.pi, 50))
print(newton_method(kepler_equation, dkepler_equation, E, t=3.2))

# k, l = valid_newton_approximation(np.arange(0.0, np.pi, 0.01))
# print(k)
# print(l)
##################################################################################################################


x = a * np.cos(eccentric_anomaly) - (a * eccentricity)
y = a * np.pow(1-np.pow(eccentricity, 2), 0.5) * np.sin(eccentric_anomaly)


print(get_a_from_T(5))
"""