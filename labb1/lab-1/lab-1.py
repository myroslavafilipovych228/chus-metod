import numpy as np
import matplotlib.pyplot as plt
import math


def f(x):
    """Функція для інтерполяції"""
    return math.sin(x)


def progonka(y, h, N, c):
    alfa = [0.0] * (N + 2)
    beta = [0.0] * (N + 2)
    hamma = [0.0] * (N + 2)
    delta = [0.0] * (N + 2)
    A = [0.0] * (N + 2)
    B = [0.0] * (N + 2)

    alfa[1] = hamma[1] = delta[1] = 0.0
    beta[1] = 1.0

    for i in range(2, N + 1):
        alfa[i] = h[i - 1]
        beta[i] = 2 * (h[i - 1] + h[i])
        hamma[i] = h[i]
        delta[i] = 3 * (((y[i] - y[i - 1]) / h[i]) - ((y[i - 1] - y[i - 2]) / h[i - 1]))

    hamma[N] = 0.0

    A[1] = -hamma[1] / beta[1]
    B[1] = delta[1] / beta[1]

    for i in range(2, N):
        denominator = alfa[i] * A[i - 1] + beta[i]
        A[i] = -hamma[i] / denominator
        B[i] = (delta[i] - alfa[i] * B[i - 1]) / denominator

    c[N] = (delta[N] - alfa[N] * B[N - 1]) / (alfa[N] * A[N - 1] + beta[N])

    for i in range(N, 1, -1):
        c[i - 1] = A[i - 1] * c[i] + B[i - 1]

    return c


def read_input_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()

        N = len(lines) - 1

        x = [0.0] * (N + 2)
        y = [0.0] * (N + 2)
        h = [0.0] * (N + 2)

        for i, line in enumerate(lines):
            if i <= N:
                parts = line.strip().split()
                if len(parts) >= 4:
                    j = int(parts[0])
                    x[i] = float(parts[1])
                    y[i] = float(parts[2])
                    h[i] = float(parts[3])

        return N, x, y, h
    except FileNotFoundError:
        print("Файл не знайдено. Створюю тестові дані...")
        return generate_test_data()


def generate_test_data():
    N = 10
    x = [0.0] * (N + 2)
    y = [0.0] * (N + 2)
    h = [0.1] * (N + 2)

    for i in range(N + 1):
        x[i] = i * h[0]
        y[i] = f(x[i])

    return N, x, y, h


def calculate_spline_coefficients(x, y, h, N, c):
    a = [0.0] * (N + 1)
    b = [0.0] * (N + 1)
    d = [0.0] * (N + 1)

    for i in range(1, N + 1):
        a[i] = y[i - 1]
        b[i] = (y[i] - y[i - 1]) / h[i] - h[i] * (c[i + 1] + 2 * c[i]) / 3
        d[i] = (c[i + 1] - c[i]) / (3 * h[i])

    return a, b, d


def spline_value(x_val, i, x, a, b, c, d, h):
    dx = x_val - x[i - 1]
    return a[i] + b[i] * dx + c[i] * dx ** 2 + d[i] * dx ** 3


def main():
    filename = "input.txt"
    N, x, y, h = read_input_file(filename)

    print("=" * 50)
    print("ЛАБОРАТОРНА РОБОТА №1")
    print("=" * 50)
    print(f"Кількість інтервалів: {N}")

    c = [0.0] * (N + 2)
    c = progonka(y, h, N, c)

    a, b, d = calculate_spline_coefficients(x, y, h, N, c)

    # Створення точок для графіка
    x_fine = []
    y_fine = []
    y_exact = []

    for i in range(1, N + 1):
        x_start = x[i - 1]
        x_end = x[i]
        for j in range(21):
            x_val = x_start + j * (x_end - x_start) / 20
            x_fine.append(x_val)
            y_fine.append(spline_value(x_val, i, x, a, b, c, d, h))
            y_exact.append(f(x_val))

    # Обчислення похибки
    error = []
    for k in range(len(x_fine)):
        error.append(abs(y_fine[k] - y_exact[k]))

    max_error = max(error)
    mean_error = sum(error) / len(error)

    print(f"\nМаксимальна похибка: {max_error:.2e}")
    print(f"Середня похибка: {mean_error:.2e}")

    # Побудова графіка
    plt.figure(figsize=(10, 6))
    plt.plot(x_fine, y_exact, 'b-', label='sin(x)', linewidth=2)
    plt.plot(x_fine, y_fine, 'r--', label='Сплайн', linewidth=2)
    plt.plot(x[:N + 1], y[:N + 1], 'go', label='Точки', markersize=8)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Кубічна сплайн-інтерполяція')
    plt.legend()
    plt.grid(True)
    plt.savefig('lab-1_plot.png')
    plt.show()

    # Збереження результатів - ТУТ ВИПРАВЛЕНО!
    with open('lab-1_results.txt', 'w') as file:
        file.write(f"Максимальна похибка: {max_error:.2e}\n")
        file.write(f"Середня похибка: {mean_error:.2e}\n")


if __name__ == "__main__":
    main()