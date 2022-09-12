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


def main():
    # Create a figure with matplotlib
    fig, ((ax_1), (ax_2)) = plt.subplots(1, 2, figsize=(10, 6))
    steps = 100
    euler_q, euler_p, euler_H = euler_HOH(0, 1, steps, 0.1)
    rk_q, rk_p, rk_H = rk_midpoint_HOH(0, 1, steps, 0.1)
    leapfrog_q, leapfrog_p, leapfrog_H = leapFrog_HOH(0, 1, steps, 0.1)
    t = np.linspace(0, 10, steps + 1)
    # P Q Evolution
    ax_1.plot(euler_q, euler_p, label='Euler forward')
    ax_1.plot(rk_q, rk_p, label='Runge-Kutta Midpoint')
    ax_1.plot(leapfrog_q, leapfrog_p, label='LeapFrog')
    ax_1.set_xlabel('Q')
    ax_1.set_ylabel('P')
    ax_1.set_title('Oscillation', fontsize=10)
    ax_1.set_aspect('equal')
    ax_1.grid(False)
    ax_1.legend(loc='upper right', prop={'size': 6})
    # HOH Evolution
    ax_2.plot(t, euler_H, label='Euler Energy')
    ax_2.plot(t, rk_H, label='Runge-Midpoint Energy')
    ax_2.plot(t, leapfrog_H, label='LeapFrog Energy')
    ax_2.set_xlabel('Time')
    ax_2.set_ylabel('Energy')
    ax_2.set_title('Total Energy over Time', fontsize=10)
    ax_2.set_ylim(0, 1.8)
    ax_2.set_aspect(3)
    ax_2.grid(False)
    ax_2.legend(loc='upper right', prop={'size': 6})

    # Save the plot if desired
    # plt.savefig('HarmonicOscillation - Euler_RungeKutta_Leapfrog.png', format='png')

    plt.show()


# Main
if __name__ == "__main__":
    main()
