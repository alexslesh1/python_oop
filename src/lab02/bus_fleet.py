# Добавить в начало файла bus_fleet.py
import sys
import os

# Добавляем путь к lab01 и lab03
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))

from models import Bus


class BusFleet:
    def __init__(self):
        """Инициализация пустой коллекции"""
        self._items = []
    
    def add(self, bus):
        if not isinstance(bus, Bus):
            raise TypeError("Можно добавлять только объекты Bus")
        
        if self._find_by_id(bus.bus_id) is not None:
            raise ValueError(f"Автобус с ID {bus.bus_id} уже существует")
        
        self._items.append(bus)
        return f"Автобус {bus.bus_id} добавлен"
    
    def remove(self, bus):
        """Удалить автобус из коллекции"""
        if bus not in self._items:
            raise ValueError("Автобус не найден в коллекции")
        self._items.remove(bus)
        return f"Автобус {bus.bus_id} удален"
    
    def remove_at(self, index):
        """Удалить автобус по индексу (оценка 5)"""
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        if index < 0 or index >= len(self._items):
            raise IndexError("Индекс вне диапазона")
        removed = self._items.pop(index)
        return f"Автобус {removed.bus_id} удален (индекс {index})"
    
    def get_all(self):
        """Вернуть список всех автобусов"""
        return self._items.copy()
    
    def clear(self):
        """Очистить коллекцию"""
        self._items.clear()
        return "Коллекция очищена"
    
    def _find_by_id(self, bus_id):
        """Внутренний метод поиска по ID"""
        for bus in self._items:
            if bus.bus_id == bus_id:
                return bus
        return None
    
    def find_by_id(self, bus_id):
        """Найти автобус по ID"""
        result = self._find_by_id(bus_id)
        if result is None:
            raise ValueError(f"Автобус с ID {bus_id} не найден")
        return result
    
    def find_by_route(self, route_number):
        """Найти все автобусы по номеру маршрута"""
        results = [bus for bus in self._items if bus.route_number == route_number]
        if not results:
            raise ValueError(f"Автобусы с маршрутом {route_number} не найдены")
        return results
    
    def find_by_driver(self, driver_name):
        """Найти все автобусы по имени водителя"""
        results = [bus for bus in self._items if bus.driver_name == driver_name]
        if not results:
            raise ValueError(f"Автобусы с водителем {driver_name} не найдены")
        return results
    
    def find_by_status(self, status):
        """Найти все автобусы по состоянию"""
        results = [bus for bus in self._items if bus.status == status]
        if not results:
            raise ValueError(f"Автобусы со статусом {status.value} не найдены")
        return results
    
    def get_on_route(self):
        """Вернуть коллекцию автобусов на маршруте"""
        new_fleet = BusFleet()
        for bus in self._items:
            if bus.status.value == "На маршруте":
                new_fleet._items.append(bus)
        return new_fleet
    
    def get_needs_maintenance(self):
        """Вернуть коллекцию автобусов, требующих ТО"""
        new_fleet = BusFleet()
        for bus in self._items:
            if bus.is_broken:
                new_fleet._items.append(bus)
        return new_fleet
    
    def get_by_min_speed(self, min_speed):
        """Вернуть коллекцию автобусов со скоростью >= min_speed"""
        new_fleet = BusFleet()
        for bus in self._items:
            if bus.speed >= min_speed:
                new_fleet._items.append(bus)
        return new_fleet
    
    def sort_by_id(self):
        """Сортировка по ID"""
        self._items.sort(key=lambda bus: bus.bus_id)
        return "Отсортировано по ID"
    
    def sort_by_route(self):
        """Сортировка по номеру маршрута (None в конец)"""
        self._items.sort(key=lambda bus: bus.route_number if bus.route_number is not None else 9999)
        return "Отсортировано по маршруту"
    
    def sort_by_speed(self):
        """Сортировка по скорости"""
        self._items.sort(key=lambda bus: bus.speed)
        return "Отсортировано по скорости"
    
    def sort(self, key_func):
        """Универсальная сортировка с пользовательским ключом"""
        self._items.sort(key=key_func)
        return "Отсортировано"
    
    def __len__(self):
        """Возвращает количество автобусов в коллекции (оценка 4)"""
        return len(self._items)
    
    def __getitem__(self, index):
        """Доступ по индексу (оценка 5) - поддерживает отрицательные индексы"""
        if isinstance(index, slice):
            new_fleet = BusFleet()
            new_fleet._items = self._items[index]
            return new_fleet
        
        if not isinstance(index, int):
            raise TypeError("Индекс должен быть целым числом")
        
        length = len(self._items)
        if index < 0:
            index = length + index
        
        if index < 0 or index >= length:
            raise IndexError("Индекс вне диапазона")
        
        return self._items[index]
    
    def __iter__(self):
        """Итератор для for item in collection (оценка 4)"""
        return iter(self._items)
    
    def __str__(self):
        """Строковое представление коллекции"""
        if not self._items:
            return "Коллекция пуста"
        result = f"BusFleet ({len(self._items)} автобусов):\n"
        for i, bus in enumerate(self._items):
            result += f"  [{i}] {bus.bus_id} | маршрут {bus.route_number} | {bus.speed} км/ч | {bus.status.value}\n"
        return result
    
    def __repr__(self): #для вывода 
        return f"BusFleet({len(self._items)} items)"
    
    def __contains__(self, bus):
        """Проверка наличия автобуса в коллекции"""
        return bus in self._items