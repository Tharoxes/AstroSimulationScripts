#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong Huynh
   Email:     thanhcong.huynh@uzh.ch
   Date:      19 December, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      12
   Thema:     2D Advection
"""

import numpy as np
import matplotlib.pyplot as plt


def ctu(rho, ca, cb, n=100):
    global rhoNew
    for i in range(n):
        rhoTmp = (1 - ca) * rho + ca * np.roll(rho, 1, axis=0)
        rhoNew = (1 - cb) * rhoTmp + cb * np.roll(rhoTmp, 1, axis=1)
        rho = rhoNew
    # Use np.roll(rho, 1, axis=0) to calculate the x-axis term in rhoTmp
    # Use np.roll(rho, 1, axis=1) to calculate the y-axis term in rhoNew
    return rhoNew


def cir(rho, ca, cb, dx, dy, dt, n=100):
    global rhoNew
    for i in range(n):
        rhoNew = rho - ((ca * dx / dt) * ((rho - np.roll(rho, 1, axis=0)) / dx) + (cb * dy / dt) * ((rho - np.roll(rho, 1, axis=1)) / dy)) * dt
        rho = rhoNew
    # Like function ctu(rho) but with CIR formula
    return rhoNew


def initialCondition(Nx, Ny, x0, y0, dx, dy, sigma_x, sigma_y):
    rho = np.zeros((Nx, Ny))
    for j in range(Nx):
        for l in range(Ny):
            x = j * dx
            y = l * dy
            rho[j, l] = np.exp(-(x - x0) ** 2 / (2 * sigma_x ** 2)
                               - (y - y0) ** 2 / (2 * sigma_y ** 2))
    return rho


def main():
    Nx = 200
    Ny = 200
    dx = 1.0 / Nx
    dy = 1.0 / Ny
    sigma_x = 10 * dx
    sigma_y = 10 * dy
    x0 = 2 * sigma_x
    y0 = 2 * sigma_y
    ca = 0.48
    cb = 0.48
    dt = 0.1

    rho = initialCondition(Nx, Ny, x0, y0, dx, dy, sigma_x, sigma_y)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 6))
    ax1.imshow(ctu(rho, ca, cb), origin="lower")
    ax1.contour(ctu(rho, ca, cb), 6, colors="black", linestyles="solid")
    ax1.set_title('CTU')
    ax2.imshow(cir(rho, ca, cb, dx, dy, dt), origin="lower")
    ax2.contour(cir(rho, ca, cb, dx, dy, dt), 6, colors="black", linestyles="solid")
    ax2.set_title('CIR')
    for i in range(8):
        ax3.contour(ctu(rho, ca, cb, i * 100), 6, cmap="viridis", linestyles = "solid")
    for i in range(8):
        ax4.contour(cir(rho, ca, cb, dx, dy, dt, i * 100), 6, cmap="viridis", linestyles="solid")

    plt.savefig("2DAdvection.png")
    plt.show()


if __name__ == "__main__":
    main()
