import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from football import (
    PlayerFactory, CaptainDecorator, InjuredDecorator,
    FootballMatch, Commentator, StatisticsTracker, MediaReporter,
    PlayerPosition
)


class TestFootballBDD(unittest.TestCase):
    """BDD тесты в стиле Behavior Driven Development"""

    def test_derby_match_scenario(self):
        """
        BDD Сценарий: Дерби между Спартаком и ЦСКА
        Given команды с капитанами и травмированными игроками
        When происходит напряженный матч с событиями
        Then система корректно обрабатывает все события и статистику
        """
        # Given - подготовка к дерби
        print("\n=== BDD СЦЕНАРИЙ: ДЕРБИ СПАРТАК vs ЦСКА ===")

        # Создаем ключевых игроков
        spartak_players = [
            PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Александр Селихов", 1),
            PlayerFactory.create_player(PlayerPosition.DEFENDER, "Георгий Джикия", 14),
            PlayerFactory.create_player(PlayerPosition.FORWARD, "Квинси Промес", 10)
        ]

        cska_players = [
            PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Игорь Акинфеев", 35),
            PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Алан Дзагоев", 10),
            PlayerFactory.create_player(PlayerPosition.FORWARD, "Федор Чалов", 9)
        ]

        # Назначаем капитанов
        spartak_captain = CaptainDecorator(spartak_players[1])  # Джикия
        cska_captain = CaptainDecorator(cska_players[1])  # Дзагоев

        # Травмируем игрока
        injured_player = InjuredDecorator(cska_players[2], "растяжение", 7)  # Чалов

        # Создаем матч и наблюдателей
        derby_match = FootballMatch("Спартак", "ЦСКА", "Лужники")
        commentator = Commentator("Василий Уткин")
        stats_tracker = StatisticsTracker()
        media = MediaReporter("Чемпионат.com")

        derby_match.attach(commentator)
        derby_match.attach(stats_tracker)
        derby_match.attach(media)

        # When - события матча
        derby_match.start_match()
        derby_match.goal("home", "Квинси Промес", 18, "Александр Соболев")  # Спартак забивает
        derby_match.yellow_card("Алан Дзагоев", 34, "грубая игра")  # ЖК Дзагоеву
        derby_match.substitution("Федор Чалов", "Арнор Сигурдссон", 65)  # Замена травмированного
        derby_match.goal("away", "Арнор Сигурдссон", 78)  # ЦСКА сравнивает
        derby_match.goal("home", "Квинси Промес", 89)  # Победа Спартака
        derby_match.finish_match()

        # Then - проверка результатов
        final_stats = stats_tracker.get_match_statistics()
        match_info = derby_match.get_match_info()

        # Проверки
        self.assertEqual(match_info["winner"], "Спартак")
        self.assertEqual(final_stats["total_goals"], 3)
        self.assertEqual(final_stats["home_goals"], 2)
        self.assertEqual(final_stats["away_goals"], 1)
        self.assertEqual(final_stats["yellow_cards"], 1)

        # Проверяем, что Промес сделал дубль
        promes_goals = [goal for goal in final_stats["goals_data"] if goal["scorer"] == "Квинси Промес"]
        self.assertEqual(len(promes_goals), 2)

        print("✅ BDD сценарий успешно завершен!")

    def test_final_match_with_injuries(self):
        """
        BDD Сценарий: Финал кубка с травмами ключевых игроков
        Given команды с травмированными игроками
        When происходит финальный матч
        Then система корректно обрабатывает ограничения травмированных игроков
        """
        # Given
        print("\n=== BDD СЦЕНАРИЙ: ФИНАЛ КУБКА ===")

        zenit_players = [
            PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Михаил Кержаков", 41),
            PlayerFactory.create_player(PlayerPosition.FORWARD, "Малком", 10),
            PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Вильмар Барриос", 5)
        ]

        lokomotiv_players = [
            PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Гильермо", 1),
            PlayerFactory.create_player(PlayerPosition.FORWARD, "Федор Смолов", 9),
            PlayerFactory.create_player(PlayerPosition.DEFENDER, "Станислав Магкеев", 3)
        ]

        # Травмируем ключевых игроков
        injured_striker = InjuredDecorator(zenit_players[1], "растяжение мышц", 10)
        injured_defender = InjuredDecorator(lokomotiv_players[2], "ушиб", 5)

        # Создаем матч
        final_match = FootballMatch("Зенит", "Локомотив", "ВЭБ Арена")
        commentator = Commentator("Константин Генич")
        stats_tracker = StatisticsTracker()

        final_match.attach(commentator)
        final_match.attach(stats_tracker)

        # When
        final_match.start_match()
        final_match.yellow_card("Вильмар Барриос", 28, "неспортивное поведение")
        final_match.yellow_card("Станислав Магкеев", 41, "подкат")
        final_match.substitution("Малком", "Клаудиньо", 72)
        final_match.goal("home", "Клаудиньо", 88)
        final_match.finish_match()

        # Then
        stats = stats_tracker.get_match_statistics()
        self.assertEqual(final_match.get_winner(), "Зенит")
        self.assertEqual(stats["total_goals"], 1)
        self.assertEqual(stats["yellow_cards"], 2)
        self.assertEqual(stats["goal_scorers"][0], "Клаудиньо")

        print("✅ BDD сценарий финала успешно завершен!")


if __name__ == '__main__':
    unittest.main()