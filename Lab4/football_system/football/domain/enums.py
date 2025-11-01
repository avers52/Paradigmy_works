from enum import Enum

class PlayerPosition(Enum):
    GOALKEEPER = "вратарь"
    DEFENDER = "защитник"
    MIDFIELDER = "полузащитник"
    FORWARD = "нападающий"

class MatchEvent(Enum):
    GOAL = "goal"
    YELLOW_CARD = "yellow_card"
    RED_CARD = "red_card"
    SUBSTITUTION = "substitution"
    MATCH_START = "match_start"
    MATCH_END = "match_end"