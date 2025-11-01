import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from football import PlayerFactory, PlayerPosition


class TestPlayerFactory(unittest.TestCase):
    """TDD тесты для фабрики игроков"""

    def test_create_goalkeeper(self):
        """Тест создания вратаря"""
        # When
        goalkeeper = PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Игорь Акинфеев", 1)

        # Then
        self.assertEqual(goalkeeper.name, "Игорь Акинфеев")
        self.assertEqual(goalkeeper.number, 1)
        self.assertEqual(goalkeeper.get_position(), "вратарь")
        self.assertIn("реакция", goalkeeper.get_specific_skills())
        self.assertIn("игра руками", goalkeeper.get_specific_skills())

    def test_create_forward(self):
        """Тест создания нападающего"""
        # When
        forward = PlayerFactory.create_player(PlayerPosition.FORWARD, "Артем Дзюба", 22)

        # Then
        self.assertEqual(forward.get_position(), "нападающий")
        self.assertIn("удар", forward.get_specific_skills())
        self.assertIn("голевое чутье", forward.get_specific_skills())

    def test_create_russian_team(self):
        """Тест создания сборной России"""
        # When
        team = PlayerFactory.create_russian_national_team()

        # Then
        self.assertEqual(len(team), 6)

        positions = [player.get_position() for player in team]
        self.assertIn("вратарь", positions)
        self.assertIn("защитник", positions)
        self.assertIn("полузащитник", positions)
        self.assertIn("нападающий", positions)

    def test_invalid_position(self):
        """Тест обработки неверной позиции"""
        with self.assertRaises(ValueError):
            PlayerFactory.create_player("INVALID", "Test", 99)


if __name__ == '__main__':
    unittest.main()