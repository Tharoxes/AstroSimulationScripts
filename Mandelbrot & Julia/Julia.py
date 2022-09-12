import numpy as np
import matplotlib.pyplot as plt


def julia_set(xmin = -2, xmax = 2, ymin = -2, ymax = 2, c=-0.29609091 + 0.62491j, max_iterations=200, threshold=2):
    # To make navigation easier we calculate these values
    nx = int(abs(xmax - xmin) * 250)  # arbitrary choice of number of steps
    ny = int(abs(ymax - ymin) * 250)  # arbitrary choice of number of steps
    x = np.linspace(xmin, xmax, nx)
    y = np.linspace(ymin, ymax, ny)

    # start values

    z = x[np.newaxis, :] + 1j * y[:, np.newaxis]

    # Initialize z to all zero
    c = np.full(z.shape, c)

    with np.warnings.catch_warnings():
        np.warnings.simplefilter("ignore")
        for i in range(max_iterations):
            z = z ** 2 + c
        julia_set = (abs(z) < threshold)
    return julia_set


def main():
    plt.imshow(julia_set(max_iterations=200), cmap='magma')
    plt.savefig("julia_set_-029609091+062491j_loop200.png")
    plt.show()
    plt.imshow(julia_set(max_iterations=1600), cmap='magma')
    plt.savefig("julia_set_-029609091+062491j_loop1600.png")
    plt.show()
    plt.imshow(julia_set(c=-0.8+0.156j, max_iterations=512), cmap='magma')
    plt.savefig("julia_set_-08+0156j_loop512.png")
    plt.show()
    plt.imshow(julia_set(c=-0.7269 + 0.1889j, max_iterations=256), cmap='magma')
    plt.savefig("julia_set_-07269+01889j_loop256.png")
    plt.show()
    plt.imshow(julia_set(c=-0.7269 + 0.1889j, max_iterations=200), cmap='magma')
    plt.savefig("julia_set_-07269+01889j_loop200.png")
    plt.show()
    plt.imshow(julia_set(c=0.1889j, max_iterations=512), cmap='magma')
    plt.savefig("julia_set_01889j_loop512.png")
    plt.show()
    plt.imshow(julia_set(c=-0.7269, max_iterations=512), cmap='magma')
    plt.savefig("julia_set_-07269_loop512.png")
    plt.show()


# main
if __name__ == "__main__":
    main()


