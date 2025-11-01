"""
Football System - система управления футбольным клубом
Реализация паттернов проектирования: Фабрика, Декоратор, Наблюдатель
"""

from .domain.enums import PlayerPosition, MatchEvent
from .domain.models import Player
from .creational.factory import PlayerFactory
from .structural.decorators import CaptainDecorator, InjuredDecorator, YoungTalentDecorator
from .behavioral.observer import FootballMatch, Commentator, StatisticsTracker, MediaReporter

__version__ = "1.0.0"
__author__ = "Football System Team"

__all__ = [
    'PlayerPosition',
    'MatchEvent',
    'Player',
    'PlayerFactory',
    'CaptainDecorator',
    'InjuredDecorator',
    'YoungTalentDecorator',
    'FootballMatch',
    'Commentator',
    'StatisticsTracker',
    'MediaReporter'
]