#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      10 April, 2022
   Kurs:      ESC202
   Semester:  FS22
   Week:      7
   Thema:     Ising Model
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# from scipy.ndimage import convolve, generate_binary_structure
from numba import njit


# k_boltzmann = 1.380649e-23
def create_grid(n):
    random_array = np.random.random((n, n))
    grid = np.zeros((n, n))
    grid[random_array >= 0.8] = 1
    grid[random_array < 0.8] = -1
    return grid


# note: white = 0/+ ; black = 1/-
@njit
def metropolis(grid: np.ndarray, beta: float):
    n = np.shape(grid)[0]
    for t in range(n ** 2):
        # 2. pick random point on array and flip spin
        x = np.random.randint(0, n)
        y = np.random.randint(0, n)
        spin_i = grid[x, y]  # initial spin
        spin_f = spin_i * -1  # proposed spin flip

        # compute change in energy
        E_i = 0
        E_f = 0
        if x > 0:
            E_i += -spin_i * grid[x - 1, y]
            E_f += -spin_f * grid[x - 1, y]
        if x < n - 1:
            E_i += -spin_i * grid[x + 1, y]
            E_f += -spin_f * grid[x + 1, y]
        if y > 0:
            E_i += -spin_i * grid[x, y - 1]
            E_f += -spin_f * grid[x, y - 1]
        if y < n - 1:
            E_i += -spin_i * grid[x, y + 1]
            E_f += -spin_f * grid[x, y + 1]

        # 3 / 4. change state with designated probabilities
        dE = E_f - E_i
        if (dE > 0) * (np.random.random() < np.exp(-beta * dE)):
            grid[x, y] = spin_f
        elif dE < 0:
            grid[x, y] = spin_f


@njit
def n_per_temperatur(grid: np.ndarray, beta):
    n = 40
    for i in range(n):
        metropolis(grid, beta)


def mean_m(grid: np.ndarray, n):
    return np.sum(grid) / (n ** 2)


def animate(i):
    beta = 1.0 / (i/10) # todo I don't know, why this factor for animation is smoother for the animation, maybe cause J or k_Boltzmann
    print(i/10)
    n_per_temperatur(grid, beta)
    mat.set_data(grid)
    return mat
    # magnetization = mean_m(grid, n)
    # temp_series.append((t, magnetization))


np.random.seed(42)
n = 100
grid = create_grid(n)
plot_series = np.zeros((0, n, n))
temp_series = []
temp_start = 40
temp_end = 0

fig, ax = plt.subplots()
mat = ax.matshow(grid)

t = temp_start
"""
while t > temp_end:
    beta = 1.0 / t
    n_per_temperatur(grid, beta)
    ax.matshow(grid)
    plot_series = np.append(plot_series, [grid], axis=0)
    magnetization = mean_m(grid, n)
    temp_series.append((t, magnetization))
    t = t - 1
"""
# print(np.shape(plot_series))
ani = animation.FuncAnimation(fig, animate, frames=np.arange(temp_start, temp_end, -1), interval=500, repeat=False)
# f = r"ising_model.gif"
# writergif = animation.PillowWriter(fps=3)
# ani.save(f, writer=writergif)
plt.show()
