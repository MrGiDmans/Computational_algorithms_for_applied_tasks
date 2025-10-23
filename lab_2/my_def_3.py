import math

def calculate_f(x: float, j: int, k: int, m: int) -> float:
    """
    Вычисляет значение функции f(x) = sh(x^j) - cos^k(pi*x^m).
    Параметры j, k, m должны быть в диапазоне [1, 4].

    Args:
        x: Значение переменной x.
        j: Показатель степени для x в гиперболическом синусе (1 ≤ j ≤ 4).
        k: Показатель степени для косинуса (1 ≤ k ≤ 4).
        m: Показатель степени для x внутри аргумента косинуса (1 ≤ m ≤ 4).

    Returns:
        Результат вычисления функции f(x).
    """
    if not (1 <= j <= 4):
        raise ValueError("j должен быть в диапазоне 1 ≤ j ≤ 4")
    if not (1 <= k <= 4):
        raise ValueError("k должен быть в диапазоне 1 ≤ k ≤ 4")
    if not (1 <= m <= 4):
        raise ValueError("m должен быть в диапазоне 1 ≤ m ≤ 4")

    hyperbolic_sin_term = math.sinh(x**j)
    cosine_arg = math.pi * (x**m)
    cos_value = math.cos(cosine_arg)
    cosine_term = cos_value**k

    return hyperbolic_sin_term - cosine_term


def calculate_f_derivative(x: float, j: int, k: int, m: int) -> float:
    term1 = j * (x**(j-1)) * math.cosh(x**j)
    term2 = k * m * math.pi * (x**(m-1)) * (math.cos(math.pi * x**m) ** (k-1)) * math.sin(math.pi * x**m)
    return term1 + term2


def bisection(func, a, b, j, k, m, tol=1e-6, max_iter=1000):
    fa = func(a, j, k, m)
    fb = func(b, j, k, m)
    if fa * fb > 0:
        raise ValueError("На концах отрезка значения функции одного знака, метод дихотомии неприменим")

    for _ in range(max_iter):
        c = (a + b) / 2
        fc = func(c, j, k, m)
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    raise RuntimeError("Метод дихотомии не сошёлся")


def newton(func, dfunc, x0, j, k, m, tol=1e-6, max_iter=1000):
    x = x0
    for _ in range(max_iter):
        fx = func(x, j, k, m)
        dfx = dfunc(x, j, k, m)
        if dfx == 0:
            raise ZeroDivisionError("Производная равна нулю")
        x_new = x - fx / dfx
        if abs(x_new - x) < tol:
            return x_new
        x = x_new
    raise RuntimeError("Метод Ньютона не сошёлся")
