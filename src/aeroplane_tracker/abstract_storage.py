from abc import ABC, abstractmethod
from typing import List, Optional
from .aeroplane import Aeroplane


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем данных"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """
        Добавление информации о самолете в хранилище
        Returns:
            True если добавление успешно, False в противном случае
        """
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria) -> List[Aeroplane]:
        """
        Получение данных о самолетах по указанным критериям
        """
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """
        Удаление информации о самолете из хранилища
        Returns:
            True если удаление успешно, False в противном случае
        """
        pass

    @abstractmethod
    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """Получение всех самолетов из хранилища"""
        pass

    @abstractmethod
    def clear_all(self) -> bool:
        """Очистка хранилища"""
        pass
