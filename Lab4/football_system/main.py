#!/usr/bin/env python3
"""
Главный модуль системы управления футбольным клубом
Демонстрация работы всех паттернов проектирования
"""

import os
import sys

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.abspath('.'))

from football import (
    PlayerFactory,
    CaptainDecorator,
    InjuredDecorator,
    YoungTalentDecorator,
    FootballMatch,
    Commentator,
    StatisticsTracker,
    MediaReporter,
    PlayerPosition,
    MatchEvent
)


def demonstrate_creational_pattern():
    """Демонстрация порождающего паттерна (Фабричный метод)"""
    print("🎯 === ДЕМОНСТРАЦИЯ ПОРОЖДАЮЩЕГО ПАТТЕРНА ===")
    print("Создание игроков разных позиций через фабрику:\n")

    # Создаем игроков разных амплуа через фабрику
    players = [
        PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Игорь Акинфеев", 1),
        PlayerFactory.create_player(PlayerPosition.DEFENDER, "Марио Фернандес", 2),
        PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Александр Головин", 17),
        PlayerFactory.create_player(PlayerPosition.FORWARD, "Артем Дзюба", 22)
    ]

    for player in players:
        print(f"✅ Создан: {player}")
        print(f"   Навыки: {', '.join(player.get_specific_skills())}")
        print(f"   Тренировка: {player.train()}")
    print()


def demonstrate_structural_pattern():
    """Демонстрация структурного паттерна (Декоратор)"""
    print("🎨 === ДЕМОНСТРАЦИЯ СТРУКТУРНОГО ПАТТЕРНА ===")
    print("Применение декораторов к игрокам:\n")

    # Создаем базовых игроков
    base_players = [
        PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Денис Черышев", 6),
        PlayerFactory.create_player(PlayerPosition.DEFENDER, "Георгий Джикия", 14),
        PlayerFactory.create_player(PlayerPosition.FORWARD, "Александр Соболев", 11)
    ]

    # Применяем декораторы
    captain = CaptainDecorator(base_players[0])
    injured_player = InjuredDecorator(base_players[1], "растяжение связок", 10)
    young_talent = YoungTalentDecorator(base_players[2], 0.9, 21)

    decorated_players = [captain, injured_player, young_talent]

    for player in decorated_players:
        print(f"🎭 {player}")
        print(f"   Навыки: {', '.join(player.get_specific_skills())}")
        print(f"   Тренировка: {player.train()}")

        # Специфические методы декораторов
        if hasattr(player, 'motivate_team'):
            print(f"   Действие: {player.motivate_team()}")
        if hasattr(player, 'recover'):
            print(f"   Реабилитация: {player.recover()}")
    print()


def demonstrate_behavioral_pattern():
    """Демонстрация поведенческого паттерна (Наблюдатель)"""
    print("👀 === ДЕМОНСТРАЦИЯ ПОВЕДЕНЧЕСКОГО ПАТТЕРНА ===")
    print("Симуляция матча с системой наблюдения:\n")

    # Создаем матч и наблюдателей
    match = FootballMatch("Россия", "Бразилия", "Лужники")
    commentator = Commentator("Георгий Черданцев")
    stats_tracker = StatisticsTracker()
    media_reporter = MediaReporter("Спорт-Экспресс")

    # Подключаем наблюдателей
    match.attach(commentator)
    match.attach(stats_tracker)
    match.attach(media_reporter)

    print("🏟️  Начинается матч Россия vs Бразилия:")
    print("=" * 60)

    # События матча
    match.start_match()
    match.goal("home", "Артем Дзюба", 23, "Александр Головин")
    match.yellow_card("Неймар", 45, "симуляция")
    match.substitution("Ришарлисон", "Габриэл Жезус", 67)
    match.goal("away", "Габриэл Жезус", 72)
    match.yellow_card("Марио Фернандес", 85, "задержка атаки")
    match.goal("home", "Александр Головин", 89)
    match.finish_match()

    print("=" * 60)

    # Выводим статистику
    stats = stats_tracker.get_match_statistics()
    print("\n📊 Статистика матча:")
    print(f"   Всего голов: {stats['total_goals']}")
    print(f"   Голы России: {stats['home_goals']}")
    print(f"   Голы Бразилии: {stats['away_goals']}")
    print(f"   Желтых карточек: {stats['yellow_cards']}")
    print(f"   Авторы голов: {', '.join(stats['goal_scorers'])}")
    print(f"   Победитель: {match.get_winner()}")
    print()


def demonstrate_complete_scenario():
    """Демонстрация полного сценария работы системы"""
    print("🚀 === ПОЛНЫЙ СЦЕНАРИЙ РАБОТЫ СИСТЕМЫ ===")
    print("Создание команды, подготовка к матчу и проведение игры:\n")

    # 1. Создаем команду через фабрику
    print("1. 📋 ФОРМИРОВАНИЕ СОСТАВА:")
    team = PlayerFactory.create_russian_national_team()
    for player in team:
        print(f"   • {player}")

    # 2. Применяем декораторы
    print("\n2. 🎭 ПОДГОТОВКА ИГРОКОВ:")
    captain = CaptainDecorator(team[3])  # Черышев - капитан
    injured_player = InjuredDecorator(team[1], "ушиб бедра", 5)  # Фернандес травмирован
    talent = YoungTalentDecorator(team[4], 0.95, 20)  # Головин - молодой талант

    print(f"   • {captain}")
    print(f"   • {injured_player}")
    print(f"   • {talent}")

    # 3. Проводим матч
    print("\n3. ⚽ ПРОВЕДЕНИЕ МАТЧА:")
    match = FootballMatch("Россия", "Германия", "Вельтинс-Арена")
    commentator = Commentator("Владимир Стогниенко")
    stats = StatisticsTracker()

    match.attach(commentator)
    match.attach(stats)

    match.start_match()
    match.goal("home", "Артем Дзюба", 34)
    match.goal("away", "Томас Мюллер", 67)
    match.goal("home", "Александр Головин", 88)
    match.finish_match()

    print(f"\n   🏆 Результат: Россия побеждает {match.get_winner()}!")


def run_tests():
    """Запуск всех тестов"""
    print("\n🧪 === ЗАПУСК ТЕСТОВ ===")
    import unittest
    import sys
    import os

    # Находим и запускаем все тесты
    loader = unittest.TestLoader()
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    suite = loader.discover(start_dir, pattern='test_*.py')

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("🏈 СИСТЕМА УПРАВЛЕНИЯ ФУТБОЛЬНЫМ КЛУБОМ")
    print("Реализация паттернов: Фабрика, Декоратор, Наблюдатель\n")

    # Демонстрация паттернов
    demonstrate_creational_pattern()
    demonstrate_structural_pattern()
    demonstrate_behavioral_pattern()
    demonstrate_complete_scenario()

    # Запуск тестов (опционально)
    run_tests_option = input("\nЗапустить тесты? (y/n): ").lower().strip()
    if run_tests_option == 'y':
        success = run_tests()
        if success:
            print("\n🎉 Все демонстрации и тесты завершены успешно!")
        else:
            print("\n❌ Некоторые тесты не прошли")
    else:
        print("\n✨ Демонстрация завершена!")