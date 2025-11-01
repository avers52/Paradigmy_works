from abc import ABC, abstractmethod
from typing import List
from football.domain.enums import MatchEvent


class MatchObserver(ABC):
    """Абстрактный наблюдатель за событиями матча"""

    @abstractmethod
    def update(self, event_type: MatchEvent, data: dict):
        pass


class MatchSubject:
    """Субъект для управления наблюдателями"""

    def __init__(self):
        self._observers: List[MatchObserver] = []

    def attach(self, observer: MatchObserver) -> None:
        """Добавить наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: MatchObserver) -> None:
        """Удалить наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, event_type: MatchEvent, data: dict) -> None:
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(event_type, data)


class FootballMatch(MatchSubject):
    """Футбольный матч - основной субъект для наблюдения"""

    def __init__(self, home_team: str, away_team: str, stadium: str = ""):
        super().__init__()
        self.home_team = home_team
        self.away_team = away_team
        self.stadium = stadium or f"Стадион {home_team}"
        self.score = {"home": 0, "away": 0}
        self.minute = 0
        self.is_finished = False
        self.events_log = []

    def start_match(self) -> None:
        """Начать матч"""
        self.minute = 0
        self.is_finished = False
        self.notify(MatchEvent.MATCH_START, {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "stadium": self.stadium
        })

    def goal(self, team: str, scorer: str, minute: int, assist: str = None) -> None:
        """Зафиксировать гол"""
        self.score[team] += 1
        self.minute = minute

        event_data = {
            "team": team,
            "scorer": scorer,
            "assist": assist,
            "minute": minute,
            "score": self.score.copy(),
            "team_name": self.home_team if team == "home" else self.away_team
        }

        self.events_log.append(("GOAL", event_data))
        self.notify(MatchEvent.GOAL, event_data)

    def yellow_card(self, player: str, minute: int, reason: str = "нарушение правил") -> None:
        """Зафиксировать желтую карточку"""
        self.minute = minute

        event_data = {
            "player": player,
            "minute": minute,
            "reason": reason
        }

        self.events_log.append(("YELLOW_CARD", event_data))
        self.notify(MatchEvent.YELLOW_CARD, event_data)

    def substitution(self, player_out: str, player_in: str, minute: int) -> None:
        """Зафиксировать замену"""
        self.minute = minute

        event_data = {
            "player_out": player_out,
            "player_in": player_in,
            "minute": minute
        }

        self.events_log.append(("SUBSTITUTION", event_data))
        self.notify(MatchEvent.SUBSTITUTION, event_data)

    def finish_match(self) -> None:
        """Завершить матч"""
        self.is_finished = True
        self.minute = 90

        event_data = {
            "final_score": self.score.copy(),
            "winner": self.get_winner(),
            "home_team": self.home_team,
            "away_team": self.away_team
        }

        self.events_log.append(("MATCH_END", event_data))
        self.notify(MatchEvent.MATCH_END, event_data)

    def get_winner(self) -> str:
        """Определить победителя"""
        if self.score["home"] > self.score["away"]:
            return self.home_team
        elif self.score["away"] > self.score["home"]:
            return self.away_team
        else:
            return "ничья"

    def get_match_info(self) -> dict:
        """Получить информацию о матче"""
        return {
            "home_team": self.home_team,
            "away_team": self.away_team,
            "score": self.score,
            "minute": self.minute,
            "is_finished": self.is_finished,
            "winner": self.get_winner() if self.is_finished else None,
            "total_events": len(self.events_log)
        }


class Commentator(MatchObserver):
    """Конкретный наблюдатель - комментатор"""

    def __init__(self, name: str):
        self.name = name

    def update(self, event_type: MatchEvent, data: dict) -> None:
        if event_type == MatchEvent.MATCH_START:
            print(
                f"🎙️ {self.name}: Матч начинается! {data['home_team']} против {data['away_team']} на стадионе {data['stadium']}")

        elif event_type == MatchEvent.GOAL:
            team_name = data['team_name']
            print(f"🎙️ {self.name}: ГОООЛ! {data['scorer']} забивает на {data['minute']} минуте! "
                  f"Счет {data['score']['home']}-{data['score']['away']} в пользу {team_name}")

            if data.get('assist'):
                print(f"🎙️ {self.name}: Голевая передача от {data['assist']}!")

        elif event_type == MatchEvent.YELLOW_CARD:
            print(
                f"🎙️ {self.name}: Желтая карточка! {data['player']} получает предупреждение на {data['minute']} минуте. Причина: {data['reason']}")

        elif event_type == MatchEvent.SUBSTITUTION:
            print(
                f"🎙️ {self.name}: Замена! {data['player_out']} уходит, на поле выходит {data['player_in']} на {data['minute']} минуте")

        elif event_type == MatchEvent.MATCH_END:
            winner = data['winner']
            score = data['final_score']
            print(f"🎙️ {self.name}: Матч завершен! Финальный счет {score['home']}-{score['away']}. "
                  f"Победитель: {winner}!")


class StatisticsTracker(MatchObserver):
    """Конкретный наблюдатель - сборщик статистики"""

    def __init__(self):
        self.goals = []
        self.cards = []
        self.substitutions = []
        self.match_events = []

    def update(self, event_type: MatchEvent, data: dict) -> None:
        self.match_events.append((event_type, data))

        if event_type == MatchEvent.GOAL:
            self.goals.append(data)

        elif event_type == MatchEvent.YELLOW_CARD:
            self.cards.append(data)

        elif event_type == MatchEvent.SUBSTITUTION:
            self.substitutions.append(data)

    def get_match_statistics(self) -> dict:
        """Получить полную статистику матча"""
        home_goals = len([g for g in self.goals if g['team'] == 'home'])
        away_goals = len([g for g in self.goals if g['team'] == 'away'])

        return {
            "total_goals": len(self.goals),
            "home_goals": home_goals,
            "away_goals": away_goals,
            "goal_scorers": [g['scorer'] for g in self.goals],
            "yellow_cards": len(self.cards),
            "card_recipients": [c['player'] for c in self.cards],
            "substitutions": len(self.substitutions),
            "total_events": len(self.match_events),
            "goals_data": self.goals,
            "cards_data": self.cards
        }


class MediaReporter(MatchObserver):
    """Конкретный наблюдатель - медиа-репортер"""

    def __init__(self, media_outlet: str):
        self.media_outlet = media_outlet
        self.breaking_news = []

    def update(self, event_type: MatchEvent, data: dict) -> None:
        if event_type == MatchEvent.GOAL:
            news = f"⚽ СЕНСАЦИЯ! {data['scorer']} забивает гол на {data['minute']} минуте!"
            self.breaking_news.append(news)
            print(f"📰 {self.media_outlet}: {news}")

        elif event_type == MatchEvent.MATCH_END:
            winner = data['winner']
            score = data['final_score']
            news = f"🏆 Матч завершен! {data['home_team']} {score['home']}-{score['away']} {data['away_team']}. Победитель: {winner}"
            self.breaking_news.append(news)
            print(f"📰 {self.media_outlet}: {news}")