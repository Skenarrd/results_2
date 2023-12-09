import os
import math
import csv
import scipy.special as sp
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
import wget

v = 3
url = 'https://jenyay.net/uploads/Student/Modelling/task_02.csv'
f = []
dx = 1000000 # шаг дискретизации

if (os.path.exists('task_02.csv') == 0):
    wget.download(url, r'task_02.csv')

with open ('task_02.csv', 'r') as data:
    reader = csv.reader(data, delimiter = ',')
    lines = list(reader)
arr = lines[v - 1]
#print(lines)

D = float(arr[1])
fmin = float(arr[2])
fmax = float(arr[3])
f = np.arange(fmin, fmax, dx)

L = const.c / f
r = D / 2
k = 2 * math.pi / L

def hn(n, x): return sp.spherical_jn(n, x) + 1j * sp.spherical_yn(n, x)
def bn(n, x): return (x * sp.spherical_jn(n - 1, x) - n * sp.spherical_jn(n, x)) / (x * hn(n - 1, x) - n * hn(n, x))
def an(n, x): return sp.spherical_jn(n, x) / hn(n, x)

arr_sum = [((-1) ** n) * (n + 0.5) * (bn(n, k * r) - an(n, k * r)) for n in range(1, 20)]
summ = np.sum(arr_sum, axis = 0)
sigma = (L ** 2) / math.pi * abs(summ) ** 2

with open("results/data2.csv", "w") as file:
    writer = csv.writer (file)
    for i in range(0, len(f)):
        writer.writerow([i + 1, f[i], sigma[i]])

plt.plot(f / 10e6, sigma)
plt.xlabel("f, МГц")
plt.ylabel("sigma, м^2")
plt.title('Задание 2')
plt.grid()
plt.show()