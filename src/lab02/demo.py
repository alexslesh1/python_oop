
import sys
import os

# Добавляем путь к lab01 для импорта моделей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))

from models import Bus
from enums import BusStatus
from bus_fleet import BusFleet
from datetime import datetime


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def print_scenario(num, title):
    print(f"\n{'-'*50}")
    print(f" СЦЕНАРИЙ {num}: {title}")
    print(f"{'-'*50}")


print_header("ЛАБОРАТОРНАЯ РАБОТА №2 - КЛАСС-КОЛЛЕКЦИЯ BUSFLEET")


print_scenario(1, "Базовые операции с коллекцией")

fleet = BusFleet()
print("Создана пустая коллекция")
print(f"Размер коллекции (len): {len(fleet)}")

bus1 = Bus("B001", 50, 15, "Иванов")
bus2 = Bus("B002", 40, 22, "Петров")
bus3 = Bus("B003", 45, 15, "Сидоров")

print("\nДобавление автобусов:")
print(fleet.add(bus1))
print(fleet.add(bus2))
print(fleet.add(bus3))

print(f"\nРазмер коллекции после добавления: {len(fleet)}")
print("\nСодержимое коллекции (get_all):")
for bus in fleet.get_all():
    print(f"   {bus.bus_id} - маршрут {bus.route_number}")

print("\nУдаление автобуса:")
print(fleet.remove(bus2))
print(f"\nСодержимое после удаления:")
for bus in fleet.get_all():
    print(f"   {bus.bus_id} - маршрут {bus.route_number}")

print("\nПроверка неправильного типа:")
try:
    fleet.add("Не автобус")
except TypeError as e:
    print(f"   Ошибка: {e}")


print_scenario(2, "Поиск, итерация и защита от дубликатов")


fleet.add(bus2)

print("Поиск по ID (find_by_id):")
found = fleet.find_by_id("B001")
print(f"   Найден: {found.bus_id} - маршрут {found.route_number} - водитель {found.driver_name}")

print("\nПоиск по маршруту (find_by_route):")
for bus in fleet.find_by_route(15):
    print(f"   {bus.bus_id} - водитель {bus.driver_name}")

print("\nПоиск по водителю (find_by_driver):")
for bus in fleet.find_by_driver("Иванов"):
    print(f"   {bus.bus_id} - маршрут {bus.route_number}")

print("\nИтерация по коллекции (for item in fleet):")
for bus in fleet:
    print(f"   {bus.bus_id}: скорость {bus.speed} км/ч")

print(f"\nДлина коллекции (len): {len(fleet)}")

print("\nПроверка на дубликаты (нельзя добавить автобус с тем же ID):")
try:
    fleet.add(Bus("B001", 55, 30, "Николаев"))
except ValueError as e:
    print(f"   Ошибка: {e}")

print_scenario(3, "Индексация, сортировка и фильтрация")

bus4 = Bus("B004", 55, 30, "Козлов", 45, BusStatus.ON_ROUTE)
bus5 = Bus("B005", 60, 15, "Михайлов", 30, BusStatus.ON_ROUTE)
bus6 = Bus("B006", 35, 40, "Федоров", 0, BusStatus.MAINTENANCE)

fleet.add(bus4)
fleet.add(bus5)
fleet.add(bus6)

print("Исходная коллекция (__str__):")
print(fleet)

print("\nИндексация (__getitem__):")
print(f"   fleet[0]: {fleet[0].bus_id}")
print(f"   fleet[2]: {fleet[2].bus_id}")
print(f"   fleet[-1]: {fleet[-1].bus_id} (последний элемент)")
print(f"   fleet[-2]: {fleet[-2].bus_id} (предпоследний)")

print("\nСрез (fleet[1:4]):")
slice_fleet = fleet[1:4]
print(f"   Получено {len(slice_fleet)} автобусов")
for bus in slice_fleet:
    print(f"   {bus.bus_id}")

print("\nУдаление по индексу (remove_at):")
print(fleet.remove_at(2))
print(f"   После удаления: {len(fleet)} автобусов")

print("\nСортировка по ID (sort_by_id):")
fleet.sort_by_id()
for bus in fleet:
    print(f"   {bus.bus_id} - маршрут {bus.route_number}")

print("\nСортировка по скорости (sort_by_speed):")
fleet.sort_by_speed()
for bus in fleet:
    print(f"   {bus.bus_id} - скорость {bus.speed} км/ч")

print("\nСортировка по маршруту (sort_by_route):")
fleet.sort_by_route()
for bus in fleet:
    print(f"   {bus.bus_id} - маршрут {bus.route_number}")

print("\nФильтрация: автобусы на маршруте (get_on_route):")
on_route = fleet.get_on_route()
print(f"   Найдено: {len(on_route)} автобусов")
for bus in on_route:
    print(f"   {bus.bus_id} - скорость {bus.speed} км/ч")

print("\nФильтрация: автобусы, требующие ТО (get_needs_maintenance):")
needs_to = fleet.get_needs_maintenance()
print(f"   Найдено: {len(needs_to)} автобусов")
for bus in needs_to:
    print(f"   {bus.bus_id}")

print("\nФильтрация: автобусы со скоростью >= 30 км/ч (get_by_min_speed):")
fast_buses = fleet.get_by_min_speed(30)
print(f"   Найдено: {len(fast_buses)} автобусов")
for bus in fast_buses:
    print(f"   {bus.bus_id} - {bus.speed} км/ч")

print("\nПроверка наличия (__contains__):")
print(f"   bus1 в коллекции? {bus1 in fleet}")
print(f"   bus2 в коллекции? {bus2 in fleet}")


print_scenario(4, "Очистка коллекции")

print("Очистка коллекции (clear):")
print(fleet.clear())
print(f"Размер коллекции после очистки: {len(fleet)}")

print_header("ИТОГ")
print(f"Всего создано автобусов: {Bus._total_buses}")
print(f"Текущий размер коллекции: {len(fleet)}")
print(f"\nПример repr коллекции:")
print(repr(fleet))
print(f"\nПример repr автобуса:")
print(repr(bus1))
print('='*60)