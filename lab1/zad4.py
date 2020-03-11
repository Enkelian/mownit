from numpy import float32
from numpy import float64
from numpy import arange
import matplotlib.pyplot as plt
from IPython.display import HTML, display
import tabulate
import prettytable
N = 1000


def xtoN32(x_0, r):
    xtab = [float32(x_0)]
    r = float32(r)
    for i in range(0, N):
        xtab.append(float32(r * xtab[i] * (1 - xtab[i])))
    return xtab


def xtoN64(x_0, r):
    xtab = [float64(x_0)]
    r = float64(r)
    for i in range(0, N):
        xtab.append(float64(r * xtab[i] * (1 - xtab[i])))
    return xtab


def a(lastn):
    R = []
    for r in arange(1, 4, 0.01):
        R.append(r)

    for x_0 in arange(0.1, 1, 0.1):
        for r in R:
            xtab = xtoN32(x_0, r)
            for i in (N - lastn, N):
                plt.plot(r, xtab[i], '.', markersize=2)

    plt.show()


def b():
    R = []
    for r in arange(3.75, 3.8, 0.0001):
        R.append(r)

    for x_0 in arange(0.1, 1, 0.1):
        xn32 = []
        xn64 = []
        for r in R:
            xn32.append(xtoN32(x_0, r)[N - 1])
            xn64.append(xtoN64(x_0, r)[N - 1])
        plt.subplot(1, 2, 1)
        plt.plot(R, xn32, '.', markersize=2)
        plt.subplot(1, 2, 2)
        plt.plot(R, xn64, '.', markersize=2)
    plt.show()


def c():
    r = 4
    n = 1000
    eps = 1e-4
    x_0s = []
    for x_0 in arange(0.01, 1, 0.01):
        x_0s.append(x_0)

    iters = []
    for x_0 in x_0s:
        xtab = [float32(x_0)]
        r = float32(r)
        i = 0
        while xtab[i] > eps and i < n:
            xtab.append(r * xtab[i] * (1 - xtab[i]))
            i = i + 1
        iters.append(i)
    plt.plot(x_0s, iters, '.', markersize=2)
    plt.show()


# a(1)
c()
