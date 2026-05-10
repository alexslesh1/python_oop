"""
Модуль с Generic-коллекцией и Protocols для лабораторной работы №6
"""

from typing import TypeVar, Generic, Callable, Optional, List, Protocol
import sys
import os

# Добавляем пути для импорта из предыдущих лабораторных
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab04'))

from enums import BusStatus
from bus_models import (
    ServiceableBus, 
    ServiceableTouristBus, 
    ServiceableCityBus, 
    ServiceableSchoolBus
)

# ========== TypeVar для Generic-коллекции ==========
T = TypeVar('T')  # Основной тип для коллекции
R = TypeVar('R')  # Тип для результата map (может отличаться от T)


class TypedCollection(Generic[T]):
    """
    Generic-версия коллекции из ЛР-2
    Хранит объекты только одного типа T
    """
    
    def __init__(self) -> None:
        """Конструктор с аннотацией типов"""
        self._items: List[T] = []
    
    def add(self, item: T) -> None:
        """Добавить элемент в коллекцию"""
        self._items.append(item)
    
    def remove(self, item: T) -> None:
        """Удалить элемент из коллекции"""
        if item not in self._items:
            raise ValueError("Элемент не найден в коллекции")
        self._items.remove(item)
    
    def remove_at(self, index: int) -> T:
        """Удалить элемент по индексу"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items.pop(index)
    
    def get_all(self) -> List[T]:
        """Вернуть список всех элементов"""
        return self._items.copy()
    
    def clear(self) -> None:
        """Очистить коллекцию"""
        self._items.clear()
    
    def __len__(self) -> int:
        """Возвращает количество элементов"""
        return len(self._items)
    
    def __getitem__(self, index: int) -> T:
        """Доступ по индексу"""
        if isinstance(index, slice):
            new_collection = TypedCollection[T]()
            new_collection._items = self._items[index]
            return new_collection
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < -len(self._items) or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        return self._items[index]
    
    def __iter__(self):
        """Итератор для цикла for"""
        return iter(self._items)
    
    def __contains__(self, item: T) -> bool:
        """Проверка наличия элемента"""
        return item in self._items
    
    # ========== Методы для оценки 4 ==========
    
    def find(self, predicate: Callable[[T], bool]) -> Optional[T]:
        """
        Найти первый элемент, удовлетворяющий условию
        Возвращает элемент или None
        """
        for item in self._items:
            if predicate(item):
                return item
        return None
    
    def filter(self, predicate: Callable[[T], bool]) -> List[T]:
        """
        Фильтрация элементов по условию
        Возвращает список всех подходящих элементов
        """
        return [item for item in self._items if predicate(item)]
    
    def map(self, transform: Callable[[T], R]) -> List[R]:
        """
        Преобразование элементов с помощью функции
        Тип результата может отличаться от типа исходной коллекции
        """
        return [transform(item) for item in self._items]
    
    def sort_by(self, key_func: Callable[[T], any], reverse: bool = False) -> None:
        """Сортировка коллекции по переданной функции-ключу"""
        self._items.sort(key=key_func, reverse=reverse)
    
    def apply(self, func: Callable[[T], any]) -> List[any]:
        """Применить функцию ко всем элементам"""
        return [func(item) for item in self._items]
    
    def __str__(self) -> str:
        if not self._items:
            return "TypedCollection (пуста)"
        result = f"TypedCollection (тип: {type(self._items[0]).__name__}, {len(self._items)} элементов):\n"
        for i, item in enumerate(self._items):
            result += f"  [{i}] {item}\n"
        return result
    
    def __repr__(self) -> str:
        return f"TypedCollection({len(self._items)} items)"


# ========== Protocols для оценки 5 ==========

class Displayable(Protocol):
    """
    Protocol для объектов, которые можно отобразить
    Любой объект, у которого есть метод display() -> str
    """
    def display(self) -> str:
        ...


class Scorable(Protocol):
    """
    Protocol для объектов, которые имеют оценку/балл
    Любой объект, у которого есть метод score() -> float
    """
    def score(self) -> float:
        ...


# ========== TypeVar с ограничением для Protocols ==========

D = TypeVar('D', bound=Displayable)  # Только объекты с методом display
S = TypeVar('S', bound=Scorable)     # Только объекты с методом score


# ========== Классы-адаптеры для демонстрации Protocols ==========

class DisplayableBusAdapter:
    """
    Адаптер для автобуса, реализующий Protocol Displayable
    (демонстрация структурной типизации - класс не наследуется от Protocol)
    """
    def __init__(self, bus) -> None:
        self._bus = bus
    
    def display(self) -> str:
        """Реализация метода display для Protocol"""
        route = self._bus.route_number if self._bus.route_number else "не назначен"
        return f"{self._bus.bus_id}: маршрут {route}, {self._bus.speed} км/ч, {self._bus.status.value}"
    
    def get_bus(self):
        return self._bus


class ScorableBusAdapter:
    """
    Адаптер для автобуса, реализующий Protocol Scorable
    """
    def __init__(self, bus) -> None:
        self._bus = bus
    
    def score(self) -> float:
        """Реализация метода score для Protocol (на основе стоимости проезда)"""
        return self._bus.calculate_fare()
    
    def get_bus(self):
        return self._bus