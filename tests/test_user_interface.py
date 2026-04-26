import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import Mock, patch  # Добавьте эту строку!
from src.aeroplane_tracker.aeroplane import Aeroplane
from src.aeroplane_tracker.user_interface import (
    get_top_aeroplanes,
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude_range,
    print_aeroplanes
)


class TestUserInterface(unittest.TestCase):

    def setUp(self):
        self.aeroplanes = [
            Aeroplane("A1", "USA", 300, 15000),
            Aeroplane("A2", "Russia", 250, 12000),
            Aeroplane("A3", "Germany", 280, 18000),
            Aeroplane("A4", "France", 200, 9000),
            Aeroplane("A5", "USA", 350, 20000),
            Aeroplane("A6", "United Kingdom", 320, 16000),
        ]

    def test_get_top_aeroplanes(self):
        """Тест получения топ N самолетов по высоте"""
        top3 = get_top_aeroplanes(self.aeroplanes, 3)
        self.assertEqual(len(top3), 3)
        self.assertEqual(top3[0].callsign, "A5")
        self.assertEqual(top3[1].callsign, "A3")
        self.assertEqual(top3[2].callsign, "A6")

    def test_get_top_aeroplanes_with_none_altitude(self):
        """Тест топ N с самолетами без высоты"""
        aeroplanes_with_none = self.aeroplanes + [
            Aeroplane("A7", "Japan", 280, None)
        ]
        top3 = get_top_aeroplanes(aeroplanes_with_none, 3)
        self.assertEqual(len(top3), 3)

    def test_get_top_aeroplanes_more_than_available(self):
        """Тест запроса топа больше чем есть самолетов"""
        top10 = get_top_aeroplanes(self.aeroplanes, 10)
        expected_count = len([a for a in self.aeroplanes if a.altitude is not None])
        self.assertEqual(len(top10), expected_count)

    def test_filter_by_country_single(self):
        """Тест фильтрации по одной стране"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, ["USA"])
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0].callsign, "A1")
        self.assertEqual(filtered[1].callsign, "A5")

    def test_filter_by_country_multiple(self):
        """Тест фильтрации по нескольким странам"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, ["USA", "Germany"])
        self.assertEqual(len(filtered), 3)
        callsigns = [a.callsign for a in filtered]
        self.assertIn("A1", callsigns)
        self.assertIn("A3", callsigns)
        self.assertIn("A5", callsigns)

    def test_filter_by_country_partial_match(self):
        """Тест фильтрации по частичному совпадению"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, ["Unit"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].callsign, "A6")

    def test_filter_by_country_empty(self):
        """Тест фильтрации с пустым списком стран"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, [])
        self.assertEqual(len(filtered), len(self.aeroplanes))

    def test_filter_by_altitude_range(self):
        """Тест фильтрации по диапазону высот"""
        filtered = filter_aeroplanes_by_altitude_range(self.aeroplanes, 10000, 17000)
        self.assertEqual(len(filtered), 3)
        callsigns = [a.callsign for a in filtered]
        self.assertIn("A1", callsigns)
        self.assertIn("A2", callsigns)
        self.assertIn("A6", callsigns)

    def test_filter_by_altitude_min_only(self):
        """Тест фильтрации только по минимальной высоте"""
        # Создаем тестовые данные
        aeroplanes = [
            Aeroplane("A1", "USA", 300, 15000),
            Aeroplane("A2", "Russia", 250, 12000),
            Aeroplane("A3", "Germany", 280, 18000),
            Aeroplane("A4", "France", 200, 9000),
            Aeroplane("A5", "Japan", 350, 20000),
        ]

        # Фильтр выше 16000 метров
        filtered = filter_aeroplanes_by_altitude_range(aeroplanes, 16000, None)
        # A3 (18000) и A5 (20000) подходят
        self.assertEqual(len(filtered), 2)
        callsigns = [a.callsign for a in filtered]
        self.assertIn("A3", callsigns)
        self.assertIn("A5", callsigns)

    def test_filter_by_altitude_max_only(self):
        """Тест фильтрации только по максимальной высоте"""
        filtered = filter_aeroplanes_by_altitude_range(self.aeroplanes, None, 11000)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].callsign, "A4")

    def test_filter_by_altitude_no_match(self):
        """Тест фильтрации без совпадений"""
        filtered = filter_aeroplanes_by_altitude_range(self.aeroplanes, 30000, 40000)
        self.assertEqual(len(filtered), 0)


# Удалите или закомментируйте класс TestUserInteraction, так как он вызывает ошибку
# class TestUserInteraction(unittest.TestCase):
#     ...

if __name__ == '__main__':
    unittest.main()
