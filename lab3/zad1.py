from mpmath import mp

a1 = 1.5 * mp.pi
b1 = 2 * mp.pi


def f1(x): return mp.cos(x) * mp.cosh(x) - 1


def df1(x): return mp.cos(x) * mp.sinh(x) - mp.sin(x) * mp.cosh(x)


a2 = 0
b2 = mp.pi / 2


def f2(x): return 1 / x - mp.tan(x)


def df2(x): return -1 / x ** 2 - mp.sec(x) ** 2


a3 = 1
b3 = 3


def f3(x): return 2 ** (-x) + mp.e ** x + 2 * mp.cos(x) - 6


def df3(x): return mp.e ** x - 2 ** (-x) * mp.log(2) - 2 * mp.sin(x)


def bisection(f, a, b, eps, prec):
    mp.dps = prec
    a = mp.mpf(a)
    b = mp.mpf(b)
    i = 0
    while b - a > eps:
        i += 1
        x = (a + b) / 2
        if f(b) * f(x) < 0:
            a = x
        else:
            b = x

    return (a + b) / 2, i


print(bisection(f2, a2, b2, 10e-7, 10))


def newton(f, df, a, b, eps, prec, iters):
    mp.dps = prec
    i = 0
    x = a
    x_p = b
    while abs(x_p - x) > eps and i < iters:
        x_p = x
        x = x_p - f(x_p) / df(x_p)
        i += 1
    return x, i


print(newton(f3, df3, a3, b3, 10e-7, 10, 10000))


def secand(f, a, b, eps, prec, iters):
    mp.dps = prec
    i = 2
    xs = [a, b]
    while abs(xs[i-1] - xs[i-2]) > eps and i < iters:
        xs.append((f(xs[i-1]) * xs[i-2] - f(xs[i-2]) * xs[i-1]) / (f(xs[i-1]) - f(xs[i-2])))
        i += 1
    return xs[-1], i


print(secand(f3, a3, b3, 0.00001, 10, 10000))
