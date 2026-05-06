"""
Расширенная коллекция BusFleet с поддержкой функций высшего порядка
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab02'))

from bus_fleet import BusFleet


class ExtendedBusFleet(BusFleet):
    """
    Расширенная коллекция автобусов с поддержкой:
    - sort_by() - сортировка по переданной функции
    - filter_by() - фильтрация по предикату
    - apply() - применение функции ко всем элементам
    - map() - преобразование элементов
    """
    
    def sort_by(self, key_func, reverse=False):
        """
        Сортировка коллекции по переданной функции-ключу
        
        Args:
            key_func: функция, возвращающая значение для сортировки
            reverse: если True, сортировка в обратном порядке
        """
        self._items.sort(key=key_func, reverse=reverse)
        return self
    
    def filter_by(self, predicate):
        """
        Фильтрация коллекции по предикату
        Возвращает новую коллекцию с отфильтрованными элементами
        
        Args:
            predicate: функция, возвращающая True/False
        """
        filtered = ExtendedBusFleet()
        filtered._items = [item for item in self._items if predicate(item)]
        return filtered
    
    def apply(self, func):
        """
        Применить функцию ко всем элементам коллекции
        
        Args:
            func: функция, принимающая элемент и возвращающая результат
        """
        results = []
        for item in self._items:
            result = func(item)
            results.append(result)
        return results
    
    def map(self, func):
        """
        Преобразовать коллекцию, применяя функцию к каждому элементу
        Возвращает список результатов
        
        Args:
            func: функция преобразования
        """
        return list(map(func, self._items))