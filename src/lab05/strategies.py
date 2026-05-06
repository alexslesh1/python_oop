"""
Модуль стратегий для лабораторной работы №5
Содержит функции-стратегии для сортировки, фильтрации и обработки объектов
"""

from datetime import datetime


# ========== Функции для сортировки (стратегии сортировки) ==========

def by_bus_id(bus):
    """Стратегия сортировки по ID автобуса"""
    return bus.bus_id


def by_capacity(bus):
    """Стратегия сортировки по вместимости"""
    return bus.capacity


def by_speed(bus):
    """Стратегия сортировки по текущей скорости"""
    return bus.speed


def by_route_number(bus):
    """Стратегия сортировки по номеру маршрута (None -> бесконечность)"""
    return bus.route_number if bus.route_number is not None else float('inf')


def by_comfort_level(bus):
    """Стратегия сортировки по уровню комфорта (для туристических)"""
    return getattr(bus, 'comfort_level', 0)


def by_passenger_load(bus):
    """Стратегия сортировки по загруженности (для городских)"""
    if hasattr(bus, 'passengers_count') and bus.capacity > 0:
        return bus.passengers_count / bus.capacity
    return 0


# ========== Функции для фильтрации (стратегии фильтрации) ==========

def is_on_route(bus):
    """Фильтр: автобус на маршруте"""
    from enums import BusStatus
    return bus.status == BusStatus.ON_ROUTE


def is_on_parking(bus):
    """Фильтр: автобус на парковке"""
    from enums import BusStatus
    return bus.status == BusStatus.ON_PARKING


def needs_maintenance_filter(bus):
    """Фильтр: автобус требует ТО"""
    return bus.is_broken


def is_tourist_bus(bus):
    """Фильтр: только туристические автобусы"""
    return type(bus).__name__ == 'ServiceableTouristBus' or hasattr(bus, 'comfort_level')


def is_city_bus(bus):
    """Фильтр: только городские автобусы"""
    return hasattr(bus, 'passengers_count')


def is_school_bus(bus):
    """Фильтр: только школьные автобусы"""
    return hasattr(bus, 'max_speed_limit')


def speed_above_threshold(threshold):
    """
    Фабрика функций: создаёт фильтр для автобусов со скоростью выше порога
    
    Возвращает функцию-замыкание (фабрика функций для оценки 4)
    """
    def filter_fn(bus):
        return bus.speed >= threshold
    return filter_fn


def capacity_below_threshold(threshold):
    """
    Фабрика функций: создаёт фильтр для автобусов с вместимостью ниже порога
    """
    def filter_fn(bus):
        return bus.capacity <= threshold
    return filter_fn


# ========== Функции для преобразования (map) ==========

def to_info_string(bus):
    """Преобразование объекта в строку с краткой информацией"""
    return f"{bus.bus_id}: маршрут {bus.route_number}, {bus.speed} км/ч"


def to_dict(bus):
    """Преобразование объекта в словарь"""
    return {
        'id': bus.bus_id,
        'capacity': bus.capacity,
        'route': bus.route_number,
        'speed': bus.speed,
        'status': bus.status.value
    }


def extract_ids(bus):
    """Извлечение ID автобуса"""
    return bus.bus_id


# ========== Callable-объекты для паттерна Стратегия (оценка 5) ==========

class SortByIdStrategy:
    """Стратегия сортировки по ID"""
    def __call__(self, bus):
        return bus.bus_id


class SortBySpeedStrategy:
    """Стратегия сортировки по скорости"""
    def __call__(self, bus):
        return bus.speed


class SortByRouteStrategy:
    """Стратегия сортировки по маршруту"""
    def __call__(self, bus):
        return bus.route_number if bus.route_number is not None else float('inf')


class OnRouteFilterStrategy:
    """Стратегия фильтрации: автобусы на маршруте"""
    def __call__(self, bus):
        from enums import BusStatus
        return bus.status == BusStatus.ON_ROUTE


class NeedsMaintenanceStrategy:
    """Стратегия фильтрации: автобусы, требующие ТО"""
    def __call__(self, bus):
        return bus.is_broken


class DiscountStrategy:
    """Callable-объект для применения скидки"""
    def __init__(self, discount=0.1):
        self.discount = discount
    
    def __call__(self, bus):
        fare = bus.calculate_fare()
        discounted = fare * (1 - self.discount)
        return f"{bus.bus_id}: {fare} -> {discounted:.2f} руб."


class ActivateStrategy:
    """Стратегия активации/деактивации"""
    def __init__(self, activate=True):
        self.activate = activate
    
    def __call__(self, bus):
        from enums import BusStatus
        if self.activate:
            try:
                bus.start_route()
                return f"{bus.bus_id}: активирован (выехал на маршрут)"
            except:
                return f"{bus.bus_id}: не может выехать (нет маршрута)"
        else:
            bus.park()
            return f"{bus.bus_id}: деактивирован (на парковке)"