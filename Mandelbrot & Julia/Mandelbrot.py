import numpy as np
import matplotlib.pyplot as plt


def mandelbrot(xmin, xmax, ymin, ymax, N_max, threshold):
    nx = int(abs(xmax - xmin) * 150)  # arbitrary choice of number of steps
    ny = int(abs(ymax - ymin) * 150)  # arbitrary choice of number of steps
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)

    # grid
    c = x[np.newaxis, :] + 1j * y[:, np.newaxis]
    z = c
    # two RuntimeErrors occured:
    # overflow encountered in square (could not be solved dtype choice)
    # invalid value encountered in square
    with np.warnings.catch_warnings():
        np.warnings.simplefilter("ignore")
        for i in range(N_max):
            z = z ** 2 + c
        mandelbrot_set = (abs(z) < threshold)
    return mandelbrot_set


def main():
    # start values
    xmin = -2
    xmax = 1
    ymin = -1.5
    ymax = 1.5

    # calculate mandelbrot set and create a plot
    plt.imshow(mandelbrot(xmin, xmax, ymin, ymax, 80, 2), extent=[-2, 2, -2, 2], cmap='RdBu')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Mandelbrot set")
    plt.savefig("Mandelbrot.png")

    plt.show()

    # Mandelbrot set is colored in black
    plt.imshow(mandelbrot(xmin, xmax, ymin, ymax, 80, 2), extent=[-2, 2, -2, 2], cmap='binary')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Mandelbrot set")
    plt.savefig("Mandelbrot_black.png")

    plt.show()


# main
if __name__ == "__main__":
    main()
