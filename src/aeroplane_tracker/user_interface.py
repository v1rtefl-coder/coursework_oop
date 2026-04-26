from typing import List, Optional
from .aeroplane import Aeroplane
from .api_client import AeroplanesAPI
from .json_storage import JSONSaver


def get_top_aeroplanes(aeroplanes: List[Aeroplane], top_n: int) -> List[Aeroplane]:
    """
    Получение топ N самолетов по высоте полета
    """
    if not aeroplanes:
        return []

    # Сортировка по высоте (Descending)
    sorted_aeroplanes = sorted(
        [a for a in aeroplanes if a.altitude is not None],
        key=lambda x: x.altitude,
        reverse=True
    )

    return sorted_aeroplanes[:top_n]


def filter_aeroplanes_by_country(aeroplanes: List[Aeroplane], countries: List[str]) -> List[Aeroplane]:
    """
    Фильтрация самолетов по стране регистрации
    """
    if not countries:
        return aeroplanes

    filtered = []
    for aeroplane in aeroplanes:
        for country in countries:
            if country.lower() in aeroplane.origin_country.lower():
                filtered.append(aeroplane)
                break
    return filtered


def filter_aeroplanes_by_altitude_range(aeroplanes: List[Aeroplane], min_alt: Optional[float],
                                        max_alt: Optional[float]) -> List[Aeroplane]:
    """
    Фильтрация самолетов по диапазону высот
    """
    filtered = []
    for aeroplane in aeroplanes:
        if aeroplane.altitude is None:
            continue
        if min_alt is not None and aeroplane.altitude < min_alt:
            continue
        if max_alt is not None and aeroplane.altitude > max_alt:
            continue
        filtered.append(aeroplane)
    return filtered


def print_aeroplanes(aeroplanes: List[Aeroplane], title: str = "Самолеты"):
    """
    Вывод информации о самолетах в консоль
    """
    if not aeroplanes:
        print(f"\n{title}: Не найдено")
        return

    print(f"\n{title} (найдено: {len(aeroplanes)}):")
    print("-" * 70)
    for i, aeroplane in enumerate(aeroplanes, 1):
        print(f"{i}. {aeroplane}")
    print("-" * 70)


def user_interaction():
    """
    Функция для взаимодействия с пользователем через консоль
    """
    print("=" * 70)
    print("Система отслеживания самолетов")
    print("=" * 70)

    # Инициализация компонентов
    api = AeroplanesAPI()
    storage = JSONSaver()
    current_aeroplanes = []

    while True:
        print("\nМеню:")
        print("1. Получить информацию о самолетах в стране")
        print("2. Показать топ N самолетов по высоте")
        print("3. Фильтрация по стране регистрации")
        print("4. Фильтрация по диапазону высот")
        print("5. Сохранить текущие данные в файл")
        print("6. Загрузить данные из файла")
        print("7. Показать все сохраненные самолеты")
        print("8. Очистить сохраненные данные")
        print("0. Выход")

        choice = input("\nВыберите действие: ").strip()

        if choice == "0":
            print("До свидания!")
            break

        elif choice == "1":
            country = input("Введите название страны (например, Russia, Spain, USA): ").strip()
            if not country:
                print("Название страны не может быть пустым")
                continue

            print(f"\nПолучение данных о самолетах в {country}...")
            aeroplanes_data = api.get_aeroplanes_by_country(country)

            if not aeroplanes_data:
                print(f"Не удалось получить данные для страны {country}")
                continue

            current_aeroplanes = Aeroplane.cast_to_object_list(aeroplanes_data)
            print_aeroplanes(current_aeroplanes, f"Самолеты в {country}")

        elif choice == "2":
            if not current_aeroplanes:
                print("Сначала получите данные о самолетах (выберите пункт 1)")
                continue

            try:
                top_n = int(input("Введите количество самолетов для топа: "))
                if top_n <= 0:
                    print("Количество должно быть положительным числом")
                    continue
            except ValueError:
                print("Пожалуйста, введите корректное число")
                continue

            top_aeroplanes = get_top_aeroplanes(current_aeroplanes, top_n)
            print_aeroplanes(top_aeroplanes, f"Топ {top_n} самолетов по высоте")

        elif choice == "3":
            if not current_aeroplanes:
                print("Сначала получите данные о самолетах (выберите пункт 1)")
                continue

            countries_input = input("Введите названия стран для фильтрации (через пробел): ").strip()
            if not countries_input:
                print("Фильтр не применен")
                continue

            countries = countries_input.split()
            filtered = filter_aeroplanes_by_country(current_aeroplanes, countries)
            print_aeroplanes(filtered, f"Самолеты из стран: {', '.join(countries)}")

        elif choice == "4":
            if not current_aeroplanes:
                print("Сначала получите данные о самолетах (выберите пункт 1)")
                continue

            range_input = input("Введите диапазон высот (например, 0-10000 или 5000-): ").strip()

            min_alt = None
            max_alt = None

            try:
                if '-' in range_input:
                    parts = range_input.split('-')
                    if parts[0] and parts[0].strip():
                        min_alt = float(parts[0].strip())
                    if len(parts) > 1 and parts[1] and parts[1].strip():
                        max_alt = float(parts[1].strip())
                else:
                    print("Неверный формат диапазона")
                    continue
            except ValueError:
                print("Пожалуйста, введите корректные числа")
                continue

            filtered = filter_aeroplanes_by_altitude_range(current_aeroplanes, min_alt, max_alt)
            range_str = f"{min_alt if min_alt is not None else 0} - {max_alt if max_alt is not None else '∞'}"
            print_aeroplanes(filtered, f"Самолеты на высоте {range_str} м")

        elif choice == "5":
            if not current_aeroplanes:
                print("Нет данных для сохранения")
                continue

            saved_count = 0
            for aeroplane in current_aeroplanes:
                if storage.add_aeroplane(aeroplane):
                    saved_count += 1

            print(f"Сохранено {saved_count} из {len(current_aeroplanes)} самолетов")

        elif choice == "6":
            loaded = storage.get_all_aeroplanes()
            if loaded:
                current_aeroplanes = loaded
                print_aeroplanes(loaded, "Загруженные самолеты")
            else:
                print("Нет сохраненных данных")

        elif choice == "7":
            saved = storage.get_all_aeroplanes()
            if saved:
                print_aeroplanes(saved, "Все сохраненные самолеты")
            else:
                print("Нет сохраненных данных")

        elif choice == "8":
            confirm = input("Вы уверены, что хотите очистить все сохраненные данные? (y/n): ")
            if confirm.lower() == 'y':
                if storage.clear_all():
                    print("Все данные успешно очищены")
                    if current_aeroplanes:
                        current_aeroplanes = []
                else:
                    print("Ошибка при очистке данных")
            else:
                print("Очистка отменена")

        else:
            print("Неверный выбор. Пожалуйста, выберите пункт от 0 до 8")
