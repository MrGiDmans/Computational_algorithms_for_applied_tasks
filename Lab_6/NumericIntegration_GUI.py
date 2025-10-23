#!/usr/bin/env python3
"""Numeric Integration GUI (Python 3.11)
Оконное приложение для вычисления ∫_a^b f(x) dx методом средних прямоугольников и квадратурой Гаусса.
Особенности:
- Поле ввода a, b и выражения функции (в виде обычного математического выражения, например: (x**2 - 1)*exp(-2*x) или (x^2-1)*e^{-2x})
- Отображение отформатированной строки функции (LaTeX) рядом с графиком
- Динамическое (реальное время с дебаунсом) обновление графиков при вводе
- График функции и зависимость ошибки метода прямоугольников от n
- Поддержка выбора m для формулы Гаусса (5 или 7 узлов)

Запуск:
    python3 NumericIntegration_GUI.py
Требования:
    pip install pyqt5 matplotlib sympy numpy

Примечание: в Linux/Windows/WSL приложение должно работать при наличии PyQt5.
"""

import sys
import math
import numpy as np
from functools import partial
from io import BytesIO

from PyQt5 import QtCore, QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from sympy import symbols, sympify, lambdify, latex, exp as sympy_exp

# --- Таблица узлов и весов для Гаусса (Лежандра) на [-1,1]
GAUSS_TABLE = {
    5: {
        "t": np.array([-0.9061798459, -0.5384693101, 0.0, 0.5384693101, 0.9061798459]),
        "A": np.array([0.2369268850, 0.4786286705, 0.5688888889, 0.4786286705, 0.2369268850])
    },
    7: {
        "t": np.array([-0.9491079123, -0.7415311856, -0.4058451514, 0.0, 0.4058451514, 0.7415311856, 0.9491079123]),
        "A": np.array([0.1294849662, 0.2797053915, 0.3818300505, 0.4179591837, 0.3818300505, 0.2797053915, 0.1294849662])
    }
}

# --- Вспомогательные численные методы ---

def rectangle_method(func, a, b, n):
    if n <= 0:
        raise ValueError("n должно быть положительным")
    h = (b - a) / n
    s = 0.0
    for j in range(1, n + 1):
        xj = a + (j - 0.5) * h
        s += func(xj)
    return h * s


def gauss_method(func, a, b, m):
    if m not in GAUSS_TABLE:
        raise ValueError("Поддерживаются m=5 или m=7")
    t = GAUSS_TABLE[m]["t"]
    A = GAUSS_TABLE[m]["A"]
    xm = 0.5 * (b + a)
    xr = 0.5 * (b - a)
    s = 0.0
    for i in range(m):
        s += A[i] * func(xm + xr * t[i])
    return xr * s

# --- GUI ---

class MplCanvas(FigureCanvas):
    def __init__(self, width=5, height=3, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        fig.tight_layout()


class IntegrationApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Численное интегрирование — GUI")
        self.resize(1000, 700)

        # --- Виджеты ввода ---
        self.a_input = QtWidgets.QLineEdit("0")
        self.b_input = QtWidgets.QLineEdit("2")
        self.func_input = QtWidgets.QLineEdit("(x**2 - 1)*exp(-2*x)")

        self.n_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.n_slider.setRange(5, 500)
        self.n_slider.setValue(50)
        self.n_label = QtWidgets.QLabel("n = 50")

        self.gauss_combo = QtWidgets.QComboBox()
        self.gauss_combo.addItems(["5", "7"])

        self.update_button = QtWidgets.QPushButton("Обновить")

        # Строка для вывода отформатированной функции
        self.formula_label = QtWidgets.QLabel()
        self.formula_label.setAlignment(QtCore.Qt.AlignCenter)
        self.formula_label.setMinimumHeight(60)

        # Canvas для графиков
        self.func_canvas = MplCanvas(width=6, height=4, dpi=100)
        self.error_canvas = MplCanvas(width=6, height=2.5, dpi=100)

        # Лэйауты
        controls_layout = QtWidgets.QGridLayout()
        controls_layout.addWidget(QtWidgets.QLabel("a:"), 0, 0)
        controls_layout.addWidget(self.a_input, 0, 1)
        controls_layout.addWidget(QtWidgets.QLabel("b:"), 0, 2)
        controls_layout.addWidget(self.b_input, 0, 3)
        controls_layout.addWidget(QtWidgets.QLabel("Функция f(x):"), 1, 0)
        controls_layout.addWidget(self.func_input, 1, 1, 1, 3)
        controls_layout.addWidget(QtWidgets.QLabel("Метод Гаусса m:"), 2, 0)
        controls_layout.addWidget(self.gauss_combo, 2, 1)
        controls_layout.addWidget(self.n_label, 3, 0)
        controls_layout.addWidget(self.n_slider, 3, 1, 1, 3)
        controls_layout.addWidget(self.update_button, 4, 0, 1, 4)

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.addLayout(controls_layout)
        main_layout.addWidget(self.formula_label)

        plots_split = QtWidgets.QSplitter(QtCore.Qt.Vertical)
        plots_widget = QtWidgets.QWidget()
        plots_layout = QtWidgets.QVBoxLayout()
        plots_layout.addWidget(self.func_canvas)
        plots_layout.addWidget(self.error_canvas)
        plots_widget.setLayout(plots_layout)
        plots_split.addWidget(plots_widget)

        main_layout.addWidget(plots_split)

        self.setLayout(main_layout)

        # --- Сигналы ---
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.setInterval(400)  # дебаунс 400 мс
        self.update_timer.setSingleShot(True)
        self.update_timer.timeout.connect(self._on_update_timer)

        self.func_input.textChanged.connect(self._trigger_update)
        self.a_input.textChanged.connect(self._trigger_update)
        self.b_input.textChanged.connect(self._trigger_update)
        self.n_slider.valueChanged.connect(self._on_n_change)
        self.gauss_combo.currentIndexChanged.connect(self._trigger_update)
        self.update_button.clicked.connect(self.update_all)

        # Начальное состояние
        self.current_lambda = None
        self.sympy_expr = None
        self.update_all()

    def _on_n_change(self, v):
        self.n_label.setText(f"n = {v}")
        self._trigger_update()

    def _trigger_update(self):
        # запускаем таймер-дебаунс, чтобы не перегружать при быстром наборе
        self.update_timer.start()

    def _on_update_timer(self):
        self.update_all()

    def parse_function(self, text):
        """Парсим выражение пользователя в безопасную символьную форму и возвращаем числовую функцию.
        Допускаются
        - x как переменная
        - exp(...), sin, cos, etc. (символьные)
        """
        x = symbols('x')
        # Попробуем заменить записи типа e^{-2x} на exp(-2*x) для удобства
        text = text.replace('^', '**')
        text = text.replace('e^', 'exp')
        try:
            expr = sympify(text, locals={"exp": sympy_exp})
        except Exception as e:
            raise ValueError(f"Ошибка при синтаксическом разборе функции: {e}")

        # Проверка на наличие x
        if not expr.free_symbols:
            # константа
            f = lambdify(x, expr, modules=["numpy", {"exp": np.exp}])
        else:
            f = lambdify(x, expr, modules=["numpy", {"exp": np.exp}])
        return expr, f

    def render_latex_to_pixmap(self, latex_str, fontsize=14):
        fig = Figure(figsize=(4, 0.6), dpi=100)
        ax = fig.add_subplot(111)
        ax.axis('off')
        ax.text(0.5, 0.5, r"$%s$" % latex_str, horizontalalignment='center', verticalalignment='center', fontsize=fontsize)
        fig.tight_layout()
        buf = BytesIO()
        fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', transparent=True)
        buf.seek(0)
        img = QtGui.QImage.fromData(buf.getvalue())
        pix = QtGui.QPixmap.fromImage(img)
        return pix

    def update_all(self):
        # Читаем входные данные
        a_text = self.a_input.text().strip()
        b_text = self.b_input.text().strip()
        func_text = self.func_input.text().strip()

        try:
            a = float(a_text)
            b = float(b_text)
        except Exception:
            self.show_error("Неверный формат a или b. Введите числовые значения.")
            return

        if a == b:
            self.show_error("a и b должны быть разными")
            return

        try:
            expr, f_numeric = self.parse_function(func_text)
        except ValueError as e:
            self.show_error(str(e))
            return

        # Сохраняем текущую функцию
        self.sympy_expr = expr
        self.current_lambda = f_numeric

        # Отображаем отформатированную формулу
        try:
            latex_str = latex(expr)
            pix = self.render_latex_to_pixmap(latex_str)
            self.formula_label.setPixmap(pix.scaled(self.formula_label.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation))
        except Exception:
            # fallback: показать исходную строку
            self.formula_label.setText(func_text)

        # Подготовка данных для графика функции
        xs = np.linspace(min(a, b), max(a, b), 500)
        try:
            ys = f_numeric(xs)
            # Если функция вернула скаляр (например константа), расширим
            if np.isscalar(ys):
                ys = np.full_like(xs, ys)
            ys = np.array(ys, dtype=float)
        except Exception as e:
            self.show_error(f"Ошибка при вычислении функции на сетке: {e}")
            return

        # Точное значение (символьная интеграция) -- для контроля
        try:
            x = symbols('x')
            from sympy import integrate
            exact_expr = integrate(self.sympy_expr, (x, a, b))
            exact_value = float(exact_expr)
        except Exception:
            exact_value = None

        # Метод прямоугольников: собираем для ряда n
        n_vals = np.arange(5, max(50, self.n_slider.value()), 5)
        rect_results = []
        rect_errors = []
        for n in n_vals:
            try:
                val = rectangle_method(lambda xx: float(f_numeric(xx)), a, b, int(n))
            except Exception:
                val = np.nan
            rect_results.append(val)
            if exact_value is not None and not np.isnan(val):
                rect_errors.append(abs(val - exact_value))
            else:
                rect_errors.append(np.nan)

        # Расчёт для выбранного n (слайдер)
        n_chosen = int(self.n_slider.value())
        try:
            rect_chosen = rectangle_method(lambda xx: float(f_numeric(xx)), a, b, n_chosen)
        except Exception as e:
            rect_chosen = np.nan

        # Метод Гаусса
        m = int(self.gauss_combo.currentText())
        try:
            gauss_val = gauss_method(lambda xx: float(f_numeric(xx)), a, b, m)
        except Exception as e:
            gauss_val = np.nan

        # --- Рисуем график функции ---
        ax = self.func_canvas.axes
        ax.clear()
        ax.plot(xs, ys, label='f(x)')
        ax.axhline(0, color='black', linewidth=0.7)
        ax.set_xlabel('x')
        ax.set_ylabel('f(x)')
        ax.set_title('Подынтегральная функция')
        # Отметим значения интегралов
        txt = []
        if not np.isnan(rect_chosen):
            txt.append(f"Rect(n={n_chosen}) = {rect_chosen:.8g}")
        if not np.isnan(gauss_val):
            txt.append(f"Gauss(m={m}) = {gauss_val:.8g}")
        if exact_value is not None:
            txt.append(f"Exact = {exact_value:.8g}")
        if txt:
            ax.text(0.02, 0.98, '\n'.join(txt), transform=ax.transAxes, verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        ax.legend()
        self.func_canvas.draw()

        # --- Рисуем график ошибки ---
        ax2 = self.error_canvas.axes
        ax2.clear()
        ax2.set_title('Ошибка метода прямоугольников')
        ax2.set_xlabel('n')
        ax2.set_ylabel('|I_n - I_exact|')
        ax2.set_yscale('log')
        ax2.plot(n_vals, rect_errors, marker='o')
        ax2.grid(True, which='both', linestyle='--', linewidth=0.5)
        self.error_canvas.draw()

        # Очистка ошибок в строке состояния
        self.clear_error()

    def show_error(self, message):
        self.formula_label.setText(f"Ошибка: {message}")

    def clear_error(self):
        pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    win = IntegrationApp()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
