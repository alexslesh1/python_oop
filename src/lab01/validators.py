from enums import BusStatus

def validate_bus_id(value):
    if not isinstance(value, str):
        raise ValueError("ID автобуса должен быть строкой")
    if len(value) < 1 or len(value) > 10:
        raise ValueError("ID автобуса должен быть от 1 до 10 символов")

def validate_capacity(value):
    if not isinstance(value, int):
        raise ValueError("Вместимость должна быть целым числом")
    if value <= 0 or value > 150:
        raise ValueError("Вместимость должна быть от 1 до 150")

def validate_speed(value):
    from models import Bus
    if not isinstance(value, (int, float)):
        raise ValueError("Скорость должна быть числом")
    if value < 0 or value > Bus._MAX_SPEED:
        raise ValueError(f"Скорость должна быть от 0 до {Bus._MAX_SPEED}")

def validate_status(value):
    if not isinstance(value, BusStatus):
        raise ValueError("Статус должен быть типа BusStatus")

def validate_route_number(value):
    if value is not None:
        if not isinstance(value, (int, str)):
            raise ValueError("Номер маршрута должен быть числом или строкой")
        if isinstance(value, int) and (value <= 0 or value > 999):
            raise ValueError("Номер маршрута должен быть от 1 до 999")

def validate_driver_name(value):
    if value is not None:
        if not isinstance(value, str):
            raise ValueError("Имя водителя должно быть строкой")
        if len(value) < 2:
            raise ValueError("Имя водителя должно быть не менее 2 символов")