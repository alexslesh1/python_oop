"""
Лабораторная работа №5
Демонстрация функций как аргументов, стратегий и делегатов
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab04'))
sys.path.insert(0, os.path.dirname(__file__))

from enums import BusStatus
from bus_models import (
    ServiceableBus, 
    ServiceableTouristBus, 
    ServiceableCityBus, 
    ServiceableSchoolBus
)
from collection import ExtendedBusFleet
from strategies import (
    by_bus_id, by_capacity, by_speed, by_route_number,
    is_on_route, is_on_parking, needs_maintenance_filter, is_tourist_bus,
    speed_above_threshold, capacity_below_threshold,
    to_info_string, extract_ids,
    SortByIdStrategy, NeedsMaintenanceStrategy, DiscountStrategy, ActivateStrategy
)


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def print_scenario(num, title):
    print(f"\n{'-'*50}")
    print(f" СЦЕНАРИЙ {num}: {title}")
    print(f"{'-'*50}")


# ========== СОЗДАНИЕ ОБЪЕКТОВ ==========
print("Создание объектов...")

bus1 = ServiceableBus("B003", 40, 15, "Иванов")
bus2 = ServiceableTouristBus("T001", 35, 20, "Петров", has_wifi=True, comfort_level=5)
bus3 = ServiceableCityBus("C002", 50, 15, "Сидоров", has_usb_ports=True)
bus4 = ServiceableSchoolBus("S001", 30, 5, "Козлов", has_escort=True)
bus5 = ServiceableBus("B001", 45, 25, "Михайлов")
bus6 = ServiceableTouristBus("T002", 32, 18, "Алексеева", has_wifi=False, comfort_level=3)
bus7 = ServiceableCityBus("C001", 55, 10, "Новиков", has_validator=True)

fleet = ExtendedBusFleet()
for bus in [bus1, bus2, bus3, bus4, bus5, bus6, bus7]:
    fleet.add(bus)

print_header("ЛАБОРАТОРНАЯ РАБОТА №5 - СТРАТЕГИИ И ДЕЛЕГАТЫ")


# ========== СЦЕНАРИЙ 1: Сортировка тремя разными стратегиями ==========
print_scenario(1, "Сортировка тремя разными стратегиями")

print("\nИсходная коллекция (порядок добавления):")
for bus in fleet.get_all():
    print(f"   {bus.bus_id} | {bus.capacity} мест | маршрут {bus.route_number}")

print("\n1. Сортировка по ID (by_bus_id):")
fleet.sort_by(by_bus_id)
for bus in fleet.get_all():
    print(f"   {bus.bus_id} | {bus.capacity} мест")

print("\n2. Сортировка по вместимости (by_capacity):")
fleet.sort_by(by_capacity)
for bus in fleet.get_all():
    print(f"   {bus.bus_id} | {bus.capacity} мест")

print("\n3. Сортировка по маршруту (by_route_number):")
fleet.sort_by(by_route_number)
for bus in fleet.get_all():
    print(f"   {bus.bus_id} | маршрут {bus.route_number}")


# ========== СЦЕНАРИЙ 2: Фильтрация двумя разными фильтрами ==========
print_scenario(2, "Фильтрация двумя разными фильтрами")

print("\nЗапускаем первые 4 автобуса на маршрут...")
for bus in fleet.get_all()[:4]:
    try:
        bus.start_route()
        bus.accelerate(20)
        print(f"   {bus.bus_id} - выехал на маршрут (скорость {bus.speed} км/ч)")
    except Exception as e:
        print(f"   {bus.bus_id} - ошибка: {e}")

print("\nФильтр 'на маршруте' (is_on_route):")
on_route = fleet.filter_by(is_on_route)
print(f"   Автобусов на маршруте: {len(on_route)}")
for bus in on_route.get_all():
    print(f"      {bus.bus_id} - скорость {bus.speed} км/ч")

print("\nФильтр 'требуют ТО' (needs_maintenance_filter):")
needs_maintenance = fleet.filter_by(needs_maintenance_filter)
print(f"   Автобусов, требующих ТО: {len(needs_maintenance)}")
for bus in needs_maintenance.get_all():
    print(f"      {bus.bus_id}")


# ========== СЦЕНАРИЙ 3: Применение map и filter (фабрики) ==========
print_scenario(3, "Применение map и filter (фабрики функций)")

print("\nmap: преобразование в строки (to_info_string):")
info_strings = fleet.map(to_info_string)
for s in info_strings:
    print(f"   {s}")

print("\nmap: извлечение ID автобусов:")
ids = fleet.map(extract_ids)
print(f"   {ids}")

print("\nФабрика функций: фильтр по скорости >= 40 км/ч:")
high_speed_filter = speed_above_threshold(40)
fast_buses = fleet.filter_by(high_speed_filter)
print(f"   Быстрых автобусов: {len(fast_buses)}")
for bus in fast_buses.get_all():
    print(f"      {bus.bus_id} - {bus.speed} км/ч")

print("\nФабрика функций: фильтр по вместимости <= 40:")
low_capacity_filter = capacity_below_threshold(40)
small_buses = fleet.filter_by(low_capacity_filter)
print(f"   Маленьких автобусов: {len(small_buses)}")
for bus in small_buses.get_all():
    print(f"      {bus.bus_id} - {bus.capacity} мест")

print("\nlambda выражение: сортировка по пассажирам:")
fleet.sort_by(lambda b: getattr(b, 'passengers_count', 0))
for bus in fleet.get_all():
    print(f"   {bus.bus_id} - пассажиров: {getattr(bus, 'passengers_count', 0)}")


# ========== СЦЕНАРИЙ 4: Callable-объекты как стратегии ==========
print_scenario(4, "Callable-объекты как стратегии")

print("\nСтратегия сортировки через callable-объект SortByIdStrategy():")
sort_strategy = SortByIdStrategy()
fleet.sort_by(sort_strategy)
for bus in fleet.get_all():
    print(f"   {bus.bus_id}")

print("\nСтратегия фильтрации через callable-объект NeedsMaintenanceStrategy():")
filter_strategy = NeedsMaintenanceStrategy()
needs_maintenance2 = fleet.filter_by(filter_strategy)
print(f"   Автобусов, требующих ТО: {len(needs_maintenance2)}")
for bus in needs_maintenance2.get_all():
    print(f"      {bus.bus_id}")

print("\nСтратегия применения скидки (DiscountStrategy 15%):")
discount_strategy = DiscountStrategy(0.15)
discount_results = fleet.apply(discount_strategy)
for result in discount_results[:5]:
    print(f"   {result}")

print("\nСтратегия активации (ActivateStrategy):")
activate_strategy = ActivateStrategy(True)
parked_buses = fleet.filter_by(is_on_parking)
activate_results = parked_buses.apply(activate_strategy)
for result in activate_results[:3]:
    print(f"   {result}")


# ========== СЦЕНАРИЙ 5: Цепочка операций ==========
print_scenario(5, "Цепочка операций filter -> sort -> apply")

print("\nИсходное состояние коллекции:")
print(f"   Всего автобусов: {len(fleet)}")

print("\nСобираем только туристические автобусы...")
tourist_buses = ExtendedBusFleet()
for bus in fleet.get_all():
    if is_tourist_bus(bus):
        tourist_buses.add(bus)

print(f"   Туристических автобусов: {len(tourist_buses)}")

print("\nСортировка туристических автобусов по комфорту (от большего к меньшему):")
tourist_buses.sort_by(lambda b: getattr(b, 'comfort_level', 0), reverse=True)
for bus in tourist_buses.get_all():
    comfort = getattr(bus, 'comfort_level', 0)
    print(f"      {bus.bus_id} - комфорт {comfort}★, обычная цена: {bus.calculate_fare()} руб.")

print("\nПрименение скидки 20% к туристическим автобусам:")
discount_20 = DiscountStrategy(0.2)
for bus in tourist_buses.get_all():
    result = discount_20(bus)
    print(f"      {result}")


# ========== ИТОГ ==========
print_header("ИТОГ")
print(f"Всего создано автобусов: {len(fleet)}")
print(f"Всего объектов в коллекции: 7")
print(f"Реализовано стратегий: сортировки (6), фильтрации (6), callable-объектов (5)")
print(f"Демонстрация: sorted, map, filter, lambda, фабрики функций, цепочки операций")
print('='*60)