#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      05 December, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      10
   Thema:     Electron, LeapFrog
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from matplotlib import animation
from scipy import ndimage
import matplotlib as mpl

"""
# for saving the .mp4 animation
mpl.rcParams[
    'animation.ffmpeg_path'] = r'D:\\Bachelor Informatik\\pythonProject\\ffmpeg-4.4.1-essentials_build\\bin\\ffmpeg.exe'
"""


# given SOR solution
def SOR(U, W, R):
    # define empty grid voltage
    C = np.ones_like(U)
    M = np.ones_like(U)

    # checker board
    B = np.ones_like(U, dtype=bool)
    B[::2, ::2] = False
    B[1::2, 1::2] = False

    # iterate until voltage change is smaller than 1
    while np.max(np.abs(M)) >= 1:
        ndimage.convolve(U, W, output=C, mode="constant", cval=0)
        np.multiply(R, C, out=M)
        U[B] = U[B] + M[B]

        ndimage.convolve(U, W, output=C, mode="constant", cval=0)
        np.multiply(R, C, out=M)
        U[~B] = U[~B] + M[~B]

    return U


def get_phi_a(static_field, x, y, distance):
    x_tmp = x
    y_tmp = y
    fx = int(x_tmp // distance)
    fy = int(y_tmp // distance)
    t = (x_tmp / distance - fx)
    u = (y_tmp / distance - fy)
    phi_1 = static_field[fx, fy]
    phi_2 = static_field[fx + 1, fy]
    phi_3 = static_field[fx, fy + 1]
    phi_4 = static_field[fx + 1, fy + 1]
    return 1.756e11 * ((1 - u) * (phi_2 - phi_1) + u * (phi_4 - phi_3)) / distance, \
           1.756e11 * ((1 - t) * (phi_3 - phi_1) + t * (phi_4 - phi_2)) / distance


def get_psi():
    x = np.random.normal(1, 0.5)
    y = np.random.normal(0.0, 2.0)
    return [x, y]


def leapfrog_CP(static_field, x, y, vx, vy, time, delta_t, distance):
    x_tmp = x + vx * delta_t * .5
    y_tmp = y + vy * delta_t * .5
    ax, ay = get_phi_a(static_field, x, y, distance)
    vx += ax * delta_t
    vy += ay * delta_t
    x = x_tmp + vx * delta_t * .5
    y = y_tmp + vy * delta_t * .5
    return x, y, vx, vy, time + delta_t


def init():
    for particle in particles:
        particle.set_data([], [])
    for line in lines:
        line.set_data([], [])
    for txt in text:
        txt.set_text('')

    return containers


def update(frame):
    global electron_x, electron_y
    global electron_vx, electron_vy
    global x_data, y_data
    global t, dt

    # record data
    x_data.append(electron_x / distance)
    y_data.append(electron_y / distance)

    # generate new frame data
    for _ in range(10):
        if lower_bound < electron_x < upper_bound and lower_bound < electron_y < upper_bound:
            electron_x, electron_y, electron_vx, electron_vy, t = \
                leapfrog_CP(field, electron_x, electron_y, electron_vx, electron_vy, t, dt, distance)
        elif upper_bound < electron_x and lower_bound + 0.001 < electron_y < lower_bound + 0.004:
            print("Electron hit detector in %d psec" % (t * 1e12))
            t = 0
            electron_x, electron_y = start[0] * distance, start[1] * distance
            x_data = [electron_x / distance]
            y_data = [electron_y / distance]
            electron_vx, electron_vy = np.cos(get_psi()[0]) * .1e6, np.sin(get_psi()[1]) * .1e6
        else:
            print(electron_y)
            t = 0
            electron_x, electron_y = start[0] * distance, start[1] * distance
            x_data = [electron_x / distance]
            y_data = [electron_y / distance]
            electron_vx, electron_vy = np.cos(get_psi()[0]) * .1e6, np.sin(get_psi()[1]) * .1e6

    for txt in text:
        txt.set_text("seconds: %0.12f" % t)
    for line in lines:
        line.set_data(x_data, y_data)
    for particle in particles:
        particle.set_data(x_data[-1], y_data[-1])

    return containers


def main():
    global distance
    global size
    global ani
    global containers
    global particles
    global lines
    global text
    global x_data, y_data
    global electron_x, electron_y
    global electron_vx, electron_vy
    global lower_bound, upper_bound
    global start
    global t, dt
    global field

    # model
    size = 1000
    distance = 0.01 / size
    upper_bound = distance * (
            size - 1)  # size boundary is reduced by 1 cause the bilinear calculation of the acceleration
    lower_bound = distance * 1
    inst_size = np.array([size, size], dtype=int)
    start = np.array([2, size * 0.75], dtype=int)  # in the middle of the generator

    # Field
    field = np.zeros(shape=inst_size, dtype=float)

    for i in range(950):
        field[30 + i, int(900 - i / 900 * 460)] = -1000
        field[30 + i, int(810 - i / 900 * 460)] = 1000
        field[30 + i, int(690 - i / 900 * 540)] = 1000
        field[30 + i, int(600 - i / 900 * 540)] = -1000

        field[30 + i, int(840 - i / 900 * 460)] = 0
        field[30 + i, int(660 - i / 900 * 540)] = 0

    #
    border = np.zeros_like(field, dtype=float)
    border[1:-1, 1:-1] = 1

    for i in range(920):
        border[30 + i, int(900 - i / 900 * 460)] = 0
        border[30 + i, int(810 - i / 900 * 460)] = 0
        border[30 + i, int(690 - i / 900 * 540)] = 0
        border[30 + i, int(600 - i / 900 * 540)] = 0

        border[30 + i, int(840 - i / 900 * 460)] = 0
        border[30 + i, int(660 - i / 900 * 540)] = 0

    omega = 2 / (1 + (np.pi / size))
    border *= (omega / 4)

    C = np.zeros_like(field, dtype=bool)
    C[::2, ::2] = True
    C[1::2, 1::2] = True

    W = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=float)
    """
    # safe the field and boundaries to avoid recalculation of the static field
    field = SOR(field, W, border)
    np.save("final_field_calculation", field)
    """
    field = np.load("final_field_calculation.npy")
    # field = np.zeros_like(field)

    # simulate particle
    electron_x = start[0] * distance
    electron_y = start[1] * distance
    electron_vx = 0
    electron_vy = 0
    t = 0
    dt = 1e-12

    # generate data
    hist_data = []
    detector_collision = []
    fails = 0
    count = 0
    e_x, e_y = start[0] * distance, start[1] * distance
    e_vx, e_vy = np.cos(get_psi()[0]) * .1e6, np.sin(get_psi()[1]) * .1e6
    while count < 1000:
        if lower_bound < e_x < upper_bound and lower_bound < e_y < upper_bound:
            e_x, e_y, e_vx, e_vy, t = leapfrog_CP(field, e_x, e_y, e_vx, e_vy, t, dt, distance)

        # detects electrons and collects data for the duration and collision position
        elif upper_bound < e_x and lower_bound + 0.001 < e_y < lower_bound + 0.004:
            hist_data.append(t * 1e12)
            detector_collision.append(e_y)
            t = 0
            e_x, e_y = start[0] * distance, start[1] * distance
            e_vx, e_vy = np.cos(get_psi()[0]) * .1e6, np.sin(get_psi()[1]) * .1e6
            count += 1
            print(count, "/1000")

        # if the electrons do not hit the detector
        else:
            t = 0
            e_x, e_y = start[0] * distance, start[1] * distance
            e_vx, e_vy = np.cos(get_psi()[0]) * .1e6, np.sin(get_psi()[1]) * .1e6
            fails += 1
            count += 1
            print(count, "/1000")

    # animation
    sim_background = np.ones(shape=inst_size) * 0.8
    field_background = field.T

    # fig setup
    fig = plt.figure(figsize=(15, 5))

    # axes setup
    ax_1 = fig.add_subplot(1, 3, 1)  # gs[:, :])
    ax_2 = fig.add_subplot(1, 3, 2)
    ax_3 = fig.add_subplot(1, 3, 3)
    axes = [ax_1]
    plt.setp(axes, xticks=[], yticks=[])

    # data setup for creating the animation
    x_data = []
    y_data = []

    ax_2.hist(hist_data, 100)
    ax_2.set_xlabel("Undetected electrons: %d " % fails)
    ax_2.set_xlim(0, size)

    ax_3.hist(detector_collision, 1000)
    ax_3.set_xlabel("Position of the collision on the detector")
    ax_3.set_xlim(0.001, 0.0045)

    ax_1.set_title('Electrons - bilinear/leapfrog', fontsize=10)
    ax_1.imshow(sim_background.T, origin='lower', norm=colors.Normalize(0, 1), cmap='plasma')
    CS = ax_1.contour(field_background, alpha=0.8)
    ax_1.clabel(CS, CS.levels, inline=True, fontsize=8, fmt='%dV', colors="black")
    ax_1.set_xlim(0, size)
    ax_1.set_ylim(0, size)

    particles = [ax_1.plot([], [], 'o')[0] for _ in range(1)]
    lines = [ax_1.plot([], [], alpha=.5)[0] for _ in range(1)]
    text = [ax_1.text(0.38, 0.01, '', transform=ax_1.transAxes)]

    containers = particles + lines + text

    # starting Animation
    ani = animation.FuncAnimation(fig, update, frames=256, init_func=init, blit=True, interval=10)
    """
    f = r"c://Users/tharo/Desktop/Electron_animation.mp4"
    writermp4 = animation.FFMpegWriter(fps=60)
    ani.save(f, writer=writermp4)
    """
    plt.show()


if __name__ == "__main__":
    main()
