import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from football import FootballMatch, Commentator, StatisticsTracker, MediaReporter, MatchEvent


class TestMatchObserver(unittest.TestCase):
    """TDD тесты для паттерна Наблюдатель"""

    def setUp(self):
        self.match = FootballMatch("Спартак", "Зенит", "Лужники")
        self.commentator = Commentator("Георгий Черданцев")
        self.stats_tracker = StatisticsTracker()
        self.media = MediaReporter("Спорт-Экспресс")

    def test_observer_attachment(self):
        """Тест подключения наблюдателей"""
        # When
        self.match.attach(self.commentator)
        self.match.attach(self.stats_tracker)
        self.match.attach(self.media)

        # Then
        # Проверяем через события матча
        self.match.start_match()
        self.match.goal("home", "Квинси Промес", 23)

        stats = self.stats_tracker.get_match_statistics()
        self.assertEqual(stats["total_goals"], 1)

    def test_goal_notification(self):
        """Тест уведомления о голе"""
        # Given
        self.match.attach(self.stats_tracker)

        # When
        self.match.goal("home", "Квинси Промес", 23, "Александр Соболев")

        # Then
        stats = self.stats_tracker.get_match_statistics()
        self.assertEqual(stats["total_goals"], 1)
        self.assertEqual(stats["home_goals"], 1)
        self.assertEqual(stats["goal_scorers"][0], "Квинси Промес")

    def test_match_finish(self):
        """Тест завершения матча"""
        # Given
        self.match.attach(self.stats_tracker)

        # When
        self.match.goal("home", "Квинси Промес", 23)
        self.match.goal("away", "Артем Дзюба", 67)
        self.match.finish_match()

        # Then
        stats = self.stats_tracker.get_match_statistics()
        self.assertEqual(stats["total_goals"], 2)
        self.assertEqual(self.match.get_winner(), "ничья")

    def test_detach_observer(self):
        """Тест отключения наблюдателя"""
        # Given
        self.match.attach(self.stats_tracker)
        self.match.detach(self.stats_tracker)

        # When
        self.match.goal("home", "Квинси Промес", 23)

        # Then
        stats = self.stats_tracker.get_match_statistics()
        self.assertEqual(stats["total_goals"], 0)


if __name__ == '__main__':
    unittest.main()