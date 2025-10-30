import numpy as np
import random
import math

# --- КОНСТАНТЫ И ПАРАМЕТРЫ ЗАДАЧИ ---
N = 6     # Размер матрицы [cite: 31]
P = 3     # Параметр p [cite: 31]
Q = 2     # Параметр q [cite: 31]
B = 0.05  # Параметр b [cite: 31]

EPSILON = 0.001  # Заданная погрешность [cite: 58]
K_MAX = 100      # Максимальное число итераций [cite: 57]

def create_matrix_a(n, p, q, b):
    """
    Создает квадратную матрицу А размера n*n по формулам Варианта 3.
    Индексы i, j в формулах идут от 1 до n.
    """
    A = np.zeros((n, n))
    
    # Для удобства переводим параметры в float для расчетов
    p_float = float(p)
    q_float = float(q)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if i == j:
                # Диагональные элементы: a_ii = 10 * i^(p/2)
                A[i-1, j-1] = 10 * (i ** (p_float / 2))
            else:
                # Недиагональные элементы: a_ij = b * ((i/j)^p + (j/i)^p)^(1/q)
                term1 = (i / j) ** p_float
                term2 = (j / i) ** p_float
                A[i-1, j-1] = b * ((term1 + term2) ** (1 / q_float))
                
    return A

def power_method(A, epsilon, k_max):
    """
    Реализует степенной метод для нахождения максимального по модулю 
    собственного значения.
    """
    n = A.shape[0]
    
    # 1. Выбор начального вектора x^(0) (случайный, равномерно в (0, 1)) [cite: 53]
    # Используем numpy.random.rand для создания вектора-столбца.
    x_k_minus_1 = np.random.rand(n, 1) 
    lambda_k = 0.0
    
    for k in range(1, k_max + 1):
        
        # --- Шаг 12 (Итерационный процесс) [cite: 67, 71] ---
        
        # 1. Нормирование предыдущего вектора x^(k-1)
        # ||x^(k-1)|| = sqrt(<x^(k-1), x^(k-1)>)
        norm_x = np.linalg.norm(x_k_minus_1)
        e_k_minus_1 = x_k_minus_1 / norm_x  # e_1^(k-1) = x^(k-1) / ||x^(k-1)||
        
        # 2. Умножение: x^(k) = A * e_1^(k-1)
        x_k = A @ e_k_minus_1
        
        # 3. Вычисление нового приближения собственного значения (Скалярное произведение)
        # lambda_1^(k) = <x^(k), e_1^(k-1)>
        lambda_k_new = (x_k.T @ e_k_minus_1)[0, 0]
        
        # --- Шаг 13 (Проверка условия остановки) [cite: 78, 79] ---
        
        # Разница между текущим и предыдущим lambda
        diff_lambda = abs(lambda_k_new - lambda_k)
        
        if diff_lambda < epsilon:
            # Условие сходимости выполнено
            return lambda_k_new, x_k, k, "Сходимость достигнута"

        lambda_k = lambda_k_new
        x_k_minus_1 = x_k # Переход к следующей итерации
    
    # Если цикл закончился по k_max [cite: 58]
    return lambda_k, x_k, k_max, "k_max достигнут"


# --- ОСНОВНАЯ ЧАСТЬ ПРОГРАММЫ ---
if __name__ == "__main__":
    
    # 1. Инициализация и создание матрицы
    A = create_matrix_a(N, P, Q, B)
    
    print(f"--- Задание № 9: Степенной метод (Вариант 3) ---")
    print(f"Параметры: N={N}, P={P}, Q={Q}, B={B}, Epsilon={EPSILON}, K_MAX={K_MAX}")
    print("\n--- Исходная матрица A: ---")
    # Используем numpy.set_printoptions для форматирования вывода матрицы
    with np.printoptions(precision=4, suppress=True):
        print(A)
    print("--------------------------------------\n")
    
    # 2. Выполнение степенного метода
    max_eigenvalue, max_eigenvector, iterations, status = power_method(A, EPSILON, K_MAX)
    
    # 3. Вывод результатов [cite: 104, 105]
    print(f"--- Результаты решения: ---")
    print(f"Статус завершения: {status}")
    print(f"Число итераций k: {iterations}")
    print(f"Максимальное собственное значение λ_max: {max_eigenvalue:.8f}")
    print(f"\nСоответствующий собственный вектор x (нормированный на последнем шаге):")
    # Последний x_k уже является приближением собственного вектора (не нормированным)
    # Нормируем его для вывода
    final_eigenvector = max_eigenvector / np.linalg.norm(max_eigenvector)
    with np.printoptions(precision=6, suppress=True):
        print(final_eigenvector.flatten())