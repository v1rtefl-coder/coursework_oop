import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.aeroplane_tracker.user_interface import (
    get_top_aeroplanes,
    filter_aeroplanes_by_country,
    filter_aeroplanes_by_altitude_range,
    print_aeroplanes
)
from src.aeroplane_tracker.aeroplane import Aeroplane


class TestUserInterfaceExtended(unittest.TestCase):

    def setUp(self):
        self.aeroplanes = [
            Aeroplane("TEST1", "USA", 300, 15000),
            Aeroplane("TEST2", "Russia", 250, 12000),
            Aeroplane("TEST3", "Germany", 280, 18000),
            Aeroplane("TEST4", "France", 200, 9000),
        ]

    def test_get_top_aeroplanes_empty(self):
        """Тест получения топа из пустого списка"""
        result = get_top_aeroplanes([], 5)
        self.assertEqual(result, [])

    def test_get_top_aeroplanes_zero_n(self):
        """Тест с нулевым топом"""
        result = get_top_aeroplanes(self.aeroplanes, 0)
        self.assertEqual(result, [])

    def test_filter_by_country_case_insensitive(self):
        """Тест регистронезависимой фильтрации"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, ["usa"])
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0].origin_country, "USA")

    def test_filter_by_country_no_match(self):
        """Тест фильтрации без совпадений"""
        filtered = filter_aeroplanes_by_country(self.aeroplanes, ["Japan"])
        self.assertEqual(len(filtered), 0)

    def test_filter_by_altitude_with_none(self):
        """Тест фильтрации с None значениями"""
        aeroplanes_with_none = self.aeroplanes + [Aeroplane("TEST5", "Japan", 300, None)]
        filtered = filter_aeroplanes_by_altitude_range(aeroplanes_with_none, 10000, 20000)
        # TEST1(15000), TEST2(12000), TEST3(18000) подходят
        self.assertEqual(len(filtered), 3)

    def test_print_aeroplanes_does_not_crash(self):
        """Тест что функция вывода не падает"""
        # Просто проверяем что функция не вызывает исключений
        aeroplanes = [Aeroplane("TEST", "USA", 300, 10000)]

        # Должно работать без ошибок
        print_aeroplanes(aeroplanes, "Тест")
        print_aeroplanes([], "Тест")

        # Если дошли сюда - тест пройден
        self.assertTrue(True)

    def test_filter_functions_with_empty_list(self):
        """Тест функций фильтрации с пустым списком"""
        empty_list = []

        result1 = filter_aeroplanes_by_country(empty_list, ["USA"])
        result2 = filter_aeroplanes_by_altitude_range(empty_list, 1000, 2000)
        result3 = get_top_aeroplanes(empty_list, 5)

        self.assertEqual(result1, [])
        self.assertEqual(result2, [])
        self.assertEqual(result3, [])


if __name__ == '__main__':
    unittest.main()
