import sys
import math


def get_coef(index, prompt):
    '''
    Читаем коэффициент из командной строки или вводим с клавиатуры

    Args:
        index (int): Номер параметра в командной строке
        prompt (str): Приглашение для ввода коэффициента

    Returns:
        float: Коэффициент биквадратного уравнения
    '''
    while True:
        try:
            # Пробуем прочитать коэффициент из командной строки
            if len(sys.argv) > index:
                coef_str = sys.argv[index]
                coef = float(coef_str)
                return coef
            else:
                # Вводим с клавиатуры
                print(prompt)
                coef_str = input()
                coef = float(coef_str)
                return coef
        except ValueError:
            # Если преобразование не удалось, вводим заново
            print("Ошибка! Введите действительное число.")
            # Если это был параметр командной строки, игнорируем его
            # и переходим к вводу с клавиатуры
            if len(sys.argv) > index:
                print(f"Некорректный параметр командной строки: {sys.argv[index]}")
            # Продолжаем цикл для ввода с клавиатуры


def solve_quadratic(a, b, c):
    '''
    Вычисление корней квадратного уравнения

    Args:
        a (float): коэффициент А
        b (float): коэффициент B
        c (float): коэффициент C

    Returns:
        list[float]: Список корней
    '''
    result = []
    if a == 0:
        # Линейное уравнение
        if b != 0:
            root = -c / b
            result.append(root)
        return result

    D = b * b - 4 * a * c
    if D == 0.0:
        root = -b / (2.0 * a)
        result.append(root)
    elif D > 0.0:
        sqD = math.sqrt(D)
        root1 = (-b + sqD) / (2.0 * a)
        root2 = (-b - sqD) / (2.0 * a)
        result.append(root1)
        result.append(root2)
    return result


def get_biquadratic_roots(a, b, c):
    '''
    Вычисление корней биквадратного уравнения

    Args:
        a (float): коэффициент А
        b (float): коэффициент B
        c (float): коэффициент C

    Returns:
        list[float]: Список действительных корней
    '''
    # Решаем квадратное уравнение относительно t = x²
    t_roots = solve_quadratic(a, b, c)

    result = []

    # Для каждого корня t находим x = ±√t (если t >= 0)
    for t_root in t_roots:
        if t_root > 0:
            x1 = math.sqrt(t_root)
            x2 = -math.sqrt(t_root)
            result.append(x1)
            result.append(x2)
        elif t_root == 0:
            result.append(0.0)

    # Убираем дубликаты и сортируем
    result = sorted(list(set(result)))
    return result


def main():
    '''
    Основная функция
    '''
    print("Решение биквадратного уравнения Ax⁴ + Bx² + C = 0")

    a = get_coef(1, 'Введите коэффициент А:')
    while a == 0:
        print("Коэффициент А не может быть равен нулю для биквадратного уравнения!")
        a = get_coef(1, 'Введите коэффициент А (не равный нулю):')

    b = get_coef(2, 'Введите коэффициент B:')
    c = get_coef(3, 'Введите коэффициент C:')

    # Вычисление корней
    roots = get_biquadratic_roots(a, b, c)

    # Вывод корней
    len_roots = len(roots)
    if len_roots == 0:
        print('Действительных корней нет')
    elif len_roots == 1:
        print('Один корень: {}'.format(roots[0]))
    elif len_roots == 2:
        print('Два корня: {} и {}'.format(roots[0], roots[1]))
    elif len_roots == 3:
        print('Три корня: {}, {} и {}'.format(roots[0], roots[1], roots[2]))
    elif len_roots == 4:
        print('Четыре корня: {}, {}, {} и {}'.format(roots[0], roots[1], roots[2], roots[3]))
    else:
        print('Корни: {}'.format(roots))


# Если сценарий запущен из командной строки
if __name__ == "__main__":
    main()

# Пример запуска
# qr.py 1 0 -4