import requests
from typing import List, Dict, Any, Optional
from .abstract_api import AbstractAPI


class AeroplanesAPI(AbstractAPI):
    """Класс для работы с API nominatim и opensky-network"""

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'AeroplaneTracker/1.0'
        })

    def get_country_coordinates(self, country_name: str) -> Optional[Dict[str, Any]]:
        """
        Получение координат страны через Nominatim API
        """
        try:
            params = {
                'q': country_name,
                'format': 'json',
                'limit': 1,
                'addressdetails': 0
            }

            response = self.session.get(self.nominatim_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            if not data:
                print(f"Страна '{country_name}' не найдена")
                return None

            result = data[0]
            return {
                'name': result.get('display_name', country_name),
                'boundingbox': result.get('boundingbox', []),
                'lat': result.get('lat'),
                'lon': result.get('lon')
            }

        except requests.RequestException as e:
            print(f"Ошибка при получении координат: {e}")
            return None
        except (KeyError, IndexError, ValueError) as e:
            print(f"Ошибка обработки данных: {e}")
            return None
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return None

    def get_aeroplanes_in_area(self, bounds: List[float]) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в области через OpenSky API
        bounds: [min_latitude, max_latitude, min_longitude, max_longitude]
        """
        try:
            params = {
                'lamin': bounds[0],  # min latitude
                'lamax': bounds[1],  # max latitude
                'lomin': bounds[2],  # min longitude
                'lomax': bounds[3]  # max longitude
            }

            response = self.session.get(self.opensky_url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()
            states = data.get('states')

            # Обработка случая, когда states = None
            if states is None:
                return []

            # Преобразуем данные в более удобный формат
            aeroplanes = []
            for state in states:
                if state and len(state) >= 10:
                    aeroplane_data = {
                        'icao24': state[0],
                        'callsign': state[1].strip() if state[1] else 'N/A',
                        'origin_country': state[2],
                        'time_position': state[3],
                        'last_contact': state[4],
                        'longitude': state[5],
                        'latitude': state[6],
                        'baro_altitude': state[7],
                        'on_ground': state[8],
                        'velocity': state[9],
                        'true_track': state[10],
                        'vertical_rate': state[11] if len(state) > 11 else None,
                        'geo_altitude': state[13] if len(state) > 13 else None
                    }
                    aeroplanes.append(aeroplane_data)

            return aeroplanes

        except requests.RequestException as e:
            print(f"Ошибка при получении данных о самолетах: {e}")
            return []
        except (KeyError, IndexError, ValueError) as e:
            print(f"Ошибка обработки данных: {e}")
            return []
        except Exception as e:
            print(f"Неожиданная ошибка: {e}")
            return []

    def get_aeroplanes_by_country(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолетах в указанной стране
        """
        try:
            coordinates = self.get_country_coordinates(country_name)
            if not coordinates or not coordinates.get('boundingbox'):
                print(f"Не удалось получить координаты для страны '{country_name}'")
                return []

            boundingbox = coordinates['boundingbox']
            if len(boundingbox) != 4:
                print(f"Некорректный формат boundingbox для страны '{country_name}'")
                return []

            # Преобразуем строки в числа
            try:
                bounds = [
                    float(boundingbox[0]),  # min latitude (south)
                    float(boundingbox[1]),  # max latitude (north)
                    float(boundingbox[2]),  # min longitude (west)
                    float(boundingbox[3])  # max longitude (east)
                ]
            except ValueError:
                print(f"Ошибка преобразования координат для страны '{country_name}'")
                return []

            return self.get_aeroplanes_in_area(bounds)
        except Exception as e:
            print(f"Ошибка при получении самолетов по стране: {e}")
            return []
