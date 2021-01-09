class Team():
    def __init__(self, id):
        self.id = id
        self.wins = 0
        self.rating2k = 0
        self.expectedQuality19_20 = 0
        self.year20_21 = TeamStats()

class TeamStats():
    def __init__(self):
        self.homeWins = 0
        self.awayWins = 0
