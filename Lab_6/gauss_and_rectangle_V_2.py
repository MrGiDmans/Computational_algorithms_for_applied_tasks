import numpy as np
import math
import matplotlib.pyplot as plt
from sympy import symbols, integrate, exp

# ------------------------------
# 1. Исходные данные
# ------------------------------
a = 0
b = 2

def E0(x):
    return (x**2 - 1) * math.exp(-2 * x)

# ------------------------------
# 2. Метод прямоугольников (средних)
# ------------------------------
def rectangle_method(func, a, b, n):
    h = (b - a) / n
    s = 0
    for j in range(1, n + 1):
        xj = a + (j - 0.5) * h
        s += func(xj)
    return h * s

# ------------------------------
# 3. Метод Гаусса
# ------------------------------
GAUSS_TABLE = {
    5: {
        "t": np.array([-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459]),
        "A": np.array([0.2369268850, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268850])
    },
    7: {
        "t": np.array([-0.9491079123, -0.7415311856, -0.4058451514,
                        0.0,
                        0.4058451514, 0.7415311856, 0.9491079123]),
        "A": np.array([0.1294849662, 0.2797053915, 0.3818300505,
                        0.4179591837,
                        0.3818300505, 0.2797053915, 0.1294849662])
    }
}

def gauss_method(func, a, b, m):
    t = GAUSS_TABLE[m]["t"]
    A = GAUSS_TABLE[m]["A"]

    xm = 0.5 * (b + a)
    xr = 0.5 * (b - a)

    s = 0
    for i in range(m):
        s += A[i] * func(xm + xr * t[i])
    return xr * s

# ------------------------------
# 4. Основной блок
# ------------------------------
if __name__ == "__main__":
    # Точное значение интеграла
    x = symbols('x')
    exact_expr = integrate((x**2 - 1) * exp(-2 * x), (x, a, b))
    exact_value = float(exact_expr)
    print(f"Точное значение интеграла: {exact_value:.8f}")

    # --- Метод прямоугольников ---
    n_values = np.arange(5, 105, 5)
    rect_results = [rectangle_method(E0, a, b, n) for n in n_values]
    rect_errors = [abs(I - exact_value) for I in rect_results]

    print("\nМетод прямоугольников (сходимость):")
    for n, I in zip(n_values, rect_results):
        print(f"  n = {n:3d} -> I ≈ {I:.8f}, ошибка = {abs(I - exact_value):.2e}")

    # --- Метод Гаусса ---
    print("\nМетод Гаусса:")
    for m in [5, 7]:
        I_gauss = gauss_method(E0, a, b, m)
        print(f"  m = {m} -> I ≈ {I_gauss:.8f}, ошибка = {abs(I_gauss - exact_value):.2e}")

    # ------------------------------
    # 5. Графики
    # ------------------------------

    # --- (1) Подынтегральная функция ---
    x_vals = np.linspace(a, b, 400)
    y_vals = [(x**2 - 1) * np.exp(-2 * x) for x in x_vals]

    plt.figure(figsize=(8, 4))
    plt.plot(x_vals, y_vals, 'b-', linewidth=2)
    plt.title("Подынтегральная функция E₀(x) = (x² - 1)e^{-2x}")
    plt.xlabel("x")
    plt.ylabel("E₀(x)")
    plt.grid(True)
    plt.axhline(0, color='black', linewidth=0.8)
    plt.show()

    # --- (2) Зависимость ошибки от числа узлов ---
    plt.figure(figsize=(8, 4))
    plt.plot(n_values, rect_errors, 'ro-', linewidth=2, label="Ошибка метода прямоугольников")
    plt.yscale("log")
    plt.xlabel("Количество узлов n")
    plt.ylabel("Абсолютная ошибка |Iₙ - I_exact|")
    plt.title("Сходимость метода прямоугольников")
    plt.grid(True, which="both", linestyle="--")
    plt.legend()
    plt.show()
