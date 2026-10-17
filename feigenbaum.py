# Код вычисляет константу Фейгенбаума 
# через каскад удвоения периода в логистическом отображении x -> r*x*(1-x).
# Точки бифуркации ищутся методом деления отрезка пополам.

import math


def logistic_step(r, x, iterations):
    for _ in range(iterations):          # прогоняем отображение нужное число раз
        x = r * x * (1.0 - x)            # один шаг логистического отображения
    return x


def find_bifurcation(r_low, r_high, period, eps=1e-15, max_steps=100):
    low, high = r_low, r_high            # границы отрезка поиска
    for _ in range(max_steps):           # ограничиваем число шагов бисекции
        center = 0.5 * (low + high)      # середина отрезка
        value = logistic_step(center, 0.5, period)   # состояние после 2^n итераций

        if value > 0.5:                  # цикл ещё устойчив
            low = center                 # сдвигаем левую границу
        else:                            # цикл потерял устойчивость
            high = center                # сдвигаем правую границу

        if high - low < eps:             # достигли нужной точности
            break

    return 0.5 * (low + high)            # возвращаем найденную точку


def feigenbaum_constant(order=8):
    points = [2.0, 1.0 + math.sqrt(5.0)]   # первые две точки бифуркации

    delta = 0.0                          # текущее приближение константы
    for n in range(2, order + 1):        # ищем точки для 2^n-циклов
        margin = 0.5 * (points[-1] - points[-2])   # запас для правой границы
        new_point = find_bifurcation(
            r_low=points[-1],            # нижняя граница — прошлая точка
            r_high=points[-1] + margin,  # верхняя граница — с запасом
            period=2 ** n,               # период текущего цикла
        )
        points.append(new_point)         # добавляем новую точку в список

        delta = (points[-2] - points[-3]) / (points[-1] - points[-2])   # формула константы

        print(f"порядок {n}: r = {new_point:.8f},  delta = {delta:.8f}")

    return delta                         # итоговое приближение


if __name__ == "__main__":
    result = feigenbaum_constant(order=8)   # запуск расчёта
    print()
    print(f"Вычисленная константа Фейгенбаума: {result:.8f}")
    print(f"Табличное значение:                 4.66920161")
