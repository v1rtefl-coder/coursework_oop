from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class Aeroplane:
    """Класс для представления информации о самолете"""

    callsign: str
    origin_country: str
    velocity: Optional[float]  # скорость в м/с
    altitude: Optional[float]  # высота в метрах
    icao24: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    on_ground: Optional[bool] = None
    vertical_rate: Optional[float] = None

    def __post_init__(self):
        """Валидация данных после инициализации"""
        self._validate_data()

    def _validate_data(self):
        """Валидация атрибутов"""
        if not self.callsign or not isinstance(self.callsign, str):
            raise ValueError("Позывной должен быть непустой строкой")

        if not self.origin_country or not isinstance(self.origin_country, str):
            raise ValueError("Страна регистрации должна быть непустой строкой")

        if self.velocity is not None:
            if not isinstance(self.velocity, (int, float)) or self.velocity < 0:
                raise ValueError("Скорость должна быть неотрицательным числом")

        if self.altitude is not None:
            if not isinstance(self.altitude, (int, float)):
                raise ValueError("Высота должна быть числом")

    def __eq__(self, other) -> bool:
        """Сравнение самолетов по позывному"""
        if not isinstance(other, Aeroplane):
            return False
        return self.callsign == other.callsign

    def __lt__(self, other) -> bool:
        """Сравнение по скорости (для сортировки)"""
        if not isinstance(other, Aeroplane):
            return NotImplemented
        if self.velocity is None and other.velocity is None:
            return False
        if self.velocity is None:
            return True
        if other.velocity is None:
            return False
        return self.velocity < other.velocity

    def compare_by_speed(self, other: 'Aeroplane') -> int:
        """
        Сравнение самолетов по скорости
        Returns:
            1 если текущий быстрее, -1 если медленнее, 0 если равны
        """
        if self.velocity is None and other.velocity is None:
            return 0
        if self.velocity is None:
            return -1
        if other.velocity is None:
            return 1
        if self.velocity > other.velocity:
            return 1
        elif self.velocity < other.velocity:
            return -1
        return 0

    def compare_by_altitude(self, other: 'Aeroplane') -> int:
        """
        Сравнение самолетов по высоте
        Returns:
            1 если текущий выше, -1 если ниже, 0 если равны
        """
        if self.altitude is None and other.altitude is None:
            return 0
        if self.altitude is None:
            return -1
        if other.altitude is None:
            return 1
        if self.altitude > other.altitude:
            return 1
        elif self.altitude < other.altitude:
            return -1
        return 0

    @classmethod
    def cast_to_object_list(cls, aeroplanes_data: List[Dict[str, Any]]) -> List['Aeroplane']:
        """
        Преобразование списка словарей в список объектов Aeroplane
        """
        aeroplanes = []
        for data in aeroplanes_data:
            try:
                aeroplane = cls(
                    callsign=data.get('callsign', 'N/A'),
                    origin_country=data.get('origin_country', 'Unknown'),
                    velocity=data.get('velocity'),
                    altitude=data.get('baro_altitude') or data.get('geo_altitude'),
                    icao24=data.get('icao24'),
                    latitude=data.get('latitude'),
                    longitude=data.get('longitude'),
                    on_ground=data.get('on_ground'),
                    vertical_rate=data.get('vertical_rate')
                )
                aeroplanes.append(aeroplane)
            except (ValueError, TypeError) as e:
                print(f"Ошибка при создании объекта самолета: {e}")
                continue
        return aeroplanes

    def to_dict(self) -> Dict[str, Any]:
        """Преобразование объекта в словарь для сохранения"""
        return {
            'icao24': self.icao24,
            'callsign': self.callsign,
            'origin_country': self.origin_country,
            'velocity': self.velocity,
            'altitude': self.altitude,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'on_ground': self.on_ground,
            'vertical_rate': self.vertical_rate
        }

    def __str__(self) -> str:
        """Человекочитаемое представление самолета"""
        speed_str = f"{self.velocity * 3.6:.1f} км/ч" if self.velocity is not None else "N/A"
        alt_str = f"{self.altitude:.0f} м" if self.altitude is not None else "N/A"
        return (f"{self.callsign} ({self.origin_country}) - "
                f"Скорость: {speed_str}, Высота: {alt_str}")