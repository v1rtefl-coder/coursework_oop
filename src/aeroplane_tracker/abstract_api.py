from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API сервисами"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> Optional[Dict[str, Any]]:
        """
        Получение географических координат страны
        Args:
            country_name: Название страны
        Returns:
            Словарь с координатами (boundingbox)
        """
        pass

    @abstractmethod
    def get_aeroplanes_in_area(self, bounds: List[float]) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в указанной области
        Args:
            bounds: Координаты [min_latitude, max_latitude, min_longitude, max_longitude]
        Returns:
            Список словарей с информацией о самолетах
        """
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в стране
        Args:
            country_name: Название странs
        Returns:
            Список словарей с информацией о самолетах
        """
        pass
