#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      05 November, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      6
   Thema:     Harmonic Oscillation, LeapFrog Integration
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as grt
from matplotlib.animation import FuncAnimation


def HOH(q, p):
    return 0.5 * p ** 2 - np.cos(q)


# Euler function
def euler(q, p, h):
    return q + h * p, p - h * np.sin(q)


def euler_HOH(q, p, N, dt):
    q_list = [q]
    p_list = [p]
    H_list = [HOH(q, p)]

    for i in range(N):
        q, p = euler(q, p, dt)
        q_list.append(q)
        p_list.append(p)
        H_list.append(HOH(q, p) + 1)

    return q_list, p_list, H_list


# Runge-Kutta Midpoint function
def rk_midpoint(q, p, dt):
    return p * dt, -q * dt


def rk_midpoint_HOH(q, p, N, dt):
    q_list = [q]
    p_list = [p]
    H_list = [HOH(q, p)]

    # using second order of Runge-Kutta for midpoint method
    for i in range(N):
        q_half, p_half = rk_midpoint(q, p, dt)
        q_new, p_new = rk_midpoint(q + q_half / 2.0, p, dt)

        q += q_new
        p += p_new

        q_list.append(q)
        p_list.append(p)
        H_list.append(HOH(q, p) + 1)

    return q_list, p_list, H_list


# Leapfrog function/ Strömer-Verlet function
def leapFrog(q, p, h):
    q_half = q + 0.5 * h * p
    p_new = p - h * np.sin(q_half)
    q_new = q_half + 0.5 * h * p_new
    return q_new, p_new


def leapFrog_HOH(q, p, N, dt):
    q_list = [q]
    p_list = [p]
    H_list = [HOH(q, p)]

    for i in range(N):
        q, p = leapFrog(q, p, dt)
        q_list.append(q)
        p_list.append(p)
        H_list.append(HOH(q, p) + 1)

    return q_list, p_list, H_list


def init():
    global frame
    frame = 0
    return None


def update(args):
    # consider the updated subplots by the new frame steps
    global ax_2
    global ax_3
    global frame

    # save the plot at the end of the animation (step 1100)
    if frame == steps:
        plt.savefig('Simple_Pendulum.png', format='png')

    # plot 2: Oscillation by Euler forward/Runge-Kutta Midpoint/Leapfrog
    ax_2.clear()
    ax_2.set_title('Oscillation', fontsize=10)
    ax_2.imshow(H, extent=(-12.0, 12.0, -4.0, 4.0), cmap='plasma')
    ax_2.plot(euler_q[:frame], euler_p[:frame], label='Euler')
    ax_2.plot(rk_q[:frame], rk_p[:frame], label='Runge-Kutta Midpoint')
    ax_2.plot(leap_q[:frame], leap_p[:frame], label='LeapFrog')
    ax_2.set_xlabel('Q')
    ax_2.set_ylabel('P')
    ax_2.set_xlim(-6.0, 6.0)
    ax_2.set_ylim(-4.0, 4.0)

    # plot 3: Energys
    ax_3.clear()
    ax_3.set_title('Total Energy over Time', fontsize=10)
    ax_3.plot(t[:frame], euler_H[:frame], label='Euler Energy')
    ax_3.plot(t[:frame], rk_H[:frame], label='Runge-Kutta Midpoint Energy')
    ax_3.plot(t[:frame], leap_H[:frame], label='LeapFrog Energy')
    ax_3.set_xlabel('Time')
    ax_3.set_ylabel('Energy')
    ax_3.set_ylim(0, 5.0)
    ax_3.set_xlim(0, 10)
    ax_3.legend(loc='upper right', prop={'size': 6})

    frame += 5  # animation speed
    return None


def main():
    global ax_2
    global ax_3
    global H
    global euler_q, euler_p, euler_H
    global leap_q, leap_p, leap_H
    global rk_q, rk_p, rk_H
    global t
    global steps

    Fig = plt.figure(figsize=(10, 8))
    gs = grt.GridSpec(nrows=2, ncols=2)
    ax_1 = Fig.add_subplot(gs[0, :])
    ax_2 = Fig.add_subplot(gs[1, 0])
    ax_3 = Fig.add_subplot(gs[1, 1])
    # data setup
    q, p = np.meshgrid(np.linspace(-12.0, 12.0, 420), np.linspace(-4.0, 4.0, 210))
    H = HOH(q, p)

    steps = 1100
    euler_q, euler_p, euler_H = euler_HOH(0, 0.1, steps, 0.1)
    leap_q, leap_p, leap_H = leapFrog_HOH(0, 1, steps, 0.1)
    rk_q, rk_p, rk_H = rk_midpoint_HOH(0, 0.1, steps, 0.1)
    t = np.linspace(0, 10, steps + 1)

    # plotting grid
    ax_1.set_title('Harmonic Oscillation of a Simple Pendulum', fontsize=15)
    ax_1.contour(q, p, H, 43, cmap='plasma')
    ax_1.set_xlabel('Q')
    ax_1.set_ylabel('P')
    ax_1.set_aspect('equal')

    # setup plot 2 for animation
    ax_2.set_title('Oscillation', fontsize=10)

    # setup plot 3 for animation
    ax_3.set_title('Total Energy over Time', fontsize=10)

    # starting Animation
    ani = FuncAnimation(Fig, update, None, init_func=init, interval=30)

    plt.show()


# Main
if __name__ == "__main__":
    main()
