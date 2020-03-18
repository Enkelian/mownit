import numpy as np
import scipy.linalg
N = 3


def LU(a):
    u = np.copy(a)
    l = np.zeros((N, N))
    for i in range(N):
        l[i, i] = 1
        for k in range(i+1, N):
            factor = u[k, i]/u[i, i]
            u[k] = u[k] - u[i] * factor
            l[k, i] = factor
    print(np.dot(l, u))
    print(a)
    return l, u


def LUP(a):
    print(a)
    u = np.copy(a)
    l = np.zeros((N, N))
    p = np.zeros((N, N))
    np.fill_diagonal(p, 1)
    # np.fill_diagonal(l, 1)
    for i in range(N):
        j = i
        while j < N and u[j, i] == 0:
            j += 1
        if j == N:
            return False
        # a[[j, i]] = a[[i, j]]
        u[[j, i]] = u[[i, j]]
        p[[j, i]] = p[[i, j]]
        l[[j, i]] = l[[i,j]]
        j = i
        max = u[i, i]
        max_ind = i
        while j < N:
            if u[j, i] > max:
                max = u[j, i]
                max_ind = j
            j += 1
        # a[[max_ind, i]] = a[[i, max_ind]]  # swapping rows
        u[[max_ind, i]] = u[[i, max_ind]]
        p[[max_ind, i]] = p[[i, max_ind]]
        l[[max_ind, i]] = l[[i, max_ind]]
        for k in range(i + 1, N):
            factor = u[k, i] / u[i, i]
            u[k] = u[k] - u[i] * factor
            l[k, i] = factor
    np.fill_diagonal(l, 1)
    print(np.dot(p, a))
    print(np.dot(l, u))
    return l, u, p



a=np.random.randint(20, size=(N,N))
a.astype(int)
# a = np.array([[4.,2.,1.], [2.,2.,4.], [4.,1.,2.]])
# LU(a)
l, u, p= LUP(a)

