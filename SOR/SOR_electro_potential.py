#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      20 November, 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      8
   Thema:     Electric Potential - Successive over-relaxation
"""

import numpy as np
import matplotlib.pyplot as plt

"""
idea: 
create 3 meshgrids: index meshgrid for every points; 
                    U(x, y); 
                    consider the Boundary Conditions (0 Volt; 1000V)
"""


def SOR(x, y, U, omega, iterations):
    k = 0
    while k < iterations:
        for i in range(np.shape(x)[1]):
            for j in range(np.shape(y)[1]):
                # consider here the boundary condition of 0V on the edge for black
                if 0 < i < np.shape(x)[1] - 1 and 0 < j < np.shape(y)[0] - 1 and not (U[i][j] == 1000):
                    if (i + j) % 2 == 0:
                        U[i][j] = U[i][j] + (
                                (U[i - 1][j] + U[i + 1][j] + U[i][j - 1] + U[i][j + 1] - 4 * U[i][j]) * omega / 4)

        for i in range(np.shape(x)[1]):
            for j in range(np.shape(y)[1]):
                # consider here the boundary condition of 0V on the edge for white
                if 0 < i < np.shape(x)[1] - 1 and 0 < j < np.shape(y)[0] - 1 and not (U[i][j] == 1000):
                    if (i + j) % 2 == 1:
                        U[i][j] = U[i][j] + (
                                (U[i - 1][j] + U[i + 1][j] + U[i][j - 1] + U[i][j + 1] - 4 * U[i][j]) * omega / 4)
        k += 1
    return U


def create_grid(n):
    x = np.linspace(0, n - 1, n)
    y = np.linspace(0, n - 1, n)
    xx, yy = np.meshgrid(x, y)

    U_grid = np.zeros((n, n))
    return xx, yy, U_grid


def main():
    # iterations and precicison of 1 Volt
    n = 50  # gridpoints n**2
    p = 3  # precision of 1 Volt with the boundary condition 1000V by 10^(-p)
    x, y, U = create_grid(n)

    # Boundary condition 1000 V
    U[n // 2][((n - 5) // 2):((n + 5) // 2):] = 1000

    # SOR setup
    omega = 2 / (1 + np.pi / n)
    N_iter = n // 3 * p
    U_SOR = SOR(x, y, U, omega, N_iter)
    fig, ax1 = plt.subplots(1, 1)
    cp1 = ax1.contourf(x, y, U_SOR)
    fig.colorbar(cp1)
    ax1.set_title('eletric potential SOR')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    # plt.savefig('Electric_Potential_SOR.png')

    """
    # Jakobi setup (number of iterations changed and omega value) // wait 1-2min until the code is executed for this block
    omega_jakobi = 1
    N_iter_jakobi = p * n ** 2 // 2
    U_JAK = SOR(x, y, U, omega_jakobi, N_iter_jakobi)
    fig, ax2 = plt.subplots(1, 1)
    cp2 = ax2.contourf(x, y, U_JAK)
    fig.colorbar(cp2)
    ax2.set_title('eletric potential JAK')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    # plt.savefig('Electric_Potential_JAK.png')
    """

    plt.show()


if __name__ == '__main__':
    main()
