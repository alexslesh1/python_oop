from enum import Enum
from datetime import datetime
from validators import *

# Состояния для оценки 5
class BusStatus(Enum):
    ON_ROUTE = "На маршруте"
    ON_PARKING = "На парковке"
    MAINTENANCE = "На обслуживании"

class TicketStatus(Enum):
    AVAILABLE = "Доступен"
    SOLD = "Продан"
    USED = "Использован"


class Driver:
    """Водитель"""
    _total = 0
    
    def __init__(self, name, license_num, experience, category):
        validate_driver(name, license_num, experience, category)
        self._name = name
        self._license = license_num
        self._exp = experience
        self._cat = category
        Driver._total += 1
    
    @property
    def name(self): return self._name
    @property
    def license(self): return self._license
    @property
    def experience(self): return self._exp
    @experience.setter
    def experience(self, value):
        validate_experience(value)
        self._exp = value
    
    def __str__(self):
        return f"👨‍✈️ {self._name} | Стаж: {self._exp} | Кат. {self._cat}"
    
    def __repr__(self):
        return f"Driver('{self._name}', '{self._license}', {self._exp}, '{self._cat}')"
    
    def __eq__(self, other):
        return isinstance(other, Driver) and self._license == other._license


class Route:
    """Маршрут"""
    _total = 0
    
    def __init__(self, number, start, end, distance, duration):
        validate_route(number, start, end, distance, duration)
        self._num = number
        self._start = start
        self._end = end
        self._dist = distance
        self._dur = duration
        Route._total += 1
    
    @property
    def number(self): return self._num
    @property
    def start(self): return self._start
    @property
    def end(self): return self._end
    @property
    def distance(self): return self._dist
    @property
    def duration(self): return self._dur
    
    def __str__(self):
        return f"🛣️ №{self._num} | {self._start}→{self._end} | {self._dist}км | {self._dur}мин"
    
    def __repr__(self):
        return f"Route({self._num}, '{self._start}', '{self._end}', {self._dist}, {self._dur})"
    
    def __eq__(self, other):
        return isinstance(other, Route) and self._num == other._num


class Bus:
    """Автобус"""
    _total = 0
    _MAX_SPEED = 100
    
    def __init__(self, bus_id, capacity, route=None, driver=None, 
                 speed=0, status=BusStatus.ON_PARKING):
        validate_bus(bus_id, capacity, speed, status)
        self._id = bus_id
        self._cap = capacity
        self._route = route
        self._driver = driver
        self._speed = speed
        self._status = status
        self._last_to = datetime.now()
        Bus._total += 1
    
    @property
    def bus_id(self): return self._id
    @property
    def capacity(self): return self._cap
    @property
    def route(self): return self._route
    @route.setter
    def route(self, value):
        if self._status == BusStatus.ON_ROUTE:
            raise ValueError("Нельзя сменить маршрут в пути")
        self._route = value
    
    @property
    def driver(self): return self._driver
    @driver.setter
    def driver(self, value): self._driver = value
    
    @property
    def speed(self): return self._speed
    @speed.setter
    def speed(self, value):
        validate_speed(value)
        if self._status == BusStatus.MAINTENANCE:
            raise ValueError("На ТО скорость не меняется")
        if self._status == BusStatus.ON_PARKING and value > 0:
            raise ValueError("На парковке скорость = 0")
        self._speed = value
    
    @property
    def status(self): return self._status
    
    def start_route(self):
        if self._status != BusStatus.ON_PARKING:
            raise ValueError("Автобус должен быть на парковке")
        if not self._route:
            raise ValueError("Не назначен маршрут")
        self._status = BusStatus.ON_ROUTE
        self._speed = 30
        return f"🚌 {self._id} выехал на маршрут"
    
    def park(self):
        if self._speed > 0:
            raise ValueError("Сначала остановитесь")
        self._status = BusStatus.ON_PARKING
        return f"{self._id} на парковке"
    
    def send_to_maintenance(self):
        self._status = BusStatus.MAINTENANCE
        self._speed = 0
        self._last_to = datetime.now()
        return f"{self._id} на ТО"
    
    def accelerate(self, inc):
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Ускорение только на маршруте")
        new = self._speed + inc
        validate_speed(new)
        self._speed = new
        return self._speed
    
    def brake(self, dec):
        if self._status == BusStatus.MAINTENANCE:
            raise ValueError("На ТО нельзя тормозить")
        self._speed = max(0, self._speed - dec)
        return self._speed
    
    def needs_maintenance(self):
        return (datetime.now() - self._last_to).days > 30
    
    def __str__(self):
        days = (datetime.now() - self._last_to).days
        return (f"🚌 {self._id} | Скорость: {self._speed} | "
                f"{self._status.value} | ТО: {days}дн")
    
    def __repr__(self):
        return f"Bus('{self._id}', {self._cap}, {self._speed}, {self._status})"
    
    def __eq__(self, other):
        return isinstance(other, Bus) and self._id == other._id


class Ticket:
    """Билет"""
    _total = 0
    
    def __init__(self, ticket_id, route, price, seat=None, status=TicketStatus.AVAILABLE):
        validate_ticket(ticket_id, price, status)
        self._id = ticket_id
        self._route = route
        self._price = price
        self._seat = seat
        self._status = status
        Ticket._total += 1
    
    @property
    def ticket_id(self): return self._id
    @property
    def route(self): return self._route
    @property
    def price(self): return self._price
    @property
    def status(self): return self._status
    
    def buy(self):
        if self._status != TicketStatus.AVAILABLE:
            raise ValueError(f"Билет {self._status.value}")
        self._status = TicketStatus.SOLD
        return f"🎫 {self._id} куплен за {self._price} руб."
    
    def use(self):
        if self._status != TicketStatus.SOLD:
            raise ValueError("Можно использовать только купленный билет")
        self._status = TicketStatus.USED
        return f"🎫 {self._id} использован"
    
    def __str__(self):
        seat = f"место {self._seat}" if self._seat else "без места"
        return f"🎫 {self._id} | Маршрут {self._route.number} | {self._price}руб | {seat} | {self._status.value}"
    
    def __repr__(self):
        return f"Ticket('{self._id}', {self._route.number}, {self._price}, {self._status})"
    
    def __eq__(self, other):
        return isinstance(other, Ticket) and self._id == other._id