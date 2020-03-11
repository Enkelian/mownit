import numpy as np

N = 4


def countU(A):
    U = np.array(A)
    L = np.zeros((N, N))
    for i in range(N):
        L[i,i] = 1
        j = i
        while j < N and U[j, i] == 0:
            j += 1
        U[[j, i]] = U[[i, j]]  # swapping rows
        U[i] *= (1 / U[i, i])
        for k in range(i + 1, N):
            U[k] -= U[i] * U[k, i]
            U[k, i] = 0
        for k in range(i):
            L[k, i] = U[k, i]/U[i, i]
    print()
    print(U)
    return U



A1 = np.random.rand(N, N)
# L = countL(A1)
U = countU(A1)
# print(L*U - A1)