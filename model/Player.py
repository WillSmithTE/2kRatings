class Player:
    def __init__(self, id, name, teamName):
        self.id = id
        self.name = name
        self.teamName = teamName
        self.rating = 0
        self.teamsMinutes = []

class TeamMinutes:
    def __init__(self, teamName, minutes):
        self.teamName = teamName
        self.minutes = minutes

    def __eq__(self, other):
        return self.teamName == other.teamName and self.minutes == other.minutes