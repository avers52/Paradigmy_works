import time
from contextlib import contextmanager


class cm_timer_1:
    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        print(f"time: {self.end_time - self.start_time:.1f}")


@contextmanager
def cm_timer_2():
    start_time = time.time()
    yield
    end_time = time.time()
    print(f"time: {end_time - start_time:.1f}")


if __name__ == "__main__":
    print("Test cm_timer_1:")
    with cm_timer_1():
        time.sleep(0.5)

    print("\nTest cm_timer_2:")
    with cm_timer_2():
        time.sleep(0.5)

#Создать два контекстных менеджера для измерения времени выполнения кода

#cm_timer_1 (класс): Использовал магические методы __enter__ и __exit__

#cm_timer_2 (функция): Использовал декоратор @contextmanager из contextlib