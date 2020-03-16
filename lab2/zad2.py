import numpy as np

N = 3


def LU(a):
    u = np.copy(a)
    l = np.zeros((N, N))

    for i in range(N):
        l[i, i] = 1
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