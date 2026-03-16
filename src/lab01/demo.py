from models import Driver, Route, Bus, Ticket
from enums import BusStatus, TicketStatus

def header(text): print(f"\n{'='*60}\n{text}\n{'='*60}")
def scene(num, title): print(f"\n{'-'*40}\n{num}. {title}\n{'-'*40}")

d = Driver("Иванов Петр", "77АА123456", 15, "D")
r = Route(15, "Вокзал", "Аэропорт", 25, 45)
b = Bus("А123ВС", 50, r, d)
t1, t2 = Ticket("T001", r, 500, "A1"), Ticket("T002", r, 500, "A2")

header("ТРАНСПОРТНАЯ СИСТЕМА")
print(f"Всего: Drivers {Driver._total}, Routes {Route._total}, "
      f"Buses {Bus._total}, Tickets {Ticket._total}")

scene(1, "ОРГАНИЗАЦИЯ ПЕРЕВОЗКИ")
print(d, r, b, t1, sep="\n")

print("\n🚌 Работа автобуса:")
print(b.start_route())
print(f"Ускорение: {b.accelerate(20)} км/ч")
print(f"Торможение: {b.brake(25)} км/ч")

print("\n🎫 Продажа билетов:")
print(t1.buy())
print(t2.buy())

print("\n🔍 Сравнение:")
b2 = Bus("В456СМ", 40)
print(f"b1 == b2: {b == b2}")
print(f"t1 == t2: {t1 == t2}")

scene(2, "ПРОВЕРКА ВАЛИДАЦИИ")

tests = [
    ("Водитель со стажем -5", lambda: Driver("Сидоров", "77ББ789", -5, "D")),
    ("Маршрут с нулевым расстоянием", lambda: Route(25, "A", "B", 0, 30)),
    ("Автобус со скоростью 150", lambda: Bus("С789ОР", 40, speed=150)),
    ("Билет с ценой -100", lambda: Ticket("T003", r, -100))
]

for desc, test in tests:
    try:
        test()
        print(f"❌ {desc}: ДОЛЖНО БЫТЬ ОШИБКА")
    except Exception as e:
        print(f"✅ {desc}: {e}")

print("\n🔄 Работа сеттера:")
print(f"Стаж до: {d.experience}")
d.experience = 16
print(f"Стаж после: {d.experience}")

scene(3, "ПОВЕДЕНИЕ ОТ СОСТОЯНИЯ")

b3 = Bus("D001", 45, r)  
print(f"\n🚌 Начальное: {b3.status.value}")

try:
    b3.accelerate(10)
except Exception as e:
    print(f"❌ Ускорение на парковке: {e}")

print(b3.start_route())
print(b3.send_to_maintenance())

try:
    b3.speed = 20
except Exception as e:
    print(f"❌ Изменение скорости на ТО: {e}")

t3 = Ticket("T999", r, 750)
print(f"\n🎫 Начальное: {t3.status.value}")
print(t3.buy())

try:
    t3.buy()
except Exception as e:
    print(f"❌ Повторная покупка: {e}")

print(t3.use())

try:
    t3.use()
except Exception as e:
    print(f"❌ Повторное использование: {e}")

print(f"\n🔧 Нужно ТО? {b3.needs_maintenance()}")
print(f"\nРепрезентация: {repr(b)}")
print('='*60)


