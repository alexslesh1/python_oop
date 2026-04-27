"""
Классы транспортной системы с реализацией интерфейсов
"""

import sys
import os
from datetime import datetime

# Добавляем пути для импорта из предыдущих лабораторных
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))

from base import Bus
from models import TouristBus, CityBus, SchoolBus
from enums import BusStatus
from interfaces import IPrintable, IServiceable, IComparable


class ServiceableBus(Bus, IPrintable, IServiceable, IComparable):
    """Обычный автобус с реализацией всех интерфейсов"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING):
        super().__init__(bus_id, capacity, route_number, driver_name, current_speed, status)
    
    def get_info(self) -> str:
        route = f"№{self._route_number}" if self._route_number else "не назначен"
        return f"Bus {self._id}: маршрут {route}, {self._speed} км/ч, {self._status.value}"
    
    def needs_service(self) -> bool:
        return self.is_broken
    
    def service(self) -> str:
        old_days = (datetime.now() - self._last_maintenance).days
        self.send_to_maintenance()
        return f"Bus {self._id}: проведено ТО (последнее было {old_days} дн. назад)"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Bus):
            raise TypeError("Можно сравнивать только с объектами Bus")
        if self._capacity < other._capacity:
            return -1
        elif self._capacity == other._capacity:
            return 0
        return 1


class ServiceableTouristBus(TouristBus, IPrintable, IServiceable, IComparable):
    """Туристический автобус с реализацией всех интерфейсов"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_wifi=True, has_toilet=False, comfort_level=3):
        super().__init__(bus_id, capacity, route_number, driver_name,
                        current_speed, status, has_wifi, has_toilet, comfort_level)
    
    def get_info(self) -> str:
        wifi = "WiFi" if self._has_wifi else "нет WiFi"
        return f"Туристический {self._id}: {wifi}, комфорт {self._comfort_level}★, {self._status.value}"
    
    def needs_service(self) -> bool:
        return self.is_broken or self._speed > 80
    
    def service(self) -> str:
        self.send_to_maintenance()
        return f"Туристический {self._id}: полное ТО, чистка салона, проверка кондиционера"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Bus):
            raise TypeError("Можно сравнивать только с объектами Bus")
        other_comfort = getattr(other, '_comfort_level', 0)
        if self._comfort_level < other_comfort:
            return -1
        elif self._comfort_level == other_comfort:
            return 0
        return 1


class ServiceableCityBus(CityBus, IPrintable, IComparable):
    """Городской автобус с реализацией интерфейсов (без IServiceable)"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_validator=True, has_usb_ports=False):
        super().__init__(bus_id, capacity, route_number, driver_name,
                        current_speed, status, has_validator, has_usb_ports)
    
    def get_info(self) -> str:
        usb = "USB" if self._has_usb_ports else "нет USB"
        return f"Городской {self._id}: {self._passengers_count}/{self._capacity} пасс., {usb}, {self._status.value}"
    
    def compare_to(self, other) -> int:
        if not isinstance(other, Bus):
            raise TypeError("Можно сравнивать только с объектами Bus")
        my_load = self._passengers_count / self._capacity if self._capacity > 0 else 1
        other_load = getattr(other, '_passengers_count', 0) / getattr(other, '_capacity', 1) if getattr(other, '_capacity', 0) > 0 else 0.5
        if my_load < other_load:
            return 1
        elif my_load == other_load:
            return 0
        return -1


class ServiceableSchoolBus(SchoolBus, IPrintable, IServiceable):
    """Школьный автобус с реализацией интерфейсов"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_escort=True, max_speed_limit=70):
        super().__init__(bus_id, capacity, route_number, driver_name,
                        current_speed, status, has_escort, max_speed_limit)
    
    def get_info(self) -> str:
        escort = "с сопровождением" if self._has_escort else "без сопровождения"
        return f"Школьный {self._id}: детей {self._children_count}, {escort}, лимит {self._max_speed_limit} км/ч"
    
    def needs_service(self) -> bool:
        return self.is_broken
    
    def service(self) -> str:
        self.send_to_maintenance()
        return f"Школьный {self._id}: ТО, проверка ремней безопасности, аптечки"
