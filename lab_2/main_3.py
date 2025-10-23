import math
import csv
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from my_def_3 import calculate_f, calculate_f_derivative, newton, bisection


# ---------- Генерация значений ----------
def generate_values(j: int, k: int, m: int, step: float = 0.01):
    values = []
    x = 0.0
    while x <= 1.0:
        fx = calculate_f(x, j, k, m)
        values.append((x, fx))
        x += step
    return values


# ---------- Сохранение в CSV ----------
def save_to_csv(filename: str, values: list):
    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["x", "f(x)"])
        writer.writerows(values)


# ---------- Построение графика в окне ----------
def show_graph_window(values, root_bisection=None, root_newton=None):
    win = tk.Toplevel()
    win.title("График функции и корни")

    # создаём фигуру matplotlib
    fig, ax = plt.subplots(figsize=(6, 4))
    xs, ys = zip(*values)
    ax.plot(xs, ys, label="f(x)", color="blue")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")

    if root_bisection is not None:
        ax.scatter(root_bisection, 0, color="red", label="Корень (бисекция)")
    if root_newton is not None:
        ax.scatter(root_newton, 0, color="green", label="Корень (Ньютон)")

    ax.set_title("График функции f(x)")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()
    ax.grid(True)

    # вставляем график в tkinter
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    # подпись с корнями
    text = ""
    if root_bisection is not None:
        text += f"Корень (бисекция): {root_bisection:.6f}\n"
    if root_newton is not None:
        text += f"Корень (Ньютон): {root_newton:.6f}"

    label = tk.Label(win, text=text, font=("Arial", 12), justify="left")
    label.pack(pady=5)


# ---------- Основная функция ----------
def run_calculation(j, k, m, step):
    try:
        j, k, m = int(j), int(k), int(m)
        step = float(step)
        if not (1 <= j <= 4 and 1 <= k <= 4 and 1 <= m <= 4):
            raise ValueError("j, k, m должны быть в диапазоне 1–4")
        if step <= 0 or step > 1:
            raise ValueError("Шаг должен быть в диапазоне (0, 1]")

        values = generate_values(j, k, m, step)
        save_to_csv("function_values.csv", values)

        root_bisect = bisection(calculate_f, 0, 1, j, k, m)
        save_to_csv("root_bisection.csv", [(root_bisect, calculate_f(root_bisect, j, k, m))])

        root_newton = newton(calculate_f, calculate_f_derivative, 0.5, j, k, m)
        save_to_csv("root_newton.csv", [(root_newton, calculate_f(root_newton, j, k, m))])

        # показываем окно с графиком и корнями
        show_graph_window(values, root_bisection=root_bisect, root_newton=root_newton)

    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


# ---------- Интерфейс ----------
def create_gui():
    root = tk.Tk()
    root.title("Поиск корня функции")

    tk.Label(root, text="Параметр j:").grid(row=0, column=0, padx=5, pady=5)
    combo_j = ttk.Combobox(root, values=[1, 2, 3, 4], state="readonly")
    combo_j.current(0)
    combo_j.grid(row=0, column=1)

    tk.Label(root, text="Параметр k:").grid(row=1, column=0, padx=5, pady=5)
    combo_k = ttk.Combobox(root, values=[1, 2, 3, 4], state="readonly")
    combo_k.current(0)
    combo_k.grid(row=1, column=1)

    tk.Label(root, text="Параметр m:").grid(row=2, column=0, padx=5, pady=5)
    combo_m = ttk.Combobox(root, values=[1, 2, 3, 4], state="readonly")
    combo_m.current(0)
    combo_m.grid(row=2, column=1)

    tk.Label(root, text="Шаг:").grid(row=3, column=0, padx=5, pady=5)
    entry_step = tk.Entry(root)
    entry_step.insert(0, "0.01")
    entry_step.grid(row=3, column=1)

    btn = tk.Button(root, text="Построить график и найти корни",
                    command=lambda: run_calculation(combo_j.get(), combo_k.get(), combo_m.get(), entry_step.get()))
    btn.grid(row=4, column=0, columnspan=2, pady=10)

    root.mainloop()


if __name__ == "__main__":
    create_gui()
