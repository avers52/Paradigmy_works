import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from football import PlayerFactory, CaptainDecorator, InjuredDecorator, YoungTalentDecorator, PlayerPosition


class TestPlayerDecorators(unittest.TestCase):
    """TDD тесты для декораторов игроков"""

    def setUp(self):
        self.midfielder = PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Денис Черышев", 6)
        self.defender = PlayerFactory.create_player(PlayerPosition.DEFENDER, "Марио Фернандес", 2)
        self.forward = PlayerFactory.create_player(PlayerPosition.FORWARD, "Александр Соболев", 11)

    def test_captain_decorator(self):
        """Тест декоратора капитана"""
        # When
        captain = CaptainDecorator(self.midfielder)

        # Then
        self.assertTrue(captain.is_captain)
        self.assertEqual(captain.leadership_bonus, 1.15)
        self.assertIn("лидерство", captain.get_specific_skills())
        self.assertIn("(Капитан)", str(captain))
        self.assertEqual(captain.motivate_team(), "💪 Денис Черышев мотивирует команду перед матчем!")

    def test_injured_decorator(self):
        """Тест декоратора травмы"""
        # When
        injured_player = InjuredDecorator(self.defender, "растяжение связок", 14)

        # Then
        self.assertEqual(injured_player.injury_type, "растяжение связок")
        self.assertEqual(injured_player.recovery_days, 14)
        self.assertFalse(injured_player.can_play)
        self.assertIn("травма: растяжение связок", injured_player.get_specific_skills())
        self.assertIn("Травмирован", str(injured_player))

    def test_young_talent_decorator(self):
        """Тест декоратора молодого таланта"""
        # When
        young_talent = YoungTalentDecorator(self.forward, 0.85, 19)

        # Then
        self.assertEqual(young_talent.potential, 0.85)
        self.assertEqual(young_talent.age, 19)
        self.assertTrue(young_talent.is_promising)
        self.assertIn("потенциал", young_talent.get_specific_skills())
        self.assertIn("Молодой талант", str(young_talent))

    def test_multiple_decorators(self):
        """Тест нескольких декораторов на одном игроке"""
        # When
        young_player = YoungTalentDecorator(self.midfielder, 0.9, 20)
        captain = CaptainDecorator(young_player)

        # Then
        self.assertTrue(captain.is_captain)
        self.assertEqual(captain.potential, 0.9)
        self.assertIn("потенциал", captain.get_specific_skills())
        self.assertIn("лидерство", captain.get_specific_skills())


if __name__ == '__main__':
    unittest.main()