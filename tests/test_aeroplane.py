import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from src.aeroplane_tracker.aeroplane import Aeroplane


class TestAeroplane(unittest.TestCase):

    def setUp(self):
        self.aeroplane1 = Aeroplane("UAL1621", "United States", 268.79, 10203.18)
        self.aeroplane2 = Aeroplane("DLH431", "Germany", 250.50, 9500.00)
        self.aeroplane3 = Aeroplane("AFR123", "France", 300.00, 11000.00)

    def test_aeroplane_creation(self):
        """Тест создания самолета"""
        self.assertEqual(self.aeroplane1.callsign, "UAL1621")
        self.assertEqual(self.aeroplane1.origin_country, "United States")
        self.assertEqual(self.aeroplane1.velocity, 268.79)
        self.assertEqual(self.aeroplane1.altitude, 10203.18)

    def test_invalid_aeroplane(self):
        """Тест валидации данных"""
        with self.assertRaises(ValueError):
            Aeroplane("", "USA", 100, 1000)

        with self.assertRaises(ValueError):
            Aeroplane("UAL123", "", 100, 1000)

        with self.assertRaises(ValueError):
            Aeroplane("UAL123", "USA", -100, 1000)

    def test_compare_by_speed(self):
        """Тест сравнения по скорости"""
        self.assertEqual(self.aeroplane1.compare_by_speed(self.aeroplane2), 1)
        self.assertEqual(self.aeroplane2.compare_by_speed(self.aeroplane1), -1)

        aeroplane_same = Aeroplane("TEST", "Test", 268.79, 10000)
        self.assertEqual(self.aeroplane1.compare_by_speed(aeroplane_same), 0)

    def test_compare_by_altitude(self):
        """Тест сравнения по высоте"""
        self.assertEqual(self.aeroplane1.compare_by_altitude(self.aeroplane2), 1)
        self.assertEqual(self.aeroplane2.compare_by_altitude(self.aeroplane1), -1)

    def test_cast_to_object_list(self):
        """Тест преобразования списка словарей"""
        data = [
            {'callsign': 'TEST1', 'origin_country': 'USA', 'velocity': 100, 'altitude': 1000},
            {'callsign': 'TEST2', 'origin_country': 'UK', 'velocity': 200, 'altitude': 2000}
        ]

        aeroplanes = Aeroplane.cast_to_object_list(data)
        self.assertEqual(len(aeroplanes), 2)
        self.assertEqual(aeroplanes[0].callsign, 'TEST1')
        self.assertEqual(aeroplanes[1].callsign, 'TEST2')

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        aeroplane_dict = self.aeroplane1.to_dict()
        self.assertEqual(aeroplane_dict['callsign'], 'UAL1621')
        self.assertEqual(aeroplane_dict['origin_country'], 'United States')
        self.assertEqual(aeroplane_dict['velocity'], 268.79)
        self.assertEqual(aeroplane_dict['altitude'], 10203.18)

    def test_str_representation(self):
        """Тест строкового представления"""
        str_repr = str(self.aeroplane1)
        self.assertIn("UAL1621", str_repr)
        self.assertIn("United States", str_repr)


if __name__ == '__main__':
    unittest.main()
