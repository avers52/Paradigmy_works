import json
import sys
from field import field
from gen_random import gen_random
from unique import Unique
from print_result import print_result
from cm_timer import cm_timer_1

path = sys.argv[1] if len(sys.argv) > 1 else 'data_light.json'

with open(path, encoding='utf-8') as f:
    data = json.load(f)

@print_result
def f1(arg):
    return sorted(list(Unique(field(arg, 'job-name'), ignore_case=True)), key=lambda x: x.lower())

@print_result
def f2(arg):
    return list(filter(lambda x: x.lower().startswith('программист'), arg))

@print_result
def f3(arg):
    return list(map(lambda x: f"{x} с опытом Python", arg))

@print_result
def f4(arg):
    salaries = list(gen_random(len(arg), 100000, 200000))
    return list(map(lambda x: f"{x[0]}, зарплата {x[1]} руб.", zip(arg, salaries)))


if __name__ == '__main__':
    with cm_timer_1():
        f4(f3(f2(f1(data))))





#f1() - Уникальные профессии:

#field(data, 'job-name') - достаем названия профессий

#Unique(..., ignore_case=True) - убираем дубликаты (игнорируя регистр)

#sorted(..., key=lambda x: x.lower()) - сортируем без учета регистра

#f2() - Фильтр программистов:

#filter(lambda x: x.lower().startswith('программист'), ...) - оставляем только программистов

#f3() - Добавляем Python опыт:

#map(lambda x: f"{x} с опытом Python", ...) - к каждой профессии добавляем текст

#f4() - Добавляем зарплаты:

#gen_random(len(arg), 100000, 200000) - генерируем случайные зарплаты

#zip(arg, salaries) - объединяем профессии и зарплаты

#map(...) - форматируем в красивую строку