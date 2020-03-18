import numpy as np

N = 3


def LU(a):
    u = np.copy(a)
    l = np.zeros((N, N))

    for i in range(N):
        l[i, i] = 1
        j = i
        while j < N and u[j, i] == 0:
            j += 1
        if j == N:
            return False
        a[[j, i]] = a[[i, j]]  # swapping rows
        u[[j, i]] = u[[i, j]]
        u[i] /= u[i, i]
        a[i] /= a[i, i]
        for k in range(i+1, N):
            print(k)
            factor = u[k, i]/u[i, i]
            u[k] = u[k] - u[i] * factor
            l[k, i] = factor
            print(factor)
            print(u[k])
            print(u)
            print(l)
    print(np.dot(l, u))
    return l, u


a = np.array([[4.,2.,1.], [2.,2.,4.], [4.,1.,2.]])
LU(a)
l, u = LU(a)
print(np.dot(l,u))