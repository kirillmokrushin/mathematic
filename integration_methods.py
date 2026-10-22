import numpy as np  
import sympy as sp  
from scipy.integrate import quad  

delta, coef_1, coef_2, coef_3 = sp.symbols('delta coef_1 coef_2 coef_3')  # Объявляем переменные системы
equations = [  # Создаём список уравнений
    sp.Eq(coef_1 + coef_2 + coef_3, delta),  # Первое уравнение
    sp.Eq(coef_2 * (delta/2) + coef_3 * delta, delta**2 / 2),  # Второе уравнение
    sp.Eq(coef_2 * (delta/2)**2 + coef_3 * delta**2, delta**3 / 3)  # Третье уравнение
]
solution = sp.solve(equations, (coef_1, coef_2, coef_3))  # Решаем систему уравнений
for name in (coef_1, coef_2, coef_3):  # Проходимся по найденным коэффициентам
    print(f"{name} = {sp.factor(solution[name])}")  # Печатаем коэффициенты в факторизованном виде

def integrand(x):  # Объявляем подынтегральную функцию
    return np.sin(x) / x  # Возвращаем значение sin(x)/x

left_bound, right_bound = 1.0, 2.0  # Задаём границы интегрирования
exact_value, _ = quad(integrand, left_bound, right_bound)  # Вычисляем эталонное значение
print(f"Эталон: {exact_value:.8f}")  # Печатаем эталонное значение

def method_1_node(n):  # Метод прямоугольников с 1 узлом
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = 0.0  # Инициализируем сумму
    for i in range(n):  # Проходимся по всем отрезкам
        total_sum += integrand(left_bound + (i + 0.5) * step)  # Добавляем среднее значение
    return total_sum * step  # Возвращаем результат

def method_2_nodes(n):  # Метод прямоугольников с 2 узлами
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = 0.0  # Инициализируем сумму
    for i in range(n):  # Проходимся по всем отрезкам
        total_sum += (integrand(left_bound + i * step) + integrand(left_bound + (i + 1) * step)) / 2  # Формула трапеции
    return total_sum * step  # Возвращаем результат

def method_3_nodes(n):  # Метод прямоугольников с 3 узлами
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = 0.0  # Инициализируем сумму
    for i in range(n):  # Проходимся по всем отрезкам
        x_left = left_bound + i * step  # Левая точка
        x_mid = x_left + step / 2  # Средняя точка
        x_right = x_left + step  # Правая точка
        total_sum += (integrand(x_left) + 4 * integrand(x_mid) + integrand(x_right)) / 6  # Формула Симпсона
    return total_sum * step  # Возвращаем результат

def method_trapezoid(n):  # Классический метод трапеций
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = (integrand(left_bound) + integrand(right_bound)) / 2  # Учитываем края
    for i in range(1, n):  # Проходимся по внутренним точкам
        total_sum += integrand(left_bound + i * step)  # Добавляем значения
    return total_sum * step  # Возвращаем результат

def method_simpson(n):  # Метод Симпсона
    if n % 2 != 0:  # Если n нечётное
        n += 1  # Делаем его чётным
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = integrand(left_bound) + integrand(right_bound)  # Учитываем края
    for i in range(1, n):  # Проходимся по внутренним точкам
        if i % 2 == 0:  # Если чётная точка
            total_sum += 2 * integrand(left_bound + i * step)  # Умножаем на 2
        else:  # Если нечётная точка
            total_sum += 4 * integrand(left_bound + i * step)  # Умножаем на 4
    return total_sum * step / 3  # Возвращаем результат

def method_38(n):  # Метод 3/8
    if n % 3 != 0:  # Если n не кратно 3
        n += 3 - (n % 3)  # Дополняем до кратного 3
    step = (right_bound - left_bound) / n  # Вычисляем шаг
    total_sum = integrand(left_bound) + integrand(right_bound)  # Учитываем края
    for i in range(1, n):  # Проходимся по внутренним точкам
        if i % 3 == 0:  # Если номер кратен 3
            total_sum += 2 * integrand(left_bound + i * step)  # Умножаем на 2
        else:  # В остальных случаях
            total_sum += 3 * integrand(left_bound + i * step)  # Умножаем на 3
    return total_sum * 3 * step / 8  # Возвращаем результат

methods = {  # Создаём словарь всех методов
    "Прямоугольники (1)": method_1_node,  # Добавляем метод 1
    "Прямоугольники (2)": method_2_nodes,  # Добавляем метод 2
    "Прямоугольники (3)": method_3_nodes,  # Добавляем метод 3
    "Трапеции": method_trapezoid,  # Добавляем метод трапеций
    "Симпсон": method_simpson,  # Добавляем метод Симпсона
    "3/8": method_38  # Добавляем метод 3/8
}

print("Метод                  | n")  # Печатаем заголовок таблицы
print("-" * 28)  # Печатаем разделитель
for name, calculate in methods.items():  # Проходимся по всем методам
    n = 1  # Начинаем с 1 отрезка
    while n <= 5000:  # Пока n не превышает 5000
        result = calculate(n)  # Вычисляем интеграл
        error = abs(exact_value - result)  # Считаем погрешность
        if error < 0.5e-6:  # Если достигнута точность в 6 знаков
            print(f"{name:<22} | {n}")  # Печатаем метод и нужное n
            break  # Выходим из цикла
        n += 1  # Увеличиваем n
