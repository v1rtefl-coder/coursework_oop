import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch
from src.aeroplane_tracker.api_client import AeroplanesAPI


class TestApiClient(unittest.TestCase):

    def setUp(self):
        self.api = AeroplanesAPI()

    @patch('requests.Session.get')
    def test_get_country_coordinates_success(self, mock_get):
        """Тест успешного получения координат страны"""
        mock_response = Mock()
        mock_response.json.return_value = [
            {
                'display_name': 'Russia',
                'boundingbox': ['41.0', '82.0', '19.0', '180.0'],
                'lat': '60.0',
                'lon': '100.0'
            }
        ]
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.api.get_country_coordinates('Russia')

        self.assertIsNotNone(result)
        self.assertEqual(result['name'], 'Russia')
        self.assertEqual(len(result['boundingbox']), 4)

    @patch('requests.Session.get')
    def test_get_country_coordinates_not_found(self, mock_get):
        """Тест получения координат несуществующей страны"""
        mock_response = Mock()
        mock_response.json.return_value = []
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = self.api.get_country_coordinates('InvalidCountry123')

        self.assertIsNone(result)

    @patch('requests.Session.get')
    def test_get_country_coordinates_request_error(self, mock_get):
        """Тест ошибки запроса при получении координат"""
        # Симулируем ошибку запроса
        mock_get.side_effect = Exception("Network error")

        result = self.api.get_country_coordinates('Russia')

        # Функция должна вернуть None при ошибке
        self.assertIsNone(result)

    @patch('requests.Session.get')
    def test_get_aeroplanes_in_area_success(self, mock_get):
        """Тест успешного получения самолетов в области"""
        mock_response = Mock()
        mock_response.json.return_value = {
            'states': [
                ['abc123', 'UAL123', 'USA', 12345, 12346, 50.0, 30.0, 10000, False, 250.0, 90.0, 5.0, None, 10200]
            ]
        }
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        bounds = [40.0, 60.0, 20.0, 40.0]
        result = self.api.get_aeroplanes_in_area(bounds)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['callsign'], 'UAL123')
        self.assertEqual(result[0]['origin_country'], 'USA')

    @patch('requests.Session.get')
    def test_get_aeroplanes_in_area_empty(self, mock_get):
        """Тест получения пустого списка самолетов"""
        mock_response = Mock()
        # API возвращает {'states': None} когда нет данных
        mock_response.json.return_value = {'states': None}
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        bounds = [40.0, 60.0, 20.0, 40.0]
        result = self.api.get_aeroplanes_in_area(bounds)

        # Функция должна обработать None и вернуть пустой список
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch('requests.Session.get')
    def test_get_aeroplanes_in_area_error(self, mock_get):
        """Тест ошибки при получении самолетов"""
        # Симулируем ошибку сети
        mock_get.side_effect = Exception("Connection error")

        bounds = [40.0, 60.0, 20.0, 40.0]
        result = self.api.get_aeroplanes_in_area(bounds)

        # При ошибке функция должна вернуть пустой список
        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)

    @patch.object(AeroplanesAPI, 'get_country_coordinates')
    @patch.object(AeroplanesAPI, 'get_aeroplanes_in_area')
    def test_get_aeroplanes_by_country_success(self, mock_get_area, mock_get_coords):
        """Тест успешного получения самолетов по стране"""
        mock_get_coords.return_value = {
            'name': 'Spain',
            'boundingbox': ['36.0', '43.8', '-9.3', '3.3']
        }
        mock_get_area.return_value = [{'callsign': 'IBE123', 'origin_country': 'Spain'}]

        result = self.api.get_aeroplanes_by_country('Spain')

        self.assertEqual(len(result), 1)
        mock_get_coords.assert_called_once_with('Spain')

    @patch.object(AeroplanesAPI, 'get_country_coordinates')
    def test_get_aeroplanes_by_country_no_coords(self, mock_get_coords):
        """Тест получения самолетов для страны без координат"""
        mock_get_coords.return_value = None

        result = self.api.get_aeroplanes_by_country('InvalidCountry')

        self.assertEqual(result, [])
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()
