import numpy
import matplotlib.pyplot as plt
import math
import time

N = 10000000
v = 0.53125
t = []
err = []
x = []


def countErr(k, sum):
    return abs(abs((k + 1) * v - sum) / ((k + 1) * v))


def sumRec(tab, l, r):
    if l >= r:
        return numpy.float32(tab[l])
    if abs(l - r) == 1:
        return numpy.float32(tab[l]) + numpy.float32(tab[r])

    m = l + math.floor((r - l) / 2)

    return numpy.float32(sumRec(tab, l, m - 1)) + numpy.float32(sumRec(tab, m, r))


def sumPrimitive(t, err, x):
    sum = 0
    for i in range(0, N):
        sum = numpy.float32(sum) + t[i]
        if (i + 1) % 25000 == 0:
            err.append(countErr(i + 1, sum))
            x.append(i + 1)
    return sum


def printSummary(exact_sum, result, total_time):
    print("Blad bezwzgledny: " + str(abs(exact_sum - result)))
    print("Blad wzgledny: " + str(countErr(N-1, result)))
    print("Czas wykonania: " + str(total_time))


def kahan(t):
    sum = numpy.float32(0.0)
    err = numpy.float32(0.0)

    for i in range(0, N):
        y = numpy.float32(numpy.float32(t[i]) - numpy.float32(err))
        temp = numpy.float32(sum + y)
        err = numpy.float32((temp - sum) - y)
        sum = temp
    return sum


for i in range(0, N):
    t.append(numpy.float32(v))

exact_sum = 5312500

start = time.time()
sum = sumPrimitive(t, err, x)
end = time.time()

print("Zwykle dodawanie:")
printSummary(exact_sum, sum, end - start)

start = time.time()
recursive_sum = sumRec(t, 0, N - 1)
end = time.time()

print("Dodawanie rekurencyjne:")
printSummary(exact_sum, recursive_sum, end - start)

t2 = []
small = 0.0000001
big = 1000000

for i in range(0, N):
    if i % 2 == 0:
        t2.append(numpy.float32(small))
    else:
        t2.append(numpy.float32(big))

exact_result = small*(N/2) + big*(N/2)

start = time.time()
recursive_sum = sumRec(t2, 0, N-1)
stop = time.time()

print("Dodawanie rekurencyjne o niezerowym bledzie")
print("Blad bezwzgledny: " + str(abs(exact_result - recursive_sum)))
print("Blad wzgledny: " + str((exact_result - recursive_sum)/exact_result))
print("Czas wykonania: " + str(stop - start))

plt.plot(x, err, "ro")
plt.show()

start = time.time()
kahan_sum = kahan(t)
stop = time.time()
print("Kahan")
print("Blad bezwzgledny: " + str(abs(exact_sum - kahan_sum)))
print("Blad wzgledny: " + str((exact_sum - kahan_sum)/exact_sum))
print("Czas wykonania: " + str(stop - start))

start = time.time()
kahan_sum = kahan(t2)
stop = time.time()

print("Kahan")
print("Blad bezwzgledny: " + str(abs(exact_result - kahan_sum)))
print("Blad wzgledny: " + str((exact_result - kahan_sum)/exact_result))
print("Czas wykonania: " + str(stop - start))


