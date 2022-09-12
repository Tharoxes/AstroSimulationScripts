#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      14 November, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      7
   Thema:     Solar System
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as grt
from matplotlib import animation
#import matplotlib as mpl
#mpl.rcParams['animation.ffmpeg_path'] = r'D:\\Bachelor Informatik\\pythonProject\\ffmpeg-4.4.1-essentials_build\\bin\\ffmpeg.exe'


def importing_data(filename):
    # filename = 'SolSystData.dat'

    data = np.loadtxt(filename, delimiter=',', unpack=True, ndmin=1, converters={1: lambda s: float(s)},
                      dtype={'names': ('planet', 'mass', 'x', 'y', 'z', 'vx', 'vy', 'vz'),
                             'formats': ('S10', float, float, float, float, float, float, float)})

    return data


def leapFrog(data, h):
    k_square = 0.01720209895 ** 2
    N = data.shape[0]
    h *= .5
    # Drifts
    for i in range(N):
        data[i][1] += data[i][4] * h
        data[i][2] += data[i][5] * h
        data[i][3] += data[i][6] * h

    # Kicks
    for i in range(N):
        for j in range(N):
            if i == j:
                continue
            ir3 = ((data[i][1] - data[j][1]) * (data[i][1] - data[j][1]) +
                   (data[i][2] - data[j][2]) * (data[i][2] - data[j][2]) +
                   (data[i][3] - data[j][3]) * (data[i][3] - data[j][3])) ** 1.5
            data[i][4] += k_square * (data[j][1] - data[i][1]) * data[j][0] / ir3
            data[i][5] += k_square * (data[j][2] - data[i][2]) * data[j][0] / ir3
            data[i][6] += k_square * (data[j][3] - data[i][3]) * data[j][0] / ir3

    # Drifts
    for i in range(N):
        data[i][1] += data[i][4] * h
        data[i][2] += data[i][5] * h
        data[i][3] += data[i][6] * h

    return data


def init():
    # plot 1
    for planet in planets1:
        planet.set_data([], [])
    for line in lines1:
        line.set_data([], [])
    for j, label in enumerate(labels1):
        label.set_text(SolSysNameInner[j].decode('UTF-8').strip("'"))
    for txt in text1:
        txt.set_text('')

    # plot 2
    for planet in planets2:
        planet.set_data([], [])
    for line in lines2:
        line.set_data([], [])
    for j, label in enumerate(labels2):
        label.set_text(SolSysNameInner[j].decode('UTF-8').strip("'"))
    for txt in text2:
        txt.set_text('')

    # plot 3
    for planet in planets3:
        planet.set_data([], [])
    for line in lines3:
        line.set_data([], [])
    for j, label in enumerate(labels3):
        label.set_text(SolSysNameOuter[j].decode('UTF-8').strip("'"))
    for txt in text3:
        txt.set_text('')

    # plot 4
    for planet in planets4:
        planet.set_data([], [])
    for line in lines4:
        line.set_data([], [])
    for j, label in enumerate(labels4):
        label.set_text(SolSysNameOuter[j].decode('UTF-8').strip("'"))
    for txt in text4:
        txt.set_text('')
    return containers


def update(frame):
    global solar_inner, solar_outer

    # updated frames (365/4 -> 91)
    solar_inner = leapFrog(solar_inner, 1.0)
    j = 91
    while j > 0:
        solar_outer = leapFrog(solar_outer, 1.0)
        j -= 1

    # plot 1: Plot X, Y from inner solar system
    for txt in text1:
        txt.set_text("Earth days: " + str(frame))
    for j, planet in enumerate(planets1):
        planet.set_data(x_inner[j][-1], y_inner[j][-1])
    for j, line in enumerate(lines1):
        x_inner[j].append(solar_inner[j][1])
        y_inner[j].append(solar_inner[j][2])
        line.set_data(x_inner[j], y_inner[j])
    for j, label in enumerate(labels1):
        label.set_position((x_inner[j][-1] + 0.01, y_inner[j][-1] + 0.01))

    # plot 2: Plot X, Z from inner solar system
    for txt in text2:
        txt.set_text("Earth days: " + str(frame))
    for j, line in enumerate(lines2):
        x_inner2[j].append(solar_inner[j][1])
        z_inner[j].append(solar_inner[j][3])
        line.set_data(x_inner2[j], z_inner[j])
    for j, planet in enumerate(planets2):
        planet.set_data(x_inner2[j][-1], z_inner[j][-1])
    for j, label in enumerate(labels2):
        label.set_position((x_inner2[j][-1] + 0.01, z_inner[j][-1] + 0.01))

    # plot 3: Plot X, Y from outer solar system
    for txt in text3:
        txt.set_text("Earth years: " + str(frame / 4))
    for j, line in enumerate(lines3):
        x_outer[j].append(solar_outer[j][1])
        y_outer[j].append(solar_outer[j][2])
        line.set_data(x_outer[j], y_outer[j])
    for j, planet in enumerate(planets3):
        planet.set_data(x_outer[j][-1], y_outer[j][-1])
    for j, label in enumerate(labels3):
        label.set_position((x_outer[j][-1] + 1, y_outer[j][-1] + 1))

    # plot 4: Plot X, Z from outer solar system
    for txt in text4:
        txt.set_text("Earth years: " + str(frame / 4))
    for j, line in enumerate(lines4):
        x_outer2[j].append(solar_outer[j][1])
        z_outer[j].append(solar_outer[j][3])
        line.set_data(x_outer2[j], z_outer[j])
    for j, planet in enumerate(planets4):
        planet.set_data(x_outer2[j][-1], z_outer[j][-1])
    for j, label in enumerate(labels4):
        label.set_position((x_outer2[j][-1] + 1, z_outer[j][-1] + 1))

    return containers


def main():
    global solar_inner, solar_outer
    global SolSysNameInner, SolSysNameOuter
    global x_inner, y_inner, x_inner2, z_inner
    global x_outer, y_outer, x_outer2, z_outer
    global containers
    global planets1, planets2, planets3, planets4
    global lines1, lines2, lines3, lines4
    global labels1, labels2, labels3, labels4
    global text1, text2, text3, text4

    # displaying plots
    fig = plt.figure(figsize=(10, 8))
    grid = grt.GridSpec(nrows=13, ncols=17)
    ax1 = fig.add_subplot(grid[:8, :8])
    ax2 = fig.add_subplot(grid[9:, :8])
    ax3 = fig.add_subplot(grid[:8, 9:])
    ax4 = fig.add_subplot(grid[9:, 9:])
    axes = [ax1, ax2, ax3, ax4]
    plt.setp(axes, xticks=[], yticks=[])

    # data manipulation
    data = importing_data("SolSystData.dat")
    sun = np.array(data[1:]).T[0]
    inner = np.array(data[1:]).T[1:5]
    outer = np.array(data[1:]).T[-4:]
    solar_inner = np.concatenate(([sun], inner))
    SolSysNameInner = np.array(data[0])[:5]
    solar_outer = np.concatenate(([sun], outer))
    SolSysNameOuter = np.array(data[0])[[0, 5, 6, 7, 8]]

    # consider x_inner and x_inner2(x_outer and x_outer2) are the same at the beginning, but the updated values differ from
    # the systems XY and XZ (except renaming the updated values)
    N_inner = np.shape(solar_inner)[0]

    x_inner = [[solar_inner[i][1]] for i in range(N_inner)]
    y_inner = [[solar_inner[i][2]] for i in range(N_inner)]

    x_inner2 = [[solar_inner[i][1]] for i in range(N_inner)]
    z_inner = [[solar_inner[i][3]] for i in range(N_inner)]

    N_outer = np.shape(solar_outer)[0]

    x_outer = [[solar_outer[i][1]] for i in range(N_outer)]
    y_outer = [[solar_outer[i][2]] for i in range(N_outer)]

    x_outer2 = [[solar_outer[i][1]] for i in range(N_outer)]
    z_outer = [[solar_outer[i][3]] for i in range(N_outer)]

    # Plot 1
    ax1.set_title('Inner Solar System', fontsize=10)
    ax1.set_xlim(-2.0, 2.0)
    ax1.set_ylim(-2.0, 2.0)

    planets1 = [ax1.plot([], [], 'o')[0] for i in range(N_inner)]
    lines1 = [ax1.plot([], [], linestyle='dashed')[0] for i in range(N_inner)]
    labels1 = [ax1.text([], [], '', transform=ax1.transData) for i in range(N_inner)]
    text1 = [ax1.text(0.38, 0.01, '', transform=ax1.transAxes)]

    container1 = planets1 + lines1 + labels1 + text1

    # Plot 2
    ax2.set_xlim(-2.0, 2.0)
    ax2.set_ylim(-1.0, 1.0)

    planets2 = [ax2.plot([], [], 'o')[0] for i in range(N_inner)]
    lines2 = [ax2.plot([], [], linestyle='dashed')[0] for i in range(N_inner)]
    labels2 = [ax2.text([], [], '', transform=ax2.transData) for i in range(N_inner)]
    text2 = [ax2.text(0.38, 0.01, '', transform=ax2.transAxes)]
    container2 = planets2 + lines2 + labels2 + text2

    # Plot 3
    ax3.set_title('Outer Solar System', fontsize=10)
    ax3.set_xlim(-33.0, 33.0)
    ax3.set_ylim(-33.0, 33.0)

    planets3 = [ax3.plot([], [], 'o')[0] for i in range(N_outer)]
    lines3 = [ax3.plot([], [], linestyle='dashed')[0] for i in range(N_outer)]
    labels3 = [ax3.text([], [], '', transform=ax3.transData) for i in range(N_outer)]
    text3 = [ax3.text(0.38, 0.01, '', transform=ax3.transAxes)]
    container3 = planets3 + lines3 + labels3 + text3

    # Plot 4
    ax4.set_xlim(-32.0, 32.0)
    ax4.set_ylim(-16.0, 16.0)

    planets4 = [ax4.plot([], [], 'o')[0] for i in range(N_outer)]
    lines4 = [ax4.plot([], [], linestyle='dashed')[0] for i in range(N_outer)]
    labels4 = [ax4.text([], [], '', transform=ax4.transData) for i in range(N_outer)]
    text4 = [ax4.text(0.38, 0.01, '', transform=ax4.transAxes)]
    container4 = planets4 + lines4 + labels4 + text4

    containers = container1 + container2 + container3 + container4

    # starting and saving Animation
    ani = animation.FuncAnimation(fig, update, frames=365, init_func=init, blit=True, interval=30)
    """
    f = r"c://Users/tharo/Desktop/Solar_System_first_365d.gif"
    writergif = animation.PillowWriter(fps=20)
    ani.save(f, writer=writergif)
    writervideo = animation.FFMpegWriter(fps=30)
    f = r"c://Users/tharo/Desktop/Solar_System_second_365d.mp4"
    ani.save(f, writer=writervideo)
    """
    plt.show()


if __name__ == '__main__':
    main()
