"""
Скрипт для запуска всех тестов
"""

import sys
import os
import pytest


def main():
    """Запуск тестов"""
    # Добавляем src в путь поиска модулей
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

    # Запускаем pytest
    exit_code = pytest.main([
        "tests/",
        "-v",
        "--cov=src/aeroplane_tracker",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--tb=short"
    ])

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
