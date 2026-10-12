import numpy as np

# Метод прогонки (решение трёхдиагональной системы)
def progonka(A, B, C, F):
    n = len(C)
    al, be = np.zeros(n), np.zeros(n)
    
    # Прямой ход
    al[0], be[0] = B[0]/C[0], F[0]/C[0]
    for i in range(1, n):
        d = C[i] - A[i]*al[i-1]
        if i < n-1:
            al[i] = B[i]/d
        be[i] = (F[i] + A[i]*be[i-1])/d
    
    # Обратный ход
    x = np.zeros(n)
    x[-1] = be[-1]
    for i in range(n-2, -1, -1):
        x[i] = al[i]*x[i+1] + be[i]
    return x

# Метод простых итераций
def iter(A, b, eps=0.001):
    n = len(b)
    B = np.eye(n) - A / np.diag(A)[:, None]  # матрица перехода
    c = b / np.diag(A)                        # свободный вектор
    
    x = c.copy()
    k = 0
    q = np.max(np.sum(np.abs(B), axis=1))    # норма матрицы B
    
    while True:
        x_new = B @ x + c
        k += 1
        if np.max(np.abs(x_new - x)) < (1-q)/q * eps:
            return x_new, k
        x = x_new

# Проверка метода прогонки
print("Прогонка:", progonka(
    np.array([0, 1, 1.]),
    np.array([1, 1, 0.]),
    np.array([-2, -3, -2.]),
    np.array([-4, -9, -8.])
))

# Проверка метода итераций
x, k = iter(
    np.array([[10, -1, 2], [-1, 11, -1], [2, -1, 10.]]),
    np.array([6, 25, -11.])
)
print("Итерации:", x, "| шагов:", k)
