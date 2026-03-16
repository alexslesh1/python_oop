from models import Bus
from datetime import datetime

def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")

def print_scenario(num, title):
    print(f"\n{'-'*50}")
    print(f" СЦЕНАРИЙ {num}: {title}")
    print(f"{'-'*50}")

print_header("ЛАБОРАТОРНАЯ РАБОТА №1 - КЛАСС BUS")

print_scenario(1, "Создание и нормальная работа")

bus1 = Bus("А123ВС", 50, 15, "Иванов")
bus2 = Bus("В456СМ", 40, 22, "Петров")

print(f"Создано автобусов: {Bus._total_buses}")
print("\nИнформация об автобусах:")
print(bus1)
print()
print(bus2)

print("\nВыезд на маршрут:")
print(bus1.start_route())

print("\nУскорение:")
print(f"Скорость после ускорения на 20: {bus1.accelerate(20)} км/ч")
print(f"Скорость после ускорения на 15: {bus1.accelerate(15)} км/ч")

print("\nТорможение до полной остановки:")
print(f"Скорость после торможения на 25: {bus1.brake(25)} км/ч")
print(f"Скорость после торможения на 40: {bus1.brake(40)} км/ч")

print("\nПарковка:")
print(bus1.park())

print("\nСравнение объектов:")
print(f"bus1 == bus2: {bus1 == bus2}")
print(f"bus1 == bus1: {bus1 == bus1}")

print_scenario(2, "Валидация и состояния")

print("Попытка создать автобус с неверными данными:")
try:
    bus_invalid = Bus("", -5, current_speed=150)
except ValueError as e:
    print(f"   Ошибка: {e}")

print("\nРабота сеттера:")
print(f"Старый маршрут bus2: {bus2.route_number}")
bus2.route_number = 25
print(f"Новый маршрут: {bus2.route_number}")

bus3 = Bus("С789ОР", 45)
print(f"\nНачальное состояние bus3: {bus3.status.value}")

print("\nПопытка ускориться на парковке:")
try:
    bus3.accelerate(10)
except ValueError as e:
    print(f"   Ошибка: {e}")

print("\nОтправка на ТО:")
print(bus3.send_to_maintenance())

print("\nПопытка изменить скорость на ТО:")
try:
    bus3.speed = 20
except ValueError as e:
    print(f"   Ошибка: {e}")

print("\nПроверка логического состояния (is_broken):")
bus4 = Bus("D001", 50, 10, "Сидоров")
bus4._last_maintenance = datetime(2024, 1, 1)
print(bus4)
print(f"Требуется ТО? {bus4.is_broken}")

print_header("ИТОГ")
print(f"Всего создано автобусов: {Bus._total_buses}")
print(f"Максимальная скорость: {Bus._MAX_SPEED} км/ч")
print(f"\nПример repr:")
print(repr(bus1))
print('='*60)