from enum import Enum

class BusStatus(Enum):
    ON_ROUTE = "На маршруте"
    ON_PARKING = "На парковке"
    MAINTENANCE = "На обслуживании"

class TicketStatus(Enum):
    AVAILABLE = "Доступен"
    SOLD = "Продан"
    USED = "Использован"
