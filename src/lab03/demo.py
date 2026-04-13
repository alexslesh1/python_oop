"""
Лабораторная работа №3
Наследование и иерархия классов
"""

import sys
import os

# Добавляем пути для импорта
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab02'))

from base import Bus
from models import TouristBus, CityBus, SchoolBus
from enums import BusStatus
from bus_fleet import BusFleet


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def print_scenario(num, title):
    print(f"\n{'-'*50}")
    print(f" СЦЕНАРИЙ {num}: {title}")
    print(f"{'-'*50}")


print_header("ЛАБОРАТОРНАЯ РАБОТА №3 - НАСЛЕДОВАНИЕ И ПОЛИМОРФИЗМ")

# СЦЕНАРИЙ 1: Создание объектов разных типов
print_scenario(1, "Создание объектов разных типов")

regular_bus = Bus("R001", 40, 10, "Иванов")
tourist_bus = TouristBus("T001", 35, 20, "Петров", 
                          current_speed=0, status=BusStatus.ON_PARKING,
                          has_wifi=True, has_toilet=True, comfort_level=5)
city_bus = CityBus("C001", 50, 15, "Сидоров",
                   current_speed=0, status=BusStatus.ON_PARKING,
                   has_validator=True, has_usb_ports=True)
school_bus = SchoolBus("S001", 30, 5, "Козлов",
                       current_speed=0, status=BusStatus.ON_PARKING,
                       has_escort=True, max_speed_limit=70)

print("Созданы объекты:")
print(regular_bus)
print("\n" + "-"*40)
print(tourist_bus)
print("\n" + "-"*40)
print(city_bus)
print("\n" + "-"*40)
print(school_bus)

# СЦЕНАРИЙ 2: Работа с методами дочерних классов
print_scenario(2, "Работа с методами дочерних классов")

print("Туристический автобус:")
print(tourist_bus.start_route())
print(tourist_bus.serve_snacks())
print(f"Стоимость проезда: {tourist_bus.calculate_fare()} руб.")

print("\nГородской автобус:")
print(city_bus.start_route())
print(city_bus.board_passenger())
print(city_bus.board_passenger())
print(f"Стоимость проезда: {city_bus.calculate_fare()} руб.")

print("\nШкольный автобус:")
print(school_bus.start_route())
print(school_bus.board_child())
print(school_bus.play_educational_video())
print(f"Стоимость проезда: {school_bus.calculate_fare()} руб.")

# СЦЕНАРИЙ 3: Полиморфизм и проверка типов
print_scenario(3, "Полиморфизм и проверка типов")

fleet = BusFleet()
fleet.add(regular_bus)
fleet.add(tourist_bus)
fleet.add(city_bus)
fleet.add(school_bus)

print("Полиморфный вызов calculate_fare():")
for bus in fleet:
    print(f"   {bus.bus_id} ({bus.get_bus_type()}): {bus.calculate_fare()} руб.")

print("\nПроверка типов (isinstance):")
for bus in fleet:
    if isinstance(bus, TouristBus):
        print(f"   {bus.bus_id} - Туристический (Wi-Fi: {bus.has_wifi})")
    elif isinstance(bus, CityBus):
        print(f"   {bus.bus_id} - Городской (Валидатор: {bus.has_validator})")
    elif isinstance(bus, SchoolBus):
        print(f"   {bus.bus_id} - Школьный (Сопровождающий: {bus.has_escort})")
    elif isinstance(bus, Bus):
        print(f"   {bus.bus_id} - Обычный")

# СЦЕНАРИЙ 4: Фильтрация по типу
print_scenario(4, "Фильтрация коллекции по типу")

def filter_by_type(collection, bus_type):
    filtered = BusFleet()
    for bus in collection:
        if isinstance(bus, bus_type):
            filtered.add(bus)
    return filtered

tourist_buses = filter_by_type(fleet, TouristBus)
city_buses = filter_by_type(fleet, CityBus)
school_buses = filter_by_type(fleet, SchoolBus)

print(f"Туристических автобусов: {len(tourist_buses)}")
for bus in tourist_buses:
    print(f"   {bus.bus_id} - Комфорт: {bus.comfort_level}★")

print(f"\nГородских автобусов: {len(city_buses)}")
for bus in city_buses:
    print(f"   {bus.bus_id} - USB: {bus.has_usb_ports}")

print(f"\nШкольных автобусов: {len(school_buses)}")
for bus in school_buses:
    print(f"   {bus.bus_id} - Лимит: {bus.max_speed_limit} км/ч")

# СЦЕНАРИЙ 5: Уникальное поведение
print_scenario(5, "Уникальное поведение")

school_bus2 = SchoolBus("S002", 25, 8, "Морозов",
                        current_speed=0, status=BusStatus.ON_PARKING,
                        has_escort=True, max_speed_limit=65)

print("Школьный автобус с лимитом 65 км/ч:")
print(school_bus2.start_route())
print(school_bus2.accelerate(40))
print(f"Скорость: {school_bus2.speed} км/ч")

try:
    print(school_bus2.accelerate(30))
except ValueError as e:
    print(f"Ошибка: {e}")

print("\nТуристический автобус - сервис:")
print(tourist_bus.serve_snacks())

# ИТОГ
print_header("ИТОГ")
print(f"Всего создано автобусов: {Bus._total_buses}")
print(f"Размер коллекции: {len(fleet)}")
print('='*60)