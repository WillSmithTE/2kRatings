from model.Player import Player
from model.Team import Team


class Data:
    def __init__(self):
        self.teams: Dict[str, Team] = {}
        self.players: Dict[str, Player] = {}
