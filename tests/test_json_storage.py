import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
import tempfile
from src.aeroplane_tracker.aeroplane import Aeroplane
from src.aeroplane_tracker.json_storage import JSONSaver


class TestJSONSaver(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл для тестов
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.storage = JSONSaver(self.temp_file.name)
        self.aeroplane1 = Aeroplane("TEST1", "USA", 300, 10000)
        self.aeroplane2 = Aeroplane("TEST2", "Russia", 250, 8000)
        self.aeroplane3 = Aeroplane("TEST3", "Germany", 280, 12000)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_aeroplane(self):
        """Тест добавления самолета"""
        result = self.storage.add_aeroplane(self.aeroplane1)
        self.assertTrue(result)

        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].callsign, "TEST1")

    def test_add_multiple_aeroplanes(self):
        """Тест добавления нескольких самолетов"""
        self.storage.add_aeroplane(self.aeroplane1)
        self.storage.add_aeroplane(self.aeroplane2)
        self.storage.add_aeroplane(self.aeroplane3)

        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 3)

    def test_delete_aeroplane(self):
        """Тест удаления самолета"""
        self.storage.add_aeroplane(self.aeroplane1)
        self.storage.add_aeroplane(self.aeroplane2)

        result = self.storage.delete_aeroplane(self.aeroplane1)
        self.assertTrue(result)

        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].callsign, "TEST2")

    def test_get_aeroplanes_by_criteria(self):
        """Тест получения самолетов по критериям"""
        self.storage.add_aeroplane(self.aeroplane1)
        self.storage.add_aeroplane(self.aeroplane2)
        self.storage.add_aeroplane(self.aeroplane3)

        # Фильтрация по стране
        result = self.storage.get_aeroplanes(origin_country="USA")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "TEST1")

        # Фильтрация по минимальной скорости
        result = self.storage.get_aeroplanes(min_speed=280)
        self.assertEqual(len(result), 2)  # TEST1 (300) и TEST3 (280)

        # Фильтрация по диапазону высот
        result = self.storage.get_aeroplanes(min_altitude=9000, max_altitude=11000)
        # TEST1 (10000) подходит, TEST2 (8000) нет, TEST3 (12000) нет
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].callsign, "TEST1")

    def test_update_aeroplane(self):
        """Тест обновления существующего самолета"""
        self.storage.add_aeroplane(self.aeroplane1)

        # Обновляем скорость и высоту
        updated = Aeroplane("TEST1", "USA", 350, 15000)
        self.storage.add_aeroplane(updated)

        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].velocity, 350)
        self.assertEqual(loaded[0].altitude, 15000)

    def test_clear_all(self):
        """Тест очистки хранилища"""
        self.storage.add_aeroplane(self.aeroplane1)
        self.storage.add_aeroplane(self.aeroplane2)

        self.storage.clear_all()
        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 0)

    def test_get_all_aeroplanes_empty(self):
        """Тест получения из пустого хранилища"""
        loaded = self.storage.get_all_aeroplanes()
        self.assertEqual(len(loaded), 0)


if __name__ == '__main__':
    unittest.main()
