def field(items, *args):
    assert len(args) > 0

    if len(args) == 1:
        # Если передан один аргумент - возвращаем только значения
        key = args[0]
        for item in items:
            if key in item and item[key] is not None:
                yield item[key]
    else:
        # Если передано несколько аргументов - возвращаем словари
        for item in items:
            result = {}
            has_values = False
            for key in args:
                if key in item and item[key] is not None:
                    result[key] = item[key]
                    has_values = True
            if has_values:
                yield result


if __name__ == "__main__":
    # Тестовые данные
    goods = [
        {'title': 'Ковер', 'price': 2000, 'color': 'green'},
        {'title': 'Диван для отдыха', 'color': 'black'}
    ]

    print("Test 1 - один аргумент:")
    for value in field(goods, 'title'):
        print(value)

    print("\nTest 2 - несколько аргументов:")
    for value in field(goods, 'title', 'price'):
        print(value)

#Сделать генератор, который из списка словарей достает либо значения полей, либо под-словари.
