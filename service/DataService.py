import logging
from service.TeamService import TeamService
from service.PlayerService import PlayerService
from util.util import save


class DataService:
    def __init__(self, data):
        self.data = data
        self.playerService = PlayerService()
        self.teamService = TeamService()

    def getAllData(self, cache=False):
        self.initialiseTeams()
        print(1)
        self.setPlayers()
        print(2)

        self.setPlayers2kRatings()
        print(3)

        self.setTeam2kRatings()
        print(4)

        self.setPlayersMinutesPlayedAndTeamsExpectedQuality()
        print(5)

        if cache:
            save(self.data, 'data.pickle')

    def getAndCacheAllData(self):
        self.getAllData(True)

    def initialiseTeams(self):
        self.data.teams = self.teamService.getTeams()
        self.teamService.addWinsToTeams(self.data.teams)
        logging.info('Teams created')

    def setPlayers(self):
        self.data.players = self.playerService.getAllPlayers()
        logging.info('Players created')

    def setPlayers2kRatings(self):
        self.playerService.put2kRatingsOnPlayers(self.data.players)
        logging.info('Player 2k ratings added')

    def setTeam2kRatings(self):
        print('startTeam2kratings')
        for player in self.data.players.values():
            if player.teamName in self.data.teams:
                self.data.teams[player.teamName].rating2k += player.rating ** 8
            else:
                logging.error('Unable to find team "' + player.teamName + '" of ' + player.name + ' in db')
        logging.info('Teams 2k ratings added')

    def setPlayersMinutesPlayedAndTeamsExpectedQuality(self):
        for index, player in enumerate(self.data.players.values()):
            if index % 50 == 0:
                print(index, 'players minutes set')
            player.teamsMinutes = self.playerService.get2020Minutes(player.id)
            for teamMinutes in player.teamsMinutes:
                valueAdded = (player.rating ** 8) * teamMinutes.minutes
                self.data.teams[teamMinutes.teamName].expectedQuality19_20 += valueAdded
        logging.info('Players minutes and teams expected quality set')
