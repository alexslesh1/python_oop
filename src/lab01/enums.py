from enum import Enum

class BusStatus(Enum):
    """Состояния автобуса"""
    ON_ROUTE = "На маршруте"
    ON_PARKING = "На парковке"
    MAINTENANCE = "На обслуживании"