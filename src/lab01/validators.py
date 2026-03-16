from enums import BusStatus, TicketStatus

def validate_name(v):
    if not isinstance(v, str) or len(v.strip()) < 2:
        raise ValueError("Имя минимум 2 символа")

def validate_license(v):
    if not isinstance(v, str) or len(v) < 3:
        raise ValueError("Номер прав минимум 3 символа")

def validate_experience(v):
    if not isinstance(v, (int, float)) or v < 0 or v > 60:
        raise ValueError("Стаж от 0 до 60 лет")

def validate_category(v):
    if v not in ["A", "B", "C", "D"]:
        raise ValueError("Категория A, B, C, D")

def validate_driver(name, lic, exp, cat):
    validate_name(name)
    validate_license(lic)
    validate_experience(exp)
    validate_category(cat)

def validate_route_number(v):
    if not isinstance(v, int) or v <= 0 or v > 999:
        raise ValueError("Номер маршрута 1-999")

def validate_point(v):
    if not isinstance(v, str) or len(v.strip()) < 2:
        raise ValueError("Название пункта минимум 2 символа")

def validate_distance(v):
    if not isinstance(v, (int, float)) or v <= 0 or v > 1000:
        raise ValueError("Расстояние 1-1000 км")

def validate_duration(v):
    if not isinstance(v, (int, float)) or v <= 0 or v > 1440:
        raise ValueError("Длительность 1-1440 мин")

def validate_route(num, start, end, dist, dur):
    validate_route_number(num)
    validate_point(start)
    validate_point(end)
    validate_distance(dist)
    validate_duration(dur)

def validate_bus_id(v):
    if not isinstance(v, str) or len(v) < 1 or len(v) > 10:
        raise ValueError("ID автобуса 1-10 символов")

def validate_capacity(v):
    if not isinstance(v, int) or v <= 0 or v > 150:
        raise ValueError("Вместимость 1-150")

def validate_speed(v):
    if not isinstance(v, (int, float)) or v < 0 or v > 100:
        raise ValueError("Скорость 0-100 км/ч")

def validate_bus_status(v):
    if not isinstance(v, BusStatus):
        raise ValueError("Неверный статус")

def validate_bus(bus_id, cap, speed, status):
    validate_bus_id(bus_id)
    validate_capacity(cap)
    validate_speed(speed)
    validate_bus_status(status)

def validate_ticket_id(v):
    if not isinstance(v, str) or len(v) < 1:
        raise ValueError("ID билета не пустой")

def validate_price(v):
    if not isinstance(v, (int, float)) or v <= 0 or v > 50000:
        raise ValueError("Цена 1-50000 руб.")

def validate_ticket_status(v):
    if not isinstance(v, TicketStatus):
        raise ValueError("Неверный статус")

def validate_ticket(tid, price, status):
    validate_ticket_id(tid)
    validate_price(price)
    validate_ticket_status(status)
