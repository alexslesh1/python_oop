"""
Дочерние классы автобусов
TouristBus, CityBus, SchoolBus
"""

from base import Bus
from enums import BusStatus


class TouristBus(Bus):
    """Туристический автобус - для дальних поездок и экскурсий"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_wifi=True, has_toilet=False, comfort_level=3):
        """
        Дополнительные атрибуты:
        - has_wifi: наличие Wi-Fi
        - has_toilet: наличие туалета
        - comfort_level: уровень комфорта (1-5)
        """
        # Вызов конструктора базового класса
        super().__init__(bus_id, capacity, route_number, driver_name, current_speed, status)
        
        # Новые атрибуты
        self._has_wifi = has_wifi
        self._has_toilet = has_toilet
        self._comfort_level = comfort_level
    
    # Новые методы
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
        """Подать закуски (новый метод)"""
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Подача закусков возможна только на маршруте")
        return "🍪 Пассажирам поданы закуски и напитки"
    
    # Переопределение полиморфного метода (оценка 4)
    def calculate_fare(self):
        """Стоимость проезда для туристического автобуса"""
        base_fare = super().calculate_fare()
        # Дополнительная надбавка за комфорт
        comfort_bonus = self._comfort_level * 50
        wifi_bonus = 30 if self._has_wifi else 0
        toilet_bonus = 40 if self._has_toilet else 0
        return base_fare + comfort_bonus + wifi_bonus + toilet_bonus
    
    def get_bus_type(self):
        """Переопределение метода"""
        return "Туристический автобус"
    
    # Переопределение __str__ (оценка 4)
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
        """
        Дополнительные атрибуты:
        - has_validator: наличие валидатора билетов
        - has_usb_ports: наличие USB-портов для зарядки
        """
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
        """Посадка пассажира (новый метод)"""
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Посадка возможна только на маршруте")
        if self._passengers_count >= self._capacity:
            raise ValueError("Автобус переполнен")
        self._passengers_count += 1
        return f"Пассажир сел в автобус. Всего: {self._passengers_count}/{self._capacity}"
    
    def alight_passenger(self):
        """Высадка пассажира"""
        if self._passengers_count <= 0:
            raise ValueError("В автобусе нет пассажиров")
        self._passengers_count -= 1
        return f"Пассажир вышел. Осталось: {self._passengers_count}"
    
    def calculate_fare(self):
        """Стоимость проезда для городского автобуса"""
        base_fare = super().calculate_fare()
        # Городской проезд дешевле
        return base_fare - 20
    
    def get_bus_type(self):
        return "Городской автобус"
    
    def __str__(self):
        base_str = super().__str__()
        validator = "есть" if self._has_validator else "нет"
        usb = "есть" if self._has_usb_ports else "нет"
        return (f"{base_str}\n"
                f"   Валидатор: {validator}\n"
                f"   USB-порты: {usb}\n"
                f"   Пассажиров в салоне: {self._passengers_count}")


class SchoolBus(Bus):
    """Школьный автобус - для перевозки детей"""
    
    def __init__(self, bus_id, capacity, route_number=None, driver_name=None,
                 current_speed=0, status=BusStatus.ON_PARKING,
                 has_escort=True, max_speed_limit=70):
        """
        Дополнительные атрибуты:
        - has_escort: наличие сопровождающего
        - max_speed_limit: ограничение скорости для школьного автобуса
        """
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
        """Посадка ребенка"""
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Посадка возможна только на маршруте")
        if self._children_count >= self._capacity:
            raise ValueError("Автобус переполнен")
        self._children_count += 1
        return f"Ребенок сел в автобус. Всего детей: {self._children_count}"
    
    def play_educational_video(self):
        """Включить обучающее видео (новый метод)"""
        if self._status != BusStatus.ON_ROUTE:
            raise ValueError("Видео можно включить только в пути")
        return "📺 Включено обучающее видео для детей"
    
    def calculate_fare(self):
        """Стоимость проезда для школьного автобуса (бесплатно)"""
        return 0.0
    
    def get_bus_type(self):
        return "Школьный автобус"
    
    def accelerate(self, increment):
        """Переопределение метода с учетом ограничения скорости"""
        new_speed = self._speed + increment
        if new_speed > self._max_speed_limit:
            raise ValueError(f"Школьный автобус не может ехать быстрее {self._max_speed_limit} км/ч")
        return super().accelerate(increment)
    
    def __str__(self):
        base_str = super().__str__()
        escort = "есть" if self._has_escort else "нет"
        return (f"{base_str}\n"
                f"   Сопровождающий: {escort}\n"
                f"   Ограничение скорости: {self._max_speed_limit} км/ч\n"
                f"   Детей в салоне: {self._children_count}")