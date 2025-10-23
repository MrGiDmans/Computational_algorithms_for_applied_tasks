import math
import csv
import matplotlib.pyplot as plt

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


# ---------- Построение графика ----------
def plot_graph(values: list):
    xs, ys = zip(*values)
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="f(x)", color="blue")
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")
    plt.title("График функции f(x)")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    # Пример: j=2, k=2, m=1
    j, k, m = 2, 2, 1
    values = generate_values(j, k, m, step=0.01)

    # Сохранение
    save_to_csv("function_values.csv", values)

    # График
    plot_graph(values)