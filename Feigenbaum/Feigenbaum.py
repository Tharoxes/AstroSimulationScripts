#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
   Name:      Huynh, Thanh Cong
   Email:     thanhcong.huynh@uzh.ch
   Date:      17. Octobre 2021
   Kurs:      ESC201
   Semester:  HS21
   Week:      3
   Thema:     Feigenbaum
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as figure
from matplotlib.pyplot import figure


# Pierre François Verhulst logistics equation
def locgisticEquation(a, x, N):
    while N > 0:
        N -= 1
        x = a * x * (1 - x)
    return x


def main():
    # set-up variables
    width, height = 3000, 600
    maxN = 200

    # Logistic Map with meshgrid
    # range was [0, 4], but [0, 1] is not quite interesting
    [a, x] = np.meshgrid(np.linspace(0.7, 4, width), np.linspace(0.01, 0.99, height))
    x_max = locgisticEquation(a, x, maxN)

    figure(figsize=(16, 10), dpi=200)
    plt.scatter(a, x_max, s=0.001)
    plt.title("Feigenbaum")
    plt.xlabel("a")
    plt.ylabel(r'$x_\infty $')
    plt.ylim(-0.2, 1.0)

    plt.savefig('Feigenbaum.png', format='png')
    plt.show()

    # Feigenbaum Zoom(first branch)
    figure(figsize=(16, 10), dpi=200)
    plt.scatter(a, x_max, s=0.001)
    plt.title("Feigenbaum")
    plt.xlabel("a")
    plt.ylabel(r'$x_\infty $')
    plt.ylim(0.65, 0.9)
    plt.xlim(2.95, 3.7)

    plt.savefig('FeigenbaumZoom.png', format='png')
    plt.show()
    print("Done!")


# main
if __name__ == "__main__":
    main()
