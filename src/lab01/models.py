"""
Дочерние классы автобусов
TouristBus, CityBus, SchoolBus
"""

import sys
import os

# Добавляем путь к lab01 для импорта enums
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))

from base import Bus
from enums import BusStatus


class TouristBus(Bus):
    """Туристический автобус - для дальних поездок и экскурсий"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_wifi=True, has_toilet=False, comfort_level=3):
        super().__init__(bus_id, capacity, route_number, driver_name, current_speed, status)
        
        self._has_wifi = has_wifi
        self._has_toilet = has_toilet
        self._comfort_level = comfort_level
    
    @property
    def has_wifi(self):
        return self._has_wifi
    
    @property
    def has_toilet(self):
        return self._has_toilet
    
    @property
    def comfort_level(self):
        return self._comfort_level
    
    def serve_snacks(self):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Подача закусков возможна только на маршруте")
        return "🍪 Пассажирам поданы закуски и напитки"
    
    def calculate_fare(self):
        base_fare = super().calculate_fare()
        comfort_bonus = self._comfort_level * 50
        wifi_bonus = 30 if self._has_wifi else 0
        toilet_bonus = 40 if self._has_toilet else 0
        return base_fare + comfort_bonus + wifi_bonus + toilet_bonus
    
    def get_bus_type(self):
        return "Туристический автобус"
    
    def __str__(self):
        base_str = super().__str__()
        wifi = "есть" if self._has_wifi else "нет"
        toilet = "есть" if self._has_toilet else "нет"
        return (f"{base_str}\n"
                f"   Wi-Fi: {wifi}\n"
                f"   Туалет: {toilet}\n"
                f"   Комфорт: {self._comfort_level}★")


class CityBus(Bus):
    """Городской автобус - для перевозки пассажиров внутри города"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_validator=True, has_usb_ports=False):
        super().__init__(bus_id, capacity, route_number, driver_name, current_speed, status)
        
        self._has_validator = has_validator
        self._has_usb_ports = has_usb_ports
        self._passengers_count = 0
    
    @property
    def has_validator(self):
        return self._has_validator
    
    @property
    def has_usb_ports(self):
        return self._has_usb_ports
    
    @property
    def passengers_count(self):
        return self._passengers_count
    
    def board_passenger(self):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Посадка возможна только на маршруте")
        if self._passengers_count >= self._capacity:
            raise ValueError("Автобус переполнен")
        self._passengers_count += 1
        return f"Пассажир сел. Всего: {self._passengers_count}/{self._capacity}"
    
    def alight_passenger(self):
        if self._passengers_count <= 0:
            raise ValueError("В автобусе нет пассажиров")
        self._passengers_count -= 1
        return f"Пассажир вышел. Осталось: {self._passengers_count}"
    
    def calculate_fare(self):
        return super().calculate_fare() - 20
    
    def get_bus_type(self):
        return "Городской автобус"
    
    def __str__(self):
        base_str = super().__str__()
        validator = "есть" if self._has_validator else "нет"
        usb = "есть" if self._has_usb_ports else "нет"
        return (f"{base_str}\n"
                f"   Валидатор: {validator}\n"
                f"   USB-порты: {usb}\n"
                f"   Пассажиров: {self._passengers_count}")


class SchoolBus(Bus):
    """Школьный автобус - для перевозки детей"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_escort=True, max_speed_limit=70):
        super().__init__(bus_id, capacity, route_number, driver_name, current_speed, status)
        
        self._has_escort = has_escort
        self._max_speed_limit = max_speed_limit
        self._children_count = 0
    
    @property
    def has_escort(self):
        return self._has_escort
    
    @property
    def max_speed_limit(self):
        return self._max_speed_limit
    
    def board_child(self):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Посадка возможна только на маршруте")
        if self._children_count >= self._capacity:
            raise ValueError("Автобус переполнен")
        self._children_count += 1
        return f"Ребенок сел. Всего детей: {self._children_count}"
    
    def play_educational_video(self):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Видео можно включить только в пути")
        return "📺 Включено обучающее видео"
    
    def calculate_fare(self):
        return 0.0
    
    def get_bus_type(self):
        return "Школьный автобус"
    
    def accelerate(self, increment):
        new_speed = self._speed + increment
        if new_speed > self._max_speed_limit:
            raise ValueError(f"Школьный автобус не может ехать быстрее {self._max_speed_limit} км/ч")
        return super().accelerate(increment)
    
    def __str__(self):
        base_str = super().__str__()
        escort = "есть" if self._has_escort else "нет"
        return (f"{base_str}\n"
                f"   Сопровождающий: {escort}\n"
                f"   Лимит скорости: {self._max_speed_limit} км/ч\n"
                f"   Детей в салоне: {self._children_count}")