import unittest
from unittest.mock import Mock, MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from football import PlayerFactory, FootballMatch, StatisticsTracker, PlayerPosition, MatchEvent


class TestWithMocks(unittest.TestCase):
    """
    Тесты с использованием Mock объектов
    """

    def test_match_with_mock_observers(self):
        """Тест матча с mock-наблюдателями"""
        # Создаем mock-наблюдателей
        mock_commentator = MagicMock()
        mock_stats_tracker = MagicMock()
        mock_media = MagicMock()

        match = FootballMatch("Динамо", "Краснодар")

        # Подключаем mock-объекты
        match.attach(mock_commentator)
        match.attach(mock_stats_tracker)
        match.attach(mock_media)

        # Симулируем события матча (5 событий)
        match.start_match()  # 1 событие
        match.goal("home", "Федор Смолов", 15)  # 2 событие
        match.yellow_card("Виктор Классон", 28)  # 3 событие
        match.substitution("Дмитрий Скопинцев", "Николай Комличенко", 65)  # 4 событие
        match.finish_match()  # 5 событие

        # Проверяем, что все наблюдатели получили уведомления (5 событий)
        expected_call_count = 5
        self.assertEqual(mock_commentator.update.call_count, expected_call_count)
        self.assertEqual(mock_stats_tracker.update.call_count, expected_call_count)
        self.assertEqual(mock_media.update.call_count, expected_call_count)

        # Проверяем конкретные вызовы для гола (второй вызов)
        goal_call_args = mock_commentator.update.call_args_list[1][0]
        self.assertEqual(goal_call_args[0], MatchEvent.GOAL)
        self.assertEqual(goal_call_args[1]["scorer"], "Федор Смолов")
        self.assertEqual(goal_call_args[1]["minute"], 15)

        # Проверяем первое событие (начало матча)
        start_call_args = mock_commentator.update.call_args_list[0][0]
        self.assertEqual(start_call_args[0], MatchEvent.MATCH_START)

    def test_match_without_start_and_finish(self):
        """Тест только игровых событий без начала и окончания"""
        mock_observer = MagicMock()

        match = FootballMatch("Торпедо", "Факел")
        match.attach(mock_observer)

        # Только игровые события (3 события)
        match.goal("home", "Иван Сергов", 23)
        match.yellow_card("Петр Иванов", 45)
        match.substitution("Сергей Петров", "Алексей Сидоров", 67)

        # Проверяем 3 события
        self.assertEqual(mock_observer.update.call_count, 3)

        # Проверяем типы событий
        call_args_list = mock_observer.update.call_args_list
        self.assertEqual(call_args_list[0][0][0], MatchEvent.GOAL)
        self.assertEqual(call_args_list[1][0][0], MatchEvent.YELLOW_CARD)
        self.assertEqual(call_args_list[2][0][0], MatchEvent.SUBSTITUTION)

    def test_player_factory_with_mock(self):
        """Тест фабрики игроков с mock callback"""
        # Создаем mock callback для проверки создания игроков
        mock_callback = Mock()

        # Тестируем создание разных типов игроков
        test_cases = [
            (PlayerPosition.GOALKEEPER, "Гильермо", 25),
            (PlayerPosition.DEFENDER, "Игорь Дедюх", 3),
            (PlayerPosition.MIDFIELDER, "Арсен Захарян", 10),
            (PlayerPosition.FORWARD, "Федор Чалов", 9)
        ]

        for player_type, name, number in test_cases:
            player = PlayerFactory.create_player(player_type, name, number)
            mock_callback(player)

        # Проверяем, что callback был вызван для каждого игрока
        self.assertEqual(mock_callback.call_count, len(test_cases))

        # Проверяем аргументы вызовов
        calls = mock_callback.call_args_list
        self.assertEqual(calls[0][0][0].name, "Гильермо")
        self.assertEqual(calls[1][0][0].name, "Игорь Дедюх")
        self.assertEqual(calls[2][0][0].name, "Арсен Захарян")
        self.assertEqual(calls[3][0][0].name, "Федор Чалов")

    @patch('football.creational.factory.PlayerFactory.create_player')
    def test_team_squad_with_patch(self, mock_create_player):
        """Тест создания состава команды с patch"""
        # Настраиваем mock
        mock_player = Mock()
        mock_player.name = "Test Player"
        mock_player.number = 99
        mock_player.get_position.return_value = "test_position"
        mock_player.get_specific_skills.return_value = ["skill1", "skill2"]
        mock_create_player.return_value = mock_player

        # Создаем состав
        squad = PlayerFactory.create_russian_national_team()

        # Проверяем, что фабрика вызывалась 6 раз
        self.assertEqual(mock_create_player.call_count, 6)

        # Проверяем, что состав содержит mock-игроков
        self.assertEqual(len(squad), 6)
        self.assertEqual(squad[0].name, "Test Player")

    def test_match_with_side_effects(self):
        """Тест с side_effects для mock объектов"""
        # Создаем mock с side_effect
        event_log = []

        def log_event(event_type, data):
            event_log.append((event_type, data))

        mock_observer = Mock()
        mock_observer.update.side_effect = log_event

        match = FootballMatch("Ростов", "Уфа")
        match.attach(mock_observer)

        # Генерируем события (без start/finish)
        match.goal("home", "Алексей Ионов", 33)
        match.yellow_card("Дмитрий Стоцкий", 71)

        # Проверяем через side_effect
        self.assertEqual(len(event_log), 2)
        self.assertEqual(event_log[0][0], MatchEvent.GOAL)
        self.assertEqual(event_log[0][1]["scorer"], "Алексей Ионов")
        self.assertEqual(event_log[1][0], MatchEvent.YELLOW_CARD)

    def test_statistics_tracker_with_mock_data(self):
        """Тест трекера статистики с mock данными"""
        # Создаем mock матч
        mock_match = MagicMock()
        stats_tracker = StatisticsTracker()

        # Симулируем события через update
        stats_tracker.update(MatchEvent.GOAL, {
            "team": "home",
            "scorer": "Test Player",
            "minute": 23
        })
        stats_tracker.update(MatchEvent.YELLOW_CARD, {
            "player": "Test Player 2",
            "minute": 45
        })
        stats_tracker.update(MatchEvent.GOAL, {
            "team": "away",
            "scorer": "Test Player 3",
            "minute": 67
        })

        # Проверяем статистику
        stats = stats_tracker.get_match_statistics()
        self.assertEqual(stats["total_goals"], 2)
        self.assertEqual(stats["home_goals"], 1)
        self.assertEqual(stats["away_goals"], 1)
        self.assertEqual(stats["yellow_cards"], 1)
        self.assertEqual(stats["goal_scorers"], ["Test Player", "Test Player 3"])


if __name__ == '__main__':
    unittest.main()