import numpy as np

# -----------------------------
# ПАРАМЕТРЫ ВАРИАНТА
# -----------------------------
n = 5       # размерность системы (можно 10, 15, 20)
q = 2       # параметр из условия
np.set_printoptions(precision=6, suppress=True)

# -----------------------------
# ГЕНЕРАЦИЯ МАТРИЦЫ A и ВЕКТОРА b
# -----------------------------
A = np.zeros((n, n), dtype=float)
b = np.zeros(n, dtype=float)

for i in range(n):
    for j in range(n):
        if i == j:
            A[i, j] = 10 * (i + 1) ** (n / 2)
        else:
            sign = (-1) ** (i + j)  # чередуем знаки
            A[i, j] = sign * 1e-3 * ((i + 1) / (j + 1)) ** (1 / q)
    b[i] = 9 * (i + 1) ** (n / 2)

print("Матрица A:\n", A)
print("Вектор b:\n", b)

# -----------------------------
# РЕШЕНИЕ МЕТОДОМ ФАКТОРИЗАЦИИ (LU)
# -----------------------------
x_lu = np.linalg.solve(A, b)
print("\nРешение методом LU:\n", x_lu)

# -----------------------------
# РЕШЕНИЕ МЕТОДОМ ЗЕЙДЕЛЯ
# -----------------------------
def gauss_seidel(A, b, eps=1e-10, max_iter=10000):
    n = len(A)
    x = np.zeros(n)
    for k in range(max_iter):
        x_old = x.copy()
        for i in range(n):
            s1 = np.dot(A[i, :i], x[:i])
            s2 = np.dot(A[i, i + 1:], x_old[i + 1:])
            x[i] = (b[i] - s1 - s2) / A[i, i]
        if np.linalg.norm(x - x_old, ord=np.inf) < eps:
            print(f"\nМетод Зейделя сошёлся за {k + 1} итераций.")
            return x
    print("⚠ Не сошёлся за указанное число итераций")
    return x

x_gs = gauss_seidel(A, b)

print("\nРешение методом Зейделя:\n", x_gs)

# -----------------------------
# ПРОВЕРКА НЕВЯЗКИ
# -----------------------------
r_lu = np.dot(A, x_lu) - b
r_gs = np.dot(A, x_gs) - b

print("\nНевязка LU:", np.linalg.norm(r_lu))
print("Невязка Зейделя:", np.linalg.norm(r_gs))
