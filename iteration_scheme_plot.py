# Необходимо построить графики для схемы при разных степенях.
# Схема: итерации x_{k+1} = phi(x_k), где phi(x) = mu * sqrt(x) * (1 - nu * sqrt(x)).
# Для каждого набора (mu, nu) и начального x0:
#   - проверяем сходимость итераций;
#   - строим график phi(x) вместе с прямой y = x;
#   - строим график x_k от номера итерации k.

import numpy as np
import matplotlib.pyplot as plt


def phi(x, mu, nu):
    r = np.sqrt(x)                       # корень из x
    return mu * r * (1.0 - nu * r)       # значение отображения


def iterate(mu, nu, start=0.1, eps=1e-6, max_iter=100):
    if start < 0:                        # корень из отрицательного не берём
        return None, 0, "start < 0", []

    history = [start]                    # траектория итераций
    current = start                      # текущее значение x_k

    for step in range(1, max_iter + 1):
        nxt = phi(current, mu, nu)       # следующее значение x_{k+1}

        if nxt < 0:                      # ушли в отрицательную область
            history.append(nxt)
            return nxt, step, "вышли из области sqrt", history

        history.append(nxt)              # запоминаем значение

        if abs(nxt - current) < eps:     # соседние значения почти совпали
            return nxt, step, "сошлось", history

        current = nxt                    # переходим к следующему шагу

    return current, max_iter, "не сошлось", history


def draw_phi(mu, nu, x_max=2.0):
    xs = np.linspace(0.0, x_max, 400)               # сетка по x
    plt.figure(figsize=(8, 5))
    plt.plot(xs, phi(xs, mu, nu), label="phi(x)")   # график phi(x)
    plt.plot(xs, xs, "--", label="y = x")           # прямая y = x
    plt.title(f"phi(x),  mu = {mu},  nu = {nu}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.grid(True)
    plt.legend()
    plt.show()


def draw_trajectory(history, mu, nu):
    plt.figure(figsize=(8, 5))
    plt.plot(range(len(history)), history, marker="o")   # x_k от номера k
    plt.title(f"Итерации,  mu = {mu},  nu = {nu}")
    plt.xlabel("k")
    plt.ylabel("x_k")
    plt.grid(True)
    plt.show()


def main():
    params = [                           # наборы (mu, nu, x0)
        (1.0, 1.0, 0.1),
        (1.0, 2.0, 0.1),
        (2.0, 0.5, 0.1),
        (1.0, 3.5, 0.01),
        (1.0, 4.0, 0.1),
    ]

    for mu, nu, x0 in params:
        limit, steps, status, history = iterate(mu, nu, x0)

        print("-----------------------------")
        print(f"mu = {mu},  nu = {nu},  x0 = {x0}")
        print(f"x*       = {limit}")     # найденный предел
        print(f"шагов    = {steps}")     # число итераций
        print(f"статус   = {status}")    # итог работы

        draw_phi(mu, nu)                 # график phi(x)
        draw_trajectory(history, mu, nu) # график траектории


if __name__ == "__main__":
    main()
