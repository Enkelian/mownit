import time
import numpy as np


def scale(a):
    n = len(a)
    for i in range(n):
        a[i] /= np.amax(a[i])


def gauss_jordan_solve(a):
    n = len(a)
    scale(a)
    for i in range(n):
        j = i
        while j < n and a[j, i] == 0:
            j += 1
        if j == n:
            return False
        a[[j, i]] = a[[i, j]]
        a[i] = a[i] / a[i, i]
        for k in range(i + 1, n):
            a[k] -= a[i] * a[k, i]
            a[k, i] = 0
        for k in range(i - 1, -1, -1):
            a[k] -= a[i] * a[k, i]
            a[k, i] = 0


def execute_random(n, eps):
    a1 = np.random.rand(n, n)
    fr = np.random.rand(n, 1)
    a = np.append(a1, fr, axis=1)

    start = time.time()
    res = np.linalg.solve(a1, fr)
    end = time.time()
    print("Solved by numpy ", end - start)

    start = time.time()
    gauss_jordan_solve(a)
    end = time.time()

    print("Solved by Gauss Jordan", end - start)
    print("Biggest difference between solutions:")
    print(max(res[:, 0] - a[:, n]))