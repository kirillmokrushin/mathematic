import numpy as np
import time

def lu_decomposition(A):
    n = len(A)
    U = A.copy().astype(float)
    L = np.eye(n)
    for k in range(n - 1):
        for i in range(k + 1, n):
            m = U[i, k] / U[k, k]
            L[i, k] = m
            U[i, k:] -= m * U[k, k:]
    return L, U

def forward_substitution(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y

def backward_substitution(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i+1:] @ x[i+1:]) / U[i, i]
    return x

def solve_lu(L, U, b):
    return backward_substitution(U, forward_substitution(L, b))

def gauss(A, b):
    A = A.copy().astype(float)
    b = b.copy().astype(float)
    n = len(b)
    for k in range(n - 1):
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]
    return backward_substitution(A, b)

A = np.array([[2, 1, 1], [4, 3, 3], [8, 7, 9]], dtype=float)
B = [np.array([4, 10, 24], dtype=float),
     np.array([1, 2, 3], dtype=float),
     np.array([3, 7, 19], dtype=float)]

start = time.perf_counter()
for b in B:
    gauss(A, b)
time_gauss = time.perf_counter() - start

start = time.perf_counter()
L, U = lu_decomposition(A)
solutions = [solve_lu(L, U, b) for b in B]
time_lu = time.perf_counter() - start

print("Матрица L:\n", L)
print("\nМатрица U:\n", U)
print("\nПроверка A = L * U:\n", L @ U)
print("\nРешения систем:")
for b, x in zip(B, solutions):
    print(f"\nb = {b}\nx = {x}")
print(f"\nВремя Гаусса: {time_gauss}")
print(f"Время LU: {time_lu}")
print(f"Выигрыш: {time_gauss / time_lu}")
