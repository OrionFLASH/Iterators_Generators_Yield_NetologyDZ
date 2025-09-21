"""
Домашнее задание по курсу Нетологии: "Iterators. Generators. Yield"

Реализация итераторов и генераторов для работы с вложенными списками.
Включает как простые, так и рекурсивные решения для многоуровневой вложенности.

Изученные концепции:
- Итераторы и протокол итерации
- Генераторы и ключевое слово yield
- Генераторные выражения
- yield from для делегирования
- itertools для работы с итераторами
- Контекстные менеджеры с генераторами
"""

import types
import itertools
from contextlib import contextmanager


class FlatIterator:
    """
    Итератор для плоского представления списка списков.
    Задание 1: Простая реализация для двухуровневой вложенности.
    """
    
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.current_index = 0
        self.current_sub_index = 0
    
    def __iter__(self):
        return self
    
    def __next__(self):
        # Проверяем, есть ли еще элементы в текущем подсписке
        if self.current_index < len(self.list_of_list):
            current_list = self.list_of_list[self.current_index]
            
            if self.current_sub_index < len(current_list):
                item = current_list[self.current_sub_index]
                self.current_sub_index += 1
                return item
            else:
                # Переходим к следующему подсписку
                self.current_index += 1
                self.current_sub_index = 0
                return self.__next__()
        else:
            raise StopIteration


def flat_generator(list_of_lists):
    """
    Генератор для плоского представления списка списков.
    Задание 2: Простая реализация для двухуровневой вложенности.
    """
    for sublist in list_of_lists:
        for item in sublist:
            yield item


class RecursiveFlatIterator:
    """
    Рекурсивный итератор для обработки списков с любым уровнем вложенности.
    Задание 3: Расширенная реализация с поддержкой многоуровневой вложенности.
    """
    
    def __init__(self, list_of_list):
        self.list_of_list = list_of_list
        self.flat_list = self._flatten_recursive(list_of_list)
        self.current_index = 0
    
    def _flatten_recursive(self, nested_list):
        """Рекурсивно разворачивает вложенные списки в плоский список"""
        result = []
        for item in nested_list:
            if isinstance(item, list):
                result.extend(self._flatten_recursive(item))
            else:
                result.append(item)
        return result
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current_index < len(self.flat_list):
            item = self.flat_list[self.current_index]
            self.current_index += 1
            return item
        else:
            raise StopIteration


def recursive_flat_generator(list_of_list):
    """
    Рекурсивный генератор для обработки списков с любым уровнем вложенности.
    Задание 4: Расширенная реализация с поддержкой многоуровневой вложенности.
    """
    for item in list_of_list:
        if isinstance(item, list):
            yield from recursive_flat_generator(item)
        else:
            yield item


# ДОПОЛНИТЕЛЬНЫЕ ПРИМЕРЫ ИЗУЧЕННЫХ КОНЦЕПЦИЙ

def generator_expressions_demo():
    """
    Демонстрация генераторных выражений - компактный способ создания генераторов.
    Изученная концепция: Generator Expressions
    """
    print("\n=== ГЕНЕРАТОРНЫЕ ВЫРАЖЕНИЯ ===")
    
    # Обычный генератор
    def squares_generator(n):
        for i in range(n):
            yield i ** 2
    
    # Генераторное выражение (аналогично)
    squares_gen_expr = (i ** 2 for i in range(5))
    
    print("Обычный генератор:", list(squares_generator(5)))
    print("Генераторное выражение:", list(squares_gen_expr))
    
    # Генераторное выражение с условием
    even_squares = (i ** 2 for i in range(10) if i % 2 == 0)
    print("Четные квадраты:", list(even_squares))


def itertools_demo():
    """
    Демонстрация работы с модулем itertools.
    Изученная концепция: itertools для работы с итераторами
    """
    print("\n=== ITERTOOLS ДЕМОНСТРАЦИЯ ===")
    
    # chain - объединение итераторов
    list1 = [1, 2, 3]
    list2 = [4, 5, 6]
    chained = itertools.chain(list1, list2)
    print("chain:", list(chained))
    
    # cycle - бесконечный цикл
    cycle_iter = itertools.cycle(['A', 'B', 'C'])
    print("cycle (первые 7):", [next(cycle_iter) for _ in range(7)])
    
    # islice - срез итератора
    numbers = range(20)
    sliced = itertools.islice(numbers, 5, 15, 2)
    print("islice:", list(sliced))
    
    # combinations - комбинации
    items = ['a', 'b', 'c']
    combos = itertools.combinations(items, 2)
    print("combinations:", list(combos))


@contextmanager
def generator_context_manager():
    """
    Контекстный менеджер с использованием генератора.
    Изученная концепция: Context Managers с генераторами
    """
    print("Начало работы с контекстом")
    try:
        yield "Контекст активен"
    finally:
        print("Завершение работы с контекстом")


def advanced_yield_demo():
    """
    Демонстрация продвинутых возможностей yield.
    Изученная концепция: Продвинутые возможности yield
    """
    print("\n=== ПРОДВИНУТЫЕ ВОЗМОЖНОСТИ YIELD ===")
    
    def data_processor(data):
        """Генератор с отправкой данных обратно"""
        result = []
        for item in data:
            # Получаем данные от вызывающего кода
            feedback = yield item
            if feedback:
                result.append(feedback)
        return result
    
    # Использование send()
    processor = data_processor([1, 2, 3, 4, 5])
    print("Первое значение:", next(processor))
    print("Отправка 'processed' и получение следующего:", processor.send("processed"))
    print("Следующее значение:", next(processor))
    
    # Генератор с throw()
    def error_generator():
        try:
            yield 1
            yield 2
        except ValueError as e:
            print(f"Поймано исключение: {e}")
            yield "Обработано"
    
    gen = error_generator()
    print("Первое значение:", next(gen))
    print("Бросаем исключение:", gen.throw(ValueError, "Тестовая ошибка"))


def memory_efficiency_demo():
    """
    Демонстрация эффективности использования памяти генераторами.
    Изученная концепция: Эффективность памяти генераторов
    """
    print("\n=== ЭФФЕКТИВНОСТЬ ПАМЯТИ ===")
    
    import sys
    
    # Список - занимает всю память сразу
    big_list = [i for i in range(1000)]
    list_size = sys.getsizeof(big_list)
    
    # Генератор - занимает минимум памяти
    big_generator = (i for i in range(1000))
    gen_size = sys.getsizeof(big_generator)
    
    print(f"Размер списка: {list_size} байт")
    print(f"Размер генератора: {gen_size} байт")
    print(f"Экономия памяти: {list_size - gen_size} байт")


def test_1():
    """Тест для задания 1: простой FlatIterator"""
    print("Тестирование FlatIterator (задание 1)...")
    
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            FlatIterator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(FlatIterator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    print("✓ Задание 1 выполнено успешно!")


def test_2():
    """Тест для задания 2: простой flat_generator"""
    print("Тестирование flat_generator (задание 2)...")
    
    list_of_lists_1 = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]

    for flat_iterator_item, check_item in zip(
            flat_generator(list_of_lists_1),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    ):
        assert flat_iterator_item == check_item

    assert list(flat_generator(list_of_lists_1)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None]
    assert isinstance(flat_generator(list_of_lists_1), types.GeneratorType)
    print("✓ Задание 2 выполнено успешно!")


def test_3():
    """Тест для задания 3: рекурсивный FlatIterator"""
    print("Тестирование RecursiveFlatIterator (задание 3)...")
    
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            RecursiveFlatIterator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(RecursiveFlatIterator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    print("✓ Задание 3 выполнено успешно!")


def test_4():
    """Тест для задания 4: рекурсивный flat_generator"""
    print("Тестирование recursive_flat_generator (задание 4)...")
    
    list_of_lists_2 = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]

    for flat_iterator_item, check_item in zip(
            recursive_flat_generator(list_of_lists_2),
            ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    ):
        assert flat_iterator_item == check_item

    assert list(recursive_flat_generator(list_of_lists_2)) == ['a', 'b', 'c', 'd', 'e', 'f', 'h', False, 1, 2, None, '!']
    assert isinstance(recursive_flat_generator(list_of_lists_2), types.GeneratorType)
    print("✓ Задание 4 выполнено успешно!")


def demonstrate_usage():
    """Демонстрация использования всех реализованных классов и функций"""
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ИТЕРАТОРОВ И ГЕНЕРАТОРОВ")
    print("="*60)
    
    # Тестовые данные
    simple_list = [
        ['a', 'b', 'c'],
        ['d', 'e', 'f', 'h', False],
        [1, 2, None]
    ]
    
    complex_list = [
        [['a'], ['b', 'c']],
        ['d', 'e', [['f'], 'h'], False],
        [1, 2, None, [[[[['!']]]]], []]
    ]
    
    print("\n1. Простой FlatIterator:")
    print(f"Исходный список: {simple_list}")
    print(f"Результат: {list(FlatIterator(simple_list))}")
    
    print("\n2. Простой flat_generator:")
    print(f"Исходный список: {simple_list}")
    print(f"Результат: {list(flat_generator(simple_list))}")
    
    print("\n3. Рекурсивный FlatIterator:")
    print(f"Исходный список: {complex_list}")
    print(f"Результат: {list(RecursiveFlatIterator(complex_list))}")
    
    print("\n4. Рекурсивный flat_generator:")
    print(f"Исходный список: {complex_list}")
    print(f"Результат: {list(recursive_flat_generator(complex_list))}")
    
    print("\n5. Демонстрация ленивой загрузки генератора:")
    print("Элементы генератора по одному:")
    for i, item in enumerate(flat_generator(simple_list)):
        print(f"  {i+1}: {item}")
        if i >= 4:  # Показываем только первые 5 элементов
            print("  ...")
            break
    
    # Дополнительные демонстрации изученных концепций
    generator_expressions_demo()
    itertools_demo()
    advanced_yield_demo()
    memory_efficiency_demo()
    
    # Демонстрация контекстного менеджера
    print("\n=== КОНТЕКСТНЫЙ МЕНЕДЖЕР ===")
    with generator_context_manager() as context:
        print(f"Состояние: {context}")
        print("Работаем внутри контекста...")


if __name__ == '__main__':
    print("ЗАПУСК ДОМАШНЕГО ЗАДАНИЯ ПО ИТЕРАТОРАМ И ГЕНЕРАТОРАМ")
    print("="*60)
    
    try:
        # Запуск всех тестов
        test_1()
        test_2()
        test_3()
        test_4()
        
        print("\n" + "="*60)
        print("ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО! ✓")
        print("="*60)
        
        # Демонстрация работы
        demonstrate_usage()
        
    except Exception as e:
        print(f"Ошибка при выполнении тестов: {e}")
        raise
