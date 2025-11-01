from football.domain.models import Player
from football.domain.enums import PlayerPosition


class Goalkeeper(Player):
    def get_position(self) -> str:
        return PlayerPosition.GOALKEEPER.value

    def get_specific_skills(self) -> list:
        return ["реакция", "игра руками", "командование защитой", "игра на выходах"]

    def train(self) -> str:
        return f"{self.name} отрабатывает удары и выходы один на один"


class Defender(Player):
    def get_position(self) -> str:
        return PlayerPosition.DEFENDER.value

    def get_specific_skills(self) -> list:
        return ["отбор мяча", "игра головой", "позиционная игра", "силовой прием"]

    def train(self) -> str:
        return f"{self.name} работает над силовыми приемами и игрой в обороне"


class Midfielder(Player):
    def get_position(self) -> str:
        return PlayerPosition.MIDFIELDER.value

    def get_specific_skills(self) -> list:
        return ["пас", "дриблинг", "видение поля", "длинная передача"]

    def train(self) -> str:
        return f"{self.name} совершенствует передачи и контроль мяча"


class Forward(Player):
    def get_position(self) -> str:
        return PlayerPosition.FORWARD.value

    def get_specific_skills(self) -> list:
        return ["удар", "голевое чутье", "скорость", "игра в штрафной"]

    def train(self) -> str:
        return f"{self.name} отрабатывает удары по воротам и голевые моменты"


class PlayerFactory:
    """Фабрика для создания игроков разных позиций"""

    @staticmethod
    def create_player(position: PlayerPosition, name: str, number: int) -> Player:
        if position == PlayerPosition.GOALKEEPER:
            return Goalkeeper(name, number)
        elif position == PlayerPosition.DEFENDER:
            return Defender(name, number)
        elif position == PlayerPosition.MIDFIELDER:
            return Midfielder(name, number)
        elif position == PlayerPosition.FORWARD:
            return Forward(name, number)
        else:
            raise ValueError(f"Неизвестная позиция: {position}")

    @staticmethod
    def create_russian_national_team():
        """Создает состав сборной России"""
        return [
            PlayerFactory.create_player(PlayerPosition.GOALKEEPER, "Игорь Акинфеев", 1),
            PlayerFactory.create_player(PlayerPosition.DEFENDER, "Марио Фернандес", 2),
            PlayerFactory.create_player(PlayerPosition.DEFENDER, "Георгий Джикия", 14),
            PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Денис Черышев", 6),
            PlayerFactory.create_player(PlayerPosition.MIDFIELDER, "Александр Головин", 17),
            PlayerFactory.create_player(PlayerPosition.FORWARD, "Артем Дзюба", 22)
        ]

    @staticmethod
    def create_team_squad(team_name: str):
        """Создает базовый состав команды"""
        squads = {
            "Спартак": [
                ("Александр Селихов", 1, PlayerPosition.GOALKEEPER),
                ("Георгий Джикия", 14, PlayerPosition.DEFENDER),
                ("Квинси Промес", 10, PlayerPosition.FORWARD)
            ],
            "Зенит": [
                ("Михаил Кержаков", 41, PlayerPosition.GOALKEEPER),
                ("Ярослав Ракицкий", 44, PlayerPosition.DEFENDER),
                ("Малком", 10, PlayerPosition.FORWARD)
            ]
        }

        if team_name not in squads:
            return []

        return [PlayerFactory.create_player(pos, name, num) for name, num, pos in squads[team_name]]