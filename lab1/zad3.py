from numpy import float32
from numpy import float64
import pandas

def single(n_idx, s_idx, vals, asc):
    rng = range(0, N[n_idx]) if asc else range(N[n_idx] - 1, -1, -1)
    res = float32(0)
    for i in rng:
        res = res + float32(vals[s_idx][i])
    return res


def double(n_idx, s_idx, vals, asc):
    res = float64(0)
    rng = range(0, N[n_idx]) if asc else range(N[n_idx] - 1, -1, -1)
    for i in rng:
        res = res + float64(vals[s_idx][i])
    return res


N = [50, 100, 200, 500, 1000]
S = [2, 3.6667, 5, 7.2, 10]

DH = []
EH = []


for s_idx in range(0, 5):
    DH.append([])
    EH.append([])
    for k in range(0, N[4]):
        DH[s_idx].append(1 / (k+1) ** S[s_idx])
        EH[s_idx].append((-1) ** k * DH[s_idx][k])

dzetaAsc1 = []
dzetaDesc1 = []
etaAsc1 = []
etaDesc1 = []
dzetaAsc2 = []
dzetaDesc2 = []
etaAsc2 = []
etaDesc2 = []

for s_idx in range(0, 5):
    dzetaAsc1.append([])
    dzetaDesc1.append([])
    etaAsc1.append([])
    etaDesc1.append([])
    dzetaAsc2.append([])
    dzetaDesc2.append([])
    etaAsc2.append([])
    etaDesc2.append([])
    for n_idx in range(0, 5):
        dzetaAsc1[s_idx].append(single(n_idx, s_idx, DH, True))
        dzetaDesc1[s_idx].append(single(n_idx, s_idx, DH, False))
        etaAsc1[s_idx].append(single(n_idx, s_idx, EH, True))
        etaDesc1[s_idx].append(single(n_idx, s_idx, EH, False))
        dzetaAsc2[s_idx].append(double(n_idx, s_idx, DH, True))
        dzetaDesc2[s_idx].append(double(n_idx, s_idx, DH, False))
        etaAsc2[s_idx].append(double(n_idx, s_idx, EH, True))
        etaDesc2[s_idx].append(double(n_idx, s_idx, EH, False))


print(dzetaAsc1)
print(dzetaDesc1)
print(dzetaAsc2)
print(dzetaDesc2)

dzetaDiffs1 = []
for s_idx in range(0, 5):
    dzetaDiffs1.append([])
    for n_idx in range(0, 5):
        dzetaDiffs1[s_idx].append(dzetaAsc1[0][n_idx] - dzetaDesc1[0][n_idx])

print("Roznice ")
print(dzetaDiffs1)
