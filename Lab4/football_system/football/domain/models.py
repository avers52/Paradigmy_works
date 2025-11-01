from abc import ABC, abstractmethod
from .enums import PlayerPosition


class Player(ABC):
    def __init__(self, name: str, number: int):
        self.name = name
        self.number = number
        self.position = self.get_position()

    @abstractmethod
    def get_position(self) -> str:
        pass

    @abstractmethod
    def get_specific_skills(self) -> list:
        pass

    def train(self) -> str:
        return f"{self.name} тренируется"

    def play(self) -> str:
        return f"{self.name} (#{self.number}) играет на позиции {self.position}"

    def __str__(self):
        return f"{self.name} (#{self.number}) - {self.position}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self.name}', {self.number})"