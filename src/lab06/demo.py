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
from container import (
    TypedCollection, 
    Displayable, Scorable, 
    D, S,
    DisplayableBusAdapter, 
    ScorableBusAdapter
)


def print_header(text: str) -> None:
    print(f"\n{'='*60}")
    print(f" {text}")
    print(f"{'='*60}")


def print_scenario(num: int, title: str) -> None:
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

print_header("ЛАБОРАТОРНАЯ РАБОТА №6 - GENERICS И TYPING")


# ========== СЦЕНАРИЙ 1: Generic-коллекция (оценка 3) ==========
print_scenario(1, "Generic-коллекция TypedCollection")

# Создание типизированной коллекции для автобусов
bus_collection: TypedCollection[ServiceableBus] = TypedCollection()

print("Добавление автобусов в коллекцию:")
bus_collection.add(bus1)
bus_collection.add(bus2)
bus_collection.add(bus3)
bus_collection.add(bus4)
bus_collection.add(bus5)
bus_collection.add(bus6)
bus_collection.add(bus7)

print(f"Размер коллекции: {len(bus_collection)}")
print(f"\nВсе элементы коллекции:")
for bus in bus_collection:
    print(f"   {bus.bus_id} | {bus.capacity} мест | маршрут {bus.route_number}")

print("\nДемонстрация __getitem__:")
print(f"   Элемент с индексом 0: {bus_collection[0].bus_id}")
print(f"   Элемент с индексом 3: {bus_collection[3].bus_id}")

print("\nУдаление элемента:")
bus_collection.remove(bus1)
print(f"   Автобус {bus1.bus_id} удален")
print(f"   Размер после удаления: {len(bus_collection)}")


# ========== СЦЕНАРИЙ 2: Поиск и фильтрация (оценка 4) ==========
print_scenario(2, "Поиск и фильтрация (find, filter, map)")

# Запускаем автобусы на маршрут для демонстрации
for bus in bus_collection.get_all():
    try:
        bus.start_route()
        bus.accelerate(30)
    except:
        pass

print("\nfind() - поиск автобуса по ID:")
found = bus_collection.find(lambda b: b.bus_id == "T001")
if found:
    print(f"   Найден: {found.bus_id} | скорость {found.speed} км/ч")

not_found = bus_collection.find(lambda b: b.bus_id == "XXX")
print(f"   Поиск несуществующего: {not_found} (None)")

print("\nfilter() - фильтрация автобусов по скорости >= 50 км/ч:")
fast_buses = bus_collection.filter(lambda b: b.speed >= 50)
print(f"   Найдено: {len(fast_buses)} автобусов")
for bus in fast_buses:
    print(f"      {bus.bus_id} - скорость {bus.speed} км/ч")

print("\nfilter() - фильтрация автобусов по вместимости >= 45:")
large_buses = bus_collection.filter(lambda b: b.capacity >= 45)
print(f"   Найдено: {len(large_buses)} автобусов")
for bus in large_buses:
    print(f"      {bus.bus_id} - вместимость {bus.capacity}")

print("\nmap() - преобразование в список ID (изменение типа):")
bus_ids = bus_collection.map(lambda b: b.bus_id)
print(f"   Тип результата: {type(bus_ids).__name__}[{type(bus_ids[0]).__name__}]")
print(f"   Результат: {bus_ids}")

print("\nmap() - преобразование в список стоимостей проезда (изменение типа):")
bus_fares = bus_collection.map(lambda b: b.calculate_fare())
print(f"   Тип результата: {type(bus_fares).__name__}[{type(bus_fares[0]).__name__}]")
print(f"   Результат: {bus_fares}")

print("\nmap() - преобразование в строки:")
bus_strings = bus_collection.map(lambda b: f"{b.bus_id} - {b.speed} км/ч")
for s in bus_strings[:3]:
    print(f"   {s}")


# ========== СЦЕНАРИЙ 3: Protocols (оценка 5) ==========
print_scenario(3, "Protocols - структурная типизация")

# Создаем адаптеры, реализующие Protocols
displayable_buses = []
scorable_buses = []

# Получаем автобусы заново
all_buses = [bus2, bus3, bus4, bus5, bus6, bus7]

for bus in all_buses:
    displayable_buses.append(DisplayableBusAdapter(bus))
    scorable_buses.append(ScorableBusAdapter(bus))

print("Displayable Protocol - объекты с методом display():")
print("   Классы адаптеров не наследуются от Displayable, но имеют метод display()")
print("\n   Вызов display():")
for adapter in displayable_buses[:4]:
    print(f"      {adapter.display()}")

print("\nScorable Protocol - объекты с методом score():")
print("\n   Вызов score() (стоимость проезда):")
for adapter in scorable_buses[:4]:
    print(f"      {adapter.get_bus().bus_id}: {adapter.score()} руб.")


# ========== СЦЕНАРИЙ 4: TypedCollection с ограничениями (оценка 5) ==========
print_scenario(4, "TypedCollection с ограничениями (bound=Protocol)")

# Создаем коллекцию с ограничением Displayable
displayable_collection: TypedCollection[D] = TypedCollection()

print("Добавление Displayable-объектов в коллекцию:")
for adapter in displayable_buses:
    displayable_collection.add(adapter)

print(f"Размер коллекции Displayable: {len(displayable_collection)}")
print("\nИзвлечение и вызов display():")
for i, adapter in enumerate(displayable_collection.get_all()[:4]):
    print(f"   [{i}] {adapter.display()}")

print("\nСоздание коллекции с ограничением Scorable:")
scorable_collection: TypedCollection[S] = TypedCollection()

for adapter in scorable_buses:
    scorable_collection.add(adapter)

print(f"Размер коллекции Scorable: {len(scorable_collection)}")
print("\nСортировка по score:")
scorable_collection.sort_by(lambda a: a.score(), reverse=True)
sorted_adapters = scorable_collection.get_all()
for adapter in sorted_adapters[:4]:
    print(f"   {adapter.get_bus().bus_id}: {adapter.score()} руб.")

print("\nФильтрация по score >= 30:")
high_score = scorable_collection.filter(lambda a: a.score() >= 30)
print(f"   Найдено: {len(high_score)} автобусов")
for adapter in high_score:
    bus = adapter.get_bus()
    if hasattr(bus, 'comfort_level'):
        print(f"      {bus.bus_id}: {adapter.score()} руб. (туристический, комфорт {bus.comfort_level}★)")
    else:
        print(f"      {bus.bus_id}: {adapter.score()} руб.")


# ========== СЦЕНАРИЙ 5: Дополнительная демонстрация Generic ==========
print_scenario(5, "Дополнительная демонстрация Generic")

print("Коллекция ID автобусов (TypedCollection[str]):")
id_collection: TypedCollection[str] = TypedCollection()
for bus in all_buses:
    id_collection.add(bus.bus_id)
print(f"   {id_collection.get_all()}")

print("\nКоллекция вместимости автобусов (TypedCollection[int]):")
capacity_collection: TypedCollection[int] = TypedCollection()
for bus in all_buses:
    capacity_collection.add(bus.capacity)
print(f"   {capacity_collection.get_all()}")
print(f"   Максимальная вместимость: {max(capacity_collection.get_all())}")

print("\nПрименение map к коллекции строк:")
upper_ids = id_collection.map(lambda s: s.upper())
print(f"   {upper_ids}")


# ========== ИТОГ ==========
print_header("ИТОГ")
print(f"Всего создано автобусов: 7")
print(f"Generic-коллекции: TypedCollection[T]")
print(f"Реализовано Protocol: Displayable, Scorable")
print(f"TypeVar с ограничениями: D (bound=Displayable), S (bound=Scorable)")
print(f"Демонстрация: аннотации типов, Generic, find, filter, map, Protocols")
print('='*60)