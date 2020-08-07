from util.util import *
from model.Player import Player
from util.teams import teams
import requests

def getLineupsAddress(teamId):
    return ('https://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID='
        + str(teamId) + '&VsConference=&VsDivision=')

LINEUPS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Referer': 'https://stats.nba.com/lineups/advanced/?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612750'
}

class PlayerService:

    def __init__(self):
        self.lineupsResponses = {}

    def get2020MinutesPlayedForCurrentTeam(self, player):
        response = None
        teamName = player.teamName
        if teamName in self.lineupsResponses:
            response = self.lineupsResponses[teamName]
        else:
            response = self.__getResponse(teamName)
            self.lineupsResponses[teamName] = response
        return self.__getMinutes(player.name, response)

    def playerSoupToPlayer(self, soupPlayer, teamName):
        name = soupPlayer.contents[1].find_all('span')[1].contents[0].contents[0]
        rating = int(soupPlayer.contents[2].contents[0].contents[0])
        return Player(name, teamName, rating)

    def __getResponse(self, teamName):
        teamId = next(team for team in teams if team.fullName == teamName).id
        return requests.get(getLineupsAddress(teamId), headers=LINEUPS_HEADERS).json()

    def __getMinutes(self, playerName, response):
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
