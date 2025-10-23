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
def plot_graph(values: list, root_bisection=None, root_newton=None):
    xs, ys = zip(*values)
    plt.figure(figsize=(8, 5))
    plt.plot(xs, ys, label="f(x)", color="blue")
    plt.axhline(0, color="black", linewidth=0.8, linestyle="--")

    if root_bisection is not None:
        plt.scatter(root_bisection, 0, color="red", label="Корень (бисекция)")
    if root_newton is not None:
        plt.scatter(root_newton, 0, color="green", label="Корень (Ньютон)")

    plt.title("График функции f(x)")
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.legend()
    plt.grid(True)
    plt.show()


# ---------- Функция безопасного ввода ----------
def input_value():
    def ask_param(name):
        while True:
            try:
                val = int(input(f"{name} (от 1 до 4): "))
                if 1 <= val <= 4:
                    return val
                else:
                    print("Ошибка: значение должно быть в диапазоне 1–4")
            except ValueError:
                print("Ошибка: нужно ввести число")
    print("Введите параметры функции:")
    j = ask_param("j")
    k = ask_param("k")
    m = ask_param("m")
    return j, k, m

if __name__ == "__main__":

    j, k, m = input_value()

    values = generate_values(j, k, m, step=0.001)

    save_to_csv("function_values.csv", values)

    root_bisect = bisection(calculate_f, 0, 1, j, k, m)
    save_to_csv("root_bisection.csv", [(root_bisect, calculate_f(root_bisect, j, k, m))])

    root_newton = newton(calculate_f, calculate_f_derivative, 0.5, j, k, m)
    save_to_csv("root_newton.csv", [(root_newton, calculate_f(root_newton, j, k, m))])

    plot_graph(values, root_bisection=root_bisect, root_newton=root_newton)
