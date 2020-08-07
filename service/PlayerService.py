from util.util import *
from model.Player import Player
from model.Player import TeamMinutes
from util.teams import teams, getTeamFromAbbreviation
from model.NbaStats import NbaStats
import requests
from bs4 import BeautifulSoup
import logging

TOTAL_ROW = 'TOT'

ALL_PLAYERS_PATH = 'https://stats.nba.com/stats/commonallplayers?season=2019-20&isOnlyCurrentSeason=1&leagueId=00'

def getLineupsAddress(teamId):
    return ('https://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID='
        + str(teamId) + '&VsConference=&VsDivision=')

NBA_STATS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'Referer': 'https://stats.nba.com/lineups/advanced/?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612750'
}

def getPlayerStatsAddress(playerId):
    return 'https://stats.nba.com/stats/playerdashboardbyyearoveryear?DateFrom=&DateTo=&GameSegment=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerID=' + str(playerId) + '&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&Split=yoy&VsConference=&VsDivision='

class PlayerService:

    def __init__(self):
        self.lineupsResponses = {}

    def getAllPlayers(_):
        players = {}
        stats = NbaStats(requests.get(ALL_PLAYERS_PATH, headers = NBA_STATS_HEADERS).json())
        idColumnIndex = stats.getColumnIndex('PERSON_ID')
        nameColumnIndex = stats.getColumnIndex('DISPLAY_FIRST_LAST')
        teamCityColumnIndex = stats.getColumnIndex('TEAM_CITY')
        teamNameColumnIndex = stats.getColumnIndex('TEAM_NAME')

        for row in stats.getRows():
            playerName = row[nameColumnIndex]
            players[playerName] = Player(
                row[idColumnIndex],
                playerName,
                row[teamCityColumnIndex] + ' ' + row[teamNameColumnIndex]
            )
        return players

    def put2kRatingsOnPlayers(self, players):
        playersSoup = BeautifulSoup(requests.get('https://hoopshype.com/nba2k/').text, 'html.parser')
        rows = playersSoup.find_all('div', class_='hh-ranking-ranking')[0].find_all('tr')
        for row in rows:
            try:
                name = row.find('td', class_='name').find('a').contents[0].strip()
                rating = int(row.find('td', class_='value').contents[0].strip())
                if name in players:
                    players[name].rating = rating
                else:
                    logging.info('Found a 2k rating for player not in db: ' + name)
            except Exception:
                logging.error('Failed to extract a 2k rating')

    def get2020Minutes(self, playerId):
        minutesList = []

        stats = NbaStats(requests.get(getPlayerStatsAddress(playerId), headers=NBA_STATS_HEADERS).json())
        minutesColumnIndex = stats.getColumnIndex('MIN')
        gamesPlayedColumnIndex = stats.getColumnIndex('GP')
        teamIndex = stats.getColumnIndex('TEAM_ABBREVIATION')
        
        for row in stats.getRows():
            if row[teamIndex] != TOTAL_ROW:
                minutesPerGame = row[minutesColumnIndex]
                gamesPlayed = row[gamesPlayedColumnIndex]
                teamAbbreviation = row[teamIndex]
                teamName = getTeamFromAbbreviation(teamAbbreviation).fullName
                minutes = round(minutesPerGame * gamesPlayed)
                minutesList.append(TeamMinutes(teamName, minutes))
        return minutesList

    def playerSoupToPlayer(self, soupPlayer, teamName):
        name = soupPlayer.contents[1].find_all('span')[1].contents[0].contents[0]
        rating = int(soupPlayer.contents[2].contents[0].contents[0])
        return Player(name, teamName, rating)
