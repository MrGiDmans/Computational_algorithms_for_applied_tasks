import numpy as np
import tkinter as tk
from tkinter import messagebox

class PoissonSolverGUI:
    """
    Графический интерфейс для численного решения задачи Дирихле
    для уравнения Пуассона методом Якоби.
    """
    
    # --- Параметры по умолчанию ---
    N = 10  # Размер сетки N x N
    DEFAULT_EPSILON = 0.0001
    
    def __init__(self, master):
        self.master = master
        master.title("Метод Якоби для Уравнения Пуассона (h1=h2)")
        
        # Инициализация матриц и состояния
        self.u_old, self.u_new = self._initialize_grid(self.N)
        self.iteration = 0
        
        # Переменные для отслеживания GUI
        self.max_diff_var = tk.StringVar(value="Max Diff: N/A")
        self.iteration_var = tk.StringVar(value=f"Итерация: {self.iteration}")
        self.epsilon_entry = None
        self.matrix_labels_old = []
        self.matrix_labels_new = []

        # --- Создание элементов GUI ---
        self._create_widgets(master)
        self._update_display()

    def _initialize_grid(self, N):
        """Создает и инициализирует сетку N x N с граничными условиями."""
        
        # u_old - начальная матрица/значения предыдущего шага
        u_old = np.zeros((N, N), dtype=float)
        # u_new - матрица для записи новых значений на текущем шаге
        u_new = np.zeros((N, N), dtype=float)
        
        # Задаем Граничные Условия (Boundary Conditions)
        # Верхняя граница (строка 0) = 100.0
        u_old[0, :] = 100.0
        u_new[0, :] = 100.0
        
        # Остальные границы (Нижняя, Левая, Правая) = 0.0
        u_old[-1, :] = 0.0
        u_new[-1, :] = 0.0
        u_old[:, 0] = 0.0
        u_new[:, 0] = 0.0
        u_old[:, -1] = 0.0
        u_new[:, -1] = 0.0
        
        # Корректировка углов (чтобы не было перезаписи, хотя это не критично)
        u_old[0, 0] = 100.0  # Верхний левый
        u_old[0, -1] = 100.0 # Верхний правый
        
        # Заполняем u_new начальным приближением (копируем u_old), 
        # чтобы начать итерации
        u_new = u_old.copy()
        
        return u_old, u_new

    def _create_widgets(self, master):
        """Создает все элементы интерфейса."""
        
        # --- 1. Панель управления ---
        control_frame = tk.Frame(master)
        control_frame.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        
        # Поле для Epsilon
        tk.Label(control_frame, text="Эпсилон (ε):").pack(side=tk.LEFT, padx=5)
        self.epsilon_entry = tk.Entry(control_frame, width=10)
        self.epsilon_entry.insert(0, str(self.DEFAULT_EPSILON))
        self.epsilon_entry.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для шага
        step_button = tk.Button(control_frame, text="Сделать 1 Шаг", command=self._apply_step)
        step_button.pack(side=tk.LEFT, padx=15)
        
        # Кнопка для сброса и изменения весов
        reset_button = tk.Button(control_frame, text="Сброс/Изменить BC", command=self._reset_grid)
        reset_button.pack(side=tk.LEFT, padx=15)
        
        # Статус итерации
        tk.Label(control_frame, textvariable=self.iteration_var).pack(side=tk.LEFT, padx=15)
        tk.Label(control_frame, textvariable=self.max_diff_var).pack(side=tk.LEFT, padx=15)

        # --- 2. Две Матрицы ---
        
        # Матрица 1: u_old (Изначальная/Предыдущий шаг)
        frame_old = tk.LabelFrame(master, text="Матрица 'u_old' (Предыдущий шаг / Исходная)", padx=5, pady=5)
        frame_old.grid(row=1, column=0, padx=10, pady=10)
        self._draw_matrix_labels(frame_old, self.matrix_labels_old)

        # Матрица 2: u_new (Текущий шаг)
        frame_new = tk.LabelFrame(master, text="Матрица 'u_new' (Текущий шаг / Новые значения)", padx=5, pady=5)
        frame_new.grid(row=1, column=1, padx=10, pady=10)
        self._draw_matrix_labels(frame_new, self.matrix_labels_new)

    def _draw_matrix_labels(self, frame, label_list):
        """Создает пустые Label для отображения данных матрицы."""
        for i in range(self.N):
            row_labels = []
            for j in range(self.N):
                label = tk.Label(frame, text="0.00", width=5, relief="solid", borderwidth=1)
                label.grid(row=i, column=j, padx=1, pady=1)
                row_labels.append(label)
            label_list.append(row_labels)

    def _update_display(self):
        """Обновляет текст в Label'ах на основе значений массивов u_old и u_new."""
        
        # Обновление u_old
        for i in range(self.N):
            for j in range(self.N):
                val = self.u_old[i, j]
                self.matrix_labels_old[i][j].config(text=f"{val:.2f}")

        # Обновление u_new
        for i in range(self.N):
            for j in range(self.N):
                val = self.u_new[i, j]
                self.matrix_labels_new[i][j].config(text=f"{val:.2f}")

        # Обновление номера итерации
        self.iteration_var.set(f"Итерация: {self.iteration}")

    def _jacobi_step(self):
        """Выполняет один шаг итерации Якоби и возвращает max_diff."""
        
        # В методе Якоби мы ВСЕГДА используем старые (u_old) значения для расчета 
        # всех новых (u_new) значений.
        
        max_diff = 0.0
        
        # Итерируем только по внутренним точкам (от 1 до N-2)
        # Граничные точки (0 и N-1) не изменяются.
        for i in range(1, self.N - 1):
            for j in range(1, self.N - 1):
                
                # --- Формула Якоби для h1=h2=h и f=0 ---
                # u_new[i,j] = 1/4 * (Сумма четырех соседей)
                
                sum_neighbors = (self.u_old[i+1, j] + # снизу
                                 self.u_old[i-1, j] + # сверху
                                 self.u_old[i, j+1] + # справа
                                 self.u_old[i, j-1])  # слева
                
                new_val = sum_neighbors / 4.0
                
                # Сохраняем новое значение в u_new
                self.u_new[i, j] = new_val
                
                # Рассчитываем и обновляем максимальную разницу
                diff = abs(new_val - self.u_old[i, j])
                if diff > max_diff:
                    max_diff = diff
                    
        return max_diff

    def _apply_step(self):
        """Обрабатывает нажатие кнопки "Сделать 1 Шаг"."""
        
        try:
            epsilon = float(self.epsilon_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Неверное значение Epsilon.")
            return

        if self.max_diff_var.get().startswith("Сходимость"):
            messagebox.showinfo("Готово", "Сходимость уже достигнута.")
            return
        
        # 1. Выполняем шаг итерации
        max_diff = self._jacobi_step()
        self.iteration += 1
        
        # 2. Обновляем старую матрицу (для следующего шага)
        # Это критически важный шаг для метода Якоби
        self.u_old = self.u_new.copy() 
        
        # 3. Обновляем статус
        self.max_diff_var.set(f"Max Diff: {max_diff:.6f}")
        
        # 4. Проверяем условие сходимости
        if max_diff < epsilon:
            self.max_diff_var.set(f"Сходимость (ε={epsilon:.4f}) достигнута!")
            messagebox.showinfo("Готово", f"Сходимость достигнута на итерации {self.iteration}!")
        
        # 5. Обновляем отображение GUI
        self._update_display()
        
    def _reset_grid(self):
        """Сбрасывает сетку к исходным граничным условиям."""
        
        # Переопределим граничные условия для наглядности (например, сделаем левую границу горячей)
        self.u_old, self.u_new = self._initialize_grid(self.N)
        
        # Новые условия: Верхняя 100, Левая 50, Остальные 0
        self.u_old[0, :] = 100.0
        self.u_new[0, :] = 100.0
        self.u_old[:, 0] = 50.0
        self.u_new[:, 0] = 50.0
        
        # Сброс счетчиков
        self.iteration = 0
        self.max_diff_var.set("Max Diff: N/A")
        
        # Обновление отображения
        self._update_display()
        messagebox.showinfo("Сброс", "Сетка сброшена. Новые BC: Верх=100, Лево=50, Остальное=0.")


if __name__ == '__main__':
    root = tk.Tk()
    app = PoissonSolverGUI(root)
    root.mainloop()