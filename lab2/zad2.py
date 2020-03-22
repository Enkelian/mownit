import numpy as np
import scipy.linalg


def LU(a):
    n = len(a)
    u = np.copy(a)
    l = np.zeros((n, n))
    u = u.astype(float)
    l = l.astype(float)
    for i in range(n):
        l[i, i] = 1
        for k in range(i + 1, n):
            factor = u[k, i] / u[i, i]
            u[k] = u[k] - u[i] * factor
            l[k, i] = factor
    return l, u


def LUP(a):
    n = len(a)
    u = np.copy(a)
    l = np.zeros((n, n))
    p = np.zeros((n, n))
    np.fill_diagonal(p, 1)
    u = u.astype(float)
    l = l.astype(float)
    p = p.astype(float)

    for i in range(n):  # scaling
        p[i] = p[i] / np.max(u[i])
        u[i] = u[i] / np.max(u[i])

    for i in range(n):  # partial pivoting
        j = i
        max = u[i, i]
        max_ind = i
        while j < n:
            if u[j, i] > max:
                max = u[j, i]
                max_ind = j
            j += 1
        u[[max_ind, i]] = u[[i, max_ind]]
        p[[max_ind, i]] = p[[i, max_ind]]
        l[[max_ind, i]] = l[[i, max_ind]]

        for k in range(i + 1, n):
            factor = u[k, i] / u[i, i]
            u[k] = u[k] - u[i] * factor
            u[k, i] = 0
            l[k, i] = factor
    np.fill_diagonal(l, 1)
    return l, u, p


def exec_LUP_rand(n):
    a = np.random.randint(20, size=(n, n))
    a.astype(int)
    l, u, p = LUP(a)
    print(max(list(map(max, np.dot(p, a) - np.dot(l, u)))))


exec_LUP_rand(100)