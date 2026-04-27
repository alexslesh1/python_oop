import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab01'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab02'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'lab03'))
sys.path.insert(0, os.path.dirname(__file__))

from bus_fleet import BusFleet
from enums import BusStatus
from interfaces import IPrintable, IServiceable, IComparable
from bus_models import (
    ServiceableBus, 
    ServiceableTouristBus, 
    ServiceableCityBus, 
    ServiceableSchoolBus
)


def print_header(text):
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def print_scenario(num, title):
    print(f"\n{'-'*50}")
    print(f" СЦЕНАРИЙ {num}: {title}")
    print(f"{'-'*50}")


def print_all_objects(items):
    """Функция, работающая через интерфейс IPrintable"""
    for item in items:
        if isinstance(item, IPrintable):
            print(f"   {item.get_info()}")
        else:
            print(f"   {item} - не реализует IPrintable")


def service_all(items):
    """Обслужить все объекты, реализующие IServiceable"""
    for item in items:
        if isinstance(item, IServiceable):
            if item.needs_service():
                print(f"   НУЖНО ТО: {item.get_info()}")
                print(f"      -> {item.service()}")
            else:
                print(f"   OK: {item.get_info()}")


def filter_by_interface(collection, interface):
    """Фильтрация коллекции по интерфейсу"""
    filtered = BusFleet()
    for item in collection.get_all():
        if isinstance(item, interface):
            filtered.add(item)
    return filtered


print_header("ЛАБОРАТОРНАЯ РАБОТА №4 - ИНТЕРФЕЙСЫ (ABC)")

print("\nСоздание объектов с реализацией интерфейсов:")

bus1 = ServiceableBus("B001", 40, 15, "Иванов")
bus2 = ServiceableTouristBus("T001", 35, 20, "Петров", 
                              current_speed=0, status=BusStatus.ON_PARKING,
                              has_wifi=True, has_toilet=True, comfort_level=5)
bus3 = ServiceableCityBus("C001", 50, 15, "Сидоров",
                          current_speed=0, status=BusStatus.ON_PARKING,
                          has_validator=True, has_usb_ports=True)
bus4 = ServiceableSchoolBus("S001", 30, 5, "Козлов",
                            current_speed=0, status=BusStatus.ON_PARKING,
                            has_escort=True, max_speed_limit=70)

fleet = BusFleet()
fleet.add(bus1)
fleet.add(bus2)
fleet.add(bus3)
fleet.add(bus4)

print(f"\nВсего создано объектов: {len(fleet)}")

print_scenario(1, "Базовые операции через интерфейсы")

print("\nВывод через IPrintable.get_info():")
for bus in fleet.get_all():
    print(f"   {bus.get_info()}")

print("\nПроверка IServiceable.needs_service():")
for bus in fleet.get_all():
    if isinstance(bus, IServiceable):
        print(f"   {bus.bus_id}: нуждается в ТО? {bus.needs_service()}")

print("\nСравнение через IComparable.compare_to():")
if len(fleet) >= 2:
    result = fleet[0].compare_to(fleet[1])
    if result < 0:
        print(f"   {fleet[0].bus_id} меньше {fleet[1].bus_id}")
    elif result == 0:
        print(f"   {fleet[0].bus_id} равно {fleet[1].bus_id}")
    else:
        print(f"   {fleet[0].bus_id} больше {fleet[1].bus_id}")

print_scenario(2, "Полиморфизм - единая функция для всех IPrintable")

print("\nФункция print_all_objects() работает с любыми IPrintable:")
print_all_objects(fleet.get_all())

print("\nПроверка типов через isinstance():")
for bus in fleet.get_all():
    print(f"   {bus.bus_id}:")
    print(f"      IPrintable: {isinstance(bus, IPrintable)}")
    print(f"      IServiceable: {isinstance(bus, IServiceable)}")
    print(f"      IComparable: {isinstance(bus, IComparable)}")

print_scenario(3, "Обслуживание объектов через интерфейс IServiceable")

print("\nЗапускаем автобусы для демонстрации:")
bus1.start_route()
bus1.accelerate(20)
bus2.start_route()
bus2.accelerate(50)
bus3.start_route()
bus4.start_route()

print("\nСостояние после поездки:")
for bus in fleet.get_all():
    print(f"   {bus.bus_id}: скорость {bus.speed} км/ч, состояние {bus.status.value}")

print("\nПроверка необходимости ТО:")
service_all(fleet.get_all())

print_scenario(4, "Интеграция с коллекцией - фильтрация по интерфейсу")

printable_buses = filter_by_interface(fleet, IPrintable)
serviceable_buses = filter_by_interface(fleet, IServiceable)
comparable_buses = filter_by_interface(fleet, IComparable)

print(f"\nОбъектов, реализующих IPrintable: {len(printable_buses)}")
for bus in printable_buses.get_all():
    print(f"   {bus.bus_id}")

print(f"\nОбъектов, реализующих IServiceable: {len(serviceable_buses)}")
for bus in serviceable_buses.get_all():
    print(f"   {bus.bus_id}")

print(f"\nОбъектов, реализующих IComparable: {len(comparable_buses)}")
for bus in comparable_buses.get_all():
    print(f"   {bus.bus_id}")

print_scenario(5, "Разное поведение одинаковых методов")

print("\nДемонстрация полиморфизма get_info():")
for bus in fleet.get_all():
    print(f"   {bus.get_info()}")

print("\nДемонстрация полиморфизма needs_service():")
for bus in fleet.get_all():
    if isinstance(bus, IServiceable):
        print(f"   {bus.bus_id}: {bus.needs_service()}")

# ИТОГ
print_header("ИТОГ")
print(f"Всего создано автобусов: {len(fleet)}")
print(f"Реализовано интерфейсов: IPrintable, IServiceable, IComparable")
print('='*60)
