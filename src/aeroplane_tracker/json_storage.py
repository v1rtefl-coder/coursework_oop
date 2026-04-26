import json
import os
from typing import List, Optional, Dict, Any
from .abstract_storage import AbstractStorage
from .aeroplane import Aeroplane


class JSONSaver(AbstractStorage):
    """Класс для сохранения информации о самолетах в JSON файл"""

    def __init__(self, filename: str = "data/aeroplanes.json"):
        self.filename = filename
        # Создаем папку если нужно
        os.makedirs(os.path.dirname(filename), exist_ok=True)

    def _load_from_file(self) -> List[Dict[str, Any]]:
        """Загрузка данных из JSON файла"""
        if not os.path.exists(self.filename):
            return []

        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        except Exception as e:
            print(f"Ошибка при загрузке: {e}")
            return []

    def _save_to_file(self, data: List[Dict[str, Any]]) -> bool:
        """Сохранение данных в JSON файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении: {e}")
            return False

    def add_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Добавление самолета в JSON файл"""
        try:
            data = self._load_from_file()
            aeroplane_dict = aeroplane.to_dict()

            # Обновляем или добавляем
            for i, existing in enumerate(data):
                if existing.get('callsign') == aeroplane_dict['callsign']:
                    data[i] = aeroplane_dict
                    return self._save_to_file(data)

            data.append(aeroplane_dict)
            return self._save_to_file(data)
        except Exception as e:
            print(f"Ошибка при добавлении: {e}")
            return False

    def get_aeroplanes(self, **criteria) -> List[Aeroplane]:
        """Получение самолетов по критериям"""
        data = self._load_from_file()
        result = []

        for item in data:
            match = True
            for key, value in criteria.items():
                if key == 'origin_country' and item.get('origin_country', '').lower() != value.lower():
                    match = False
                    break
                elif key == 'min_speed' and (item.get('velocity') is None or item['velocity'] < value):
                    match = False
                    break
                elif key == 'max_speed' and (item.get('velocity') is None or item['velocity'] > value):
                    match = False
                    break
                elif key == 'min_altitude' and (item.get('altitude') is None or item['altitude'] < value):
                    match = False
                    break
                elif key == 'max_altitude' and (item.get('altitude') is None or item['altitude'] > value):
                    match = False
                    break

            if match:
                try:
                    result.append(Aeroplane(**item))
                except Exception:
                    continue

        return result

    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Удаление самолета из JSON файла"""
        data = self._load_from_file()
        original_len = len(data)
        data = [item for item in data if item.get('callsign') != aeroplane.callsign]

        if len(data) < original_len:
            return self._save_to_file(data)
        return False

    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """Получение всех самолетов"""
        data = self._load_from_file()
        result = []
        for item in data:
            try:
                result.append(Aeroplane(**item))
            except Exception:
                continue
        return result

    def clear_all(self) -> bool:
        """Очистка хранилища"""
        return self._save_to_file([])

