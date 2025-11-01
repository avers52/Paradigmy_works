from football.domain.models import Player


class PlayerDecorator(Player):
    """Базовый декоратор для игроков"""

    def __init__(self, player: Player):
        self._player = player

    @property
    def player(self):
        return self._player

    def get_position(self) -> str:
        return self._player.get_position()

    def get_specific_skills(self) -> list:
        return self._player.get_specific_skills()

    def train(self) -> str:
        return self._player.train()

    def play(self) -> str:
        return self._player.play()

    def __getattr__(self, name):
        return getattr(self._player, name)


class CaptainDecorator(PlayerDecorator):
    """Декоратор для капитана команды"""

    def __init__(self, player: Player):
        super().__init__(player)
        self.is_captain = True
        self.leadership_bonus = 1.15
        self.captain_since = None

    def get_specific_skills(self) -> list:
        base_skills = super().get_specific_skills()
        return base_skills + ["лидерство", "мотивация команды", "ответственность"]

    def motivate_team(self) -> str:
        return f"💪 {self.name} мотивирует команду перед матчем!"

    def talk_to_referee(self) -> str:
        return f"🗣️ {self.name} общается с судьей от лица команды"

    def __str__(self):
        return f"{super().__str__()} (Капитан)"


class InjuredDecorator(PlayerDecorator):
    """Декоратор для травмированного игрока"""

    def __init__(self, player: Player, injury_type: str, recovery_days: int):
        super().__init__(player)
        self.injury_type = injury_type
        self.recovery_days = recovery_days
        self.performance_penalty = 0.6
        self.can_play = False

    def get_specific_skills(self) -> list:
        base_skills = super().get_specific_skills()
        return base_skills + [f"травма: {self.injury_type}"]

    def train(self) -> str:
        return f"🏥 {self.name} проходит реабилитацию после травмы ({self.injury_type})"

    def recover(self) -> str:
        self.recovery_days -= 1
        if self.recovery_days <= 0:
            self.can_play = True
            return f"✅ {self.name} полностью восстановился от травмы!"
        return f"🔄 {self.name} восстанавливается, осталось {self.recovery_days} дней"

    def play(self) -> str:
        if not self.can_play:
            return f"❌ {self.name} не может играть из-за травмы {self.injury_type}"
        return super().play()

    def __str__(self):
        return f"{super().__str__()} - Травмирован ({self.injury_type})"


class YoungTalentDecorator(PlayerDecorator):
    """Декоратор для молодого таланта"""

    def __init__(self, player: Player, potential: float, age: int):
        super().__init__(player)
        self.potential = potential  # от 0.0 до 1.0
        self.age = age
        self.learning_rate = 1.3
        self.is_promising = potential > 0.7

    def get_specific_skills(self) -> list:
        base_skills = super().get_specific_skills()
        talent_skills = ["потенциал", "обучаемость", "энергия"]
        if self.potential > 0.8:
            talent_skills.append("будущая звезда")
        return base_skills + talent_skills

    def train(self) -> str:
        base_training = super().train()
        return f"🌟 {base_training} и показывает отличные результаты благодаря таланту!"

    def develop(self) -> str:
        skill_improvement = self.potential * 0.1
        return f"📈 {self.name} развивается! Потенциал увеличивается"

    def __str__(self):
        potential_str = "высокий" if self.potential > 0.7 else "средний"
        return f"{super().__str__()} - Молодой талант ({potential_str} потенциал)"