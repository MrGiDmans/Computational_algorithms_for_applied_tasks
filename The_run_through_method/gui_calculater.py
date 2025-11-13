import tkinter as tk
from tkinter import messagebox
import numpy as np


# --- Метод прогонки (Томаса) ---
def thomas_method(a, b, c, d):
    n = len(b)
    alpha = np.zeros(n)
    beta = np.zeros(n)
    x = np.zeros(n)

    # Прямая прогонка
    alpha[0] = -c[0] / b[0]
    beta[0] = d[0] / b[0]
    for i in range(1, n):
        denom = b[i] + a[i] * alpha[i - 1]
        if abs(denom) < 1e-12:
            raise ValueError("Нулевой знаменатель в прямой прогонке")
        alpha[i] = -c[i] / denom if i < n - 1 else 0
        beta[i] = (d[i] - a[i] * beta[i - 1]) / denom

    # Обратная прогонка
    x[-1] = beta[-1]
    for i in range(n - 2, -1, -1):
        x[i] = alpha[i] * x[i + 1] + beta[i]

    return x


# --- GUI ---
class TDMA_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Метод прямой прогонки — трёхдиагональная система")

        self.n = 5  # Размер системы
        self.entries_A = []  # Поля для матрицы A
        self.entries_b = []  # Поля для вектора b
        self.result_labels = []  # Отображение X

        self.create_matrix_inputs()
        self.create_buttons()

    def create_matrix_inputs(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        # Заголовки
        tk.Label(frame, text="Матрица A", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=self.n)
        tk.Label(frame, text="", width=1).grid(row=0, column=self.n)  # Разделитель
        tk.Label(frame, text="Вектор b", font=("Arial", 10, "bold")).grid(row=0, column=self.n + 1)

        # Пример данных
        default_A = [
            [8, -2, 0, 0, 0],
            [-1, 5, 3, 0, 0],
            [0, 7, -5, -9, 0],
            [0, 0, 4, 7, 9],
            [0, 0, 0, -5, 8],
        ]
        default_b = [-7, 6, 9, -8, 5]

        # Матрица A и вектор b
        for i in range(self.n):
            row_entries = []
            for j in range(self.n):
                e = tk.Entry(frame, width=5, justify="center", font=("Consolas", 10))
                e.grid(row=i + 1, column=j, padx=2, pady=2)
                e.insert(0, str(default_A[i][j]))
                row_entries.append(e)
            self.entries_A.append(row_entries)

            # Вертикальный разделитель между A и b
            separator = tk.Label(frame, text="|", font=("Arial", 10, "bold"))
            separator.grid(row=i + 1, column=self.n, padx=5)

            # Вектор b
            e_b = tk.Entry(frame, width=6, justify="center", font=("Consolas", 10))
            e_b.grid(row=i + 1, column=self.n + 1, padx=5)
            e_b.insert(0, str(default_b[i]))
            self.entries_b.append(e_b)

        # Разделитель
        tk.Label(frame, text="").grid(row=self.n + 1, column=0)

        # Блок вывода результата
        tk.Label(frame, text="Решение X:", font=("Arial", 10, "bold")).grid(row=self.n + 2, column=0, columnspan=self.n + 2)
        for i in range(self.n):
            lbl = tk.Label(frame, text=f"x{i+1} = ?", width=10, font=("Consolas", 10))
            lbl.grid(row=self.n + 3, column=i, padx=3, pady=3)
            self.result_labels.append(lbl)

    def create_buttons(self):
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Решить методом прогонки", command=self.solve).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить", command=self.clear_results).pack(side=tk.LEFT, padx=5)

    def solve(self):
        try:
            A = np.zeros((self.n, self.n))
            b = np.zeros(self.n)

            for i in range(self.n):
                for j in range(self.n):
                    A[i, j] = float(self.entries_A[i][j].get())
                b[i] = float(self.entries_b[i].get())

            # Проверка на трёхдиагональность
            for i in range(self.n):
                for j in range(self.n):
                    if abs(i - j) > 1 and A[i, j] != 0:
                        raise ValueError("Матрица не трёхдиагональная!")

            # Извлечение диагоналей
            a = np.array([A[i, i - 1] if i > 0 else 0 for i in range(self.n)])
            main = np.array([A[i, i] for i in range(self.n)])
            c = np.array([A[i, i + 1] if i < self.n - 1 else 0 for i in range(self.n)])

            x = thomas_method(a, main, c, b)

            for i, lbl in enumerate(self.result_labels):
                lbl.config(text=f"x{i+1} = {x[i]:.5f}")

        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_results(self):
        for lbl in self.result_labels:
            lbl.config(text=f"x? = ?")


if __name__ == "__main__":
    root = tk.Tk()
    app = TDMA_GUI(root)
    root.geometry("600x400")
    root.mainloop()
