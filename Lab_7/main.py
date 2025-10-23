import numpy as np

a = np.array([2, 3, 1.5, 2.5, 1, 4])
n = len(a)
W_volume = np.prod(2 * a)

alpha = np.array([-0.11668255, -1.90093714, -2.28172284])
beta  = np.array([3.74736003,  2.88284760,  1.59672290])

def rho(x):
    return np.sum(np.abs(x[:3] - alpha)**beta)

N_values = [10**3, 10**4, 10**5, 10**6]

for N in N_values:
    X = np.random.uniform(-a, a, size=(N, n))
    mask = np.sum((X / a)**2, axis=1) <= 1
    M = mask.sum()
    X_in = X[mask]
    if M == 0:
        print(f"N={N}: внутри нет точек (M=0)")
        continue

    mean_rho_in = np.mean([rho(x) for x in X_in])
    # правильная оценка интеграла
    I_est = W_volume * (M / N) * mean_rho_in
    # оценка объёма V
    V_est = W_volume * (M / N)

    print(f"N={N:7d}  M={M:6d}  M/N={M/N:.6f}  mean_rho_in={mean_rho_in:.6f}  I_est={I_est:.6f}  V_est={V_est:.6f}")


# N: Общее число испытаний (точек).
# M: Число точек, попавших внутрь гиперэллипсоида.
# M/N: Оценка вероятности попадания в область V. 
# mean_rho_in: Оценка среднего значения p внутри области V.
# I_est: Оценка значения интеграла I. 
# V_est: Оценка объема области V.