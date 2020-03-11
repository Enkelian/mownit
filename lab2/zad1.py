import numpy
import scipy
import time
from numpy import array
import numpy as np
import kinds

# A[[row_1, row_2]] = A[[row_2, row_1]]
# A[row] *= val
# A[row_1] -= A[row_2]
# np.any(A[row])

N = 5


def scale(A):
    for i in range(N):
        A[i] /= np.amax(A[i])


def gauss_jordan_solve(A):
    scale(A)
    for i in range(N):
        j = i
        while j < N and A[j, i] == 0:
            j += 1
        if j == N:
            return False
        A[[j, i]] = A[[i, j]]   #swapping rows
        A[i] *= (1 / A[i, i])
        for k in range(i + 1, N):
            A[k] -= A[i] * A[k, i]
            A[k, i] = 0
        for k in range(i-1, -1, -1):
            A[k] -= A[i] * A[k, i]
            A[k, i] = 0

    print(A)
    # for i in range(N - 1, -1, -1):
    #     for j in range(0, i):
    #         A[j] -= (A[i] * A[j, i])
    # print(A[:, N])


A1 = np.random.rand(N, N)
fr = np.random.rand(N, 1)
A = np.append(A1, fr, axis=1)

start = time.time()
res = np.linalg.solve(A1, fr)
end = time.time()
print("Solved by numpy ", end-start)

start = time.time()
gauss_jordan_solve(A)
end = time.time()

print("Solved by Gauss Jordan", end-start)

# print(res[:, 0] - A[:, N])