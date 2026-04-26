import sys
import os

# Добавляем src в путь поиска модулей
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from aeroplane_tracker.user_interface import user_interaction

def main():
    """Главная функция запуска"""
    print("Запуск системы отслеживания самолетов...")
    print("Версия 1.0.0")
    print()
    user_interaction()

if __name__ == "__main__":
    main()
