class Unique(object):
    def __init__(self, items, **kwargs):
        self.ignore_case = kwargs.get('ignore_case', False)
        self.items = iter(items)
        self.seen = set()

    def __next__(self):
        while True:
            item = next(self.items)

            # Для сравнения учитываем регистр, если нужно
            if isinstance(item, str) and self.ignore_case:
                check_item = item.lower()
            else:
                check_item = item

            if check_item not in self.seen:
                self.seen.add(check_item)
                return item

    def __iter__(self):
        return self


if __name__ == "__main__":
    print("Test 1 - числа:")
    data1 = [1, 1, 1, 1, 1, 2, 2, 2, 2, 2]
    for item in Unique(data1):
        print(item, end=" ")
    print()

    print("\nTest 2 - строки без ignore_case:")
    data2 = ['a', 'A', 'b', 'B', 'a', 'A', 'b', 'B']
    for item in Unique(data2):
        print(item, end=" ")
    print()

    print("\nTest 3 - строки с ignore_case=True:")
    for item in Unique(data2, ignore_case=True):
        print(item, end=" ")
    print()

#Создать итератор, который пропускает повторяющиеся элементы