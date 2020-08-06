from util.util import *
from model.Player import Player

class PlayerService:

    @staticmethod
    def get2020MinutesPlayedForCurrentTeam(playerName, response):
        minutesIndex = response['resultSets'][0]['headers'].index('MIN')
        groupNameIndex = response['resultSets'][0]['headers'].index('GROUP_NAME')
        minutes = 0
        dataRows = response['resultSets'][0]['rowSet']
        for row in dataRows:
            splitName = playerName.split(' ')
            lastName = splitName[len(splitName) - 1]
            if lastName in row[groupNameIndex].lower():
                minutes += row[minutesIndex]
        return minutes

    @staticmethod
    def playerSoupToPlayer(soupPlayer, teamName):
        # save(soupPlayer, 'player.pickle')
        name = soupPlayer.contents[1].find_all('span')[1].contents[0].contents[0]
        rating = int(soupPlayer.contents[2].contents[0].contents[0])
        return Player(name, teamName, rating)


