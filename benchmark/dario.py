#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# Roughly based on: http://stackoverflow.com/questions/11443302/compiling-numpy-with-openblas-integration

from __future__ import print_function
from time import time
import numpy as np

# Let's take the randomness out of random numbers (for reproducibility)
np.random.seed(0)

SIZE = 4096
A, B = np.random.random((SIZE, SIZE)), np.random.random((SIZE, SIZE))
C, D = np.random.random((SIZE * 128,)), np.random.random((SIZE * 128,))
E = np.random.random((int(SIZE / 2), int(SIZE / 4)))
F = np.random.random((int(SIZE / 2), int(SIZE / 2)))
F = np.dot(F, F.T)
G = np.random.random((int(SIZE / 2), int(SIZE / 2)))

# Matrix multiplication
N = 20
t = time()
for i in range(N):
    np.dot(A, B)
delta = time() - t
print('Dotted two %dx%d matrices in %0.2f s.' % (SIZE, SIZE, delta / N))
del A, B

# Vector multiplication
N = 5000
t = time()
for i in range(N):
    np.dot(C, D)
delta = time() - t
print('Dotted two vectors of length %d in %0.2f ms.' % (SIZE * 128, 1e3 * delta / N))
del C, D

# Singular Value Decomposition (SVD)
N = 3
t = time()
for i in range(N):
    np.linalg.svd(E, full_matrices = False)
delta = time() - t
print("SVD of a %dx%d matrix in %0.2f s." % (SIZE / 2, SIZE / 4, delta / N))
del E

# Cholesky Decomposition
N = 3
t = time()
for i in range(N):
    np.linalg.cholesky(F)
delta = time() - t
print("Cholesky decomposition of a %dx%d matrix in %0.2f s." % (SIZE / 2, SIZE / 2, delta / N))

# Eigendecomposition
t = time()
for i in range(N):
    np.linalg.eig(G)
delta = time() - t
print("Eigendecomposition of a %dx%d matrix in %0.2f s." % (SIZE / 2, SIZE / 2, delta / N))

print('')
print('This was obtained using the following Numpy configuration:')
np.__config__.show()
