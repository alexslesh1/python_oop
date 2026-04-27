"""
Абстрактные базовые классы (интерфейсы) для лабораторной работы №4
"""

from abc import ABC, abstractmethod


class IPrintable(ABC):
    """Интерфейс для получения строкового представления объекта"""
    
    @abstractmethod
    def get_info(self) -> str:
        """Вернуть краткую информацию об объекте"""
        pass


class IServiceable(ABC):
    """Интерфейс для обслуживаемых объектов"""
    
    @abstractmethod
    def needs_service(self) -> bool:
        """Проверить, нуждается ли объект в обслуживании"""
        pass
    
    @abstractmethod
    def service(self) -> str:
        """Выполнить обслуживание и вернуть отчет"""
        pass


class IComparable(ABC):
    """Интерфейс для сравнения объектов"""
    
    @abstractmethod
    def compare_to(self, other) -> int:
        """
        Сравнить текущий объект с другим
        
        Возвращает:
        -1 если self < other
        0  если self == other
        1  если self > other
        """
        pass
