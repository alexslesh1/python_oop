"""
Базовый класс Bus
Перенесен из lab01/models.py
"""

from datetime import datetime
import sys
import os

# Добавляем путь к lab01 для импорта
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))

from enums import BusStatus
from validators import validate_bus_id, validate_capacity, validate_speed, validate_status, validate_route_number, validate_driver_name


class Bus:
    """Базовый класс Автобус"""
    
    _total_buses = 0
    _MAX_SPEED = 100
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None, 
                 current_speed=0, status=BusStatus.ON_PARKING):
        validate_bus_id(bus_id)
        validate_capacity(capacity)
        validate_speed(current_speed)
        validate_status(status)
        validate_route_number(route_number)
        validate_driver_name(driver_name)
        
        self._id = bus_id
        self._capacity = capacity
        self._route_number = route_number
        self._driver_name = driver_name
        self._speed = current_speed
        self._status = status
        self._last_maintenance = datetime.now()
        
        Bus._total_buses += 1
    
    @property
    def bus_id(self):
        return self._id
    
    @property
    def capacity(self):
        return self._capacity
    
    @property
    def route_number(self):
        return self._route_number
    
    @route_number.setter
    def route_number(self, value):
        if self._status == BusStatus.ON_ROUTE:
            raise ValueError("Нельзя сменить маршрут во время движения")
        validate_route_number(value)
        self._route_number = value
    
    @property
    def driver_name(self):
        return self._driver_name
    
    @driver_name.setter
    def driver_name(self, value):
        validate_driver_name(value)
        self._driver_name = value
    
    @property
    def speed(self):
        return self._speed
    
    @speed.setter
    def speed(self, value):
        validate_speed(value)
        if self._status == BusStatus.MAINTENANCE:
            raise ValueError("На обслуживании скорость не меняется")
        if self._status == BusStatus.ON_PARKING and value > 0:
            raise ValueError("На парковке скорость должна быть 0")
        self._speed = value
    
    @property
    def status(self):
        return self._status
    
    @property
    def is_broken(self):
        days_since = (datetime.now() - self._last_maintenance).days
        return days_since > 30
    
    def start_route(self):
        if self._status != BusStatus.ON_PARKING:
            raise ValueError("Автобус должен быть на парковке")
        if not self._route_number:
            raise ValueError("Не назначен маршрут")
        
        self._status = BusStatus.ON_ROUTE
        self._speed = 30
        return f"Автобус {self._id} выехал на маршрут №{self._route_number}"
    
    def park(self):
        if self._speed > 0:
            raise ValueError("Сначала остановите автобус")
        self._status = BusStatus.ON_PARKING
        return f"Автобус {self._id} на парковке"
    
    def send_to_maintenance(self):
        self._status = BusStatus.MAINTENANCE
        self._speed = 0
        self._last_maintenance = datetime.now()
        return f"Автобус {self._id} на обслуживании"
    
    def accelerate(self, increment):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Ускоряться можно только на маршруте")
        
        new_speed = self._speed + increment
        validate_speed(new_speed)
        self._speed = new_speed
        return self._speed
    
    def brake(self, decrement):
        if self._status == BusStatus.MAINTENANCE:
            raise ValueError("На обслуживании нельзя тормозить")
        
        self._speed = max(0, self._speed - decrement)
        return self._speed
    
    def calculate_fare(self):
        return 50.0
    
    def get_bus_type(self):
        return "Обычный автобус"
    
    def __str__(self):
        route = f"№{self._route_number}" if self._route_number else "не назначен"
        driver = self._driver_name if self._driver_name else "нет"
        days = (datetime.now() - self._last_maintenance).days
        
        return (f"🚌 Автобус: {self._id}\n"
                f"   Тип: {self.get_bus_type()}\n"
                f"   Вместимость: {self._capacity} чел.\n"
                f"   Маршрут: {route}\n"
                f"   Водитель: {driver}\n"
                f"   Скорость: {self._speed} км/ч\n"
                f"   Состояние: {self._status.value}\n"
                f"   Стоимость проезда: {self.calculate_fare()} руб.")
    
    def __repr__(self):
        return (f"Bus(bus_id='{self._id}', capacity={self._capacity}, "
                f"route='{self._route_number}', driver='{self._driver_name}', "
                f"speed={self._speed}, status={self._status})")
    
    def __eq__(self, other):
        if not isinstance(other, Bus):
            return False
        return self._id == other._id