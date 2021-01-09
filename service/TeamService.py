from model.Team import Team
from service.PlayerService import PlayerService
from util.teams import teams as teamsUtil
import logging
import requests
from bs4 import BeautifulSoup
from inflection import parameterize
from model.NbaStats import NbaStats

NBA_STANDINGS_19_20_ADDRESS = 'https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2019-20&SeasonType=Regular+Season'
NBA_STANDINGS_20_21_ADDRESS = 'https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2020-21&SeasonType=Regular+Season'
NBA_STANDINGS_HEADERS = {'Host': 'stats.nba.com', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0', 'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.5', 'Accept-Encoding': 'gzip, deflate, br', 'x-nba-stats-origin': 'stats', 'x-nba-stats-token': 'true', 'Connection': 'keep-alive', 'Referer': 'https://stats.nba.com/', 'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}

BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'


class TeamService:
    def getTeams(_):
        teams = {}
        for team in teamsUtil:
            teamName = team.fullName
            teams[teamName] = Team(team.id)
        return teams

    def addWinsToTeams(_, teams):
        response = requests.get(NBA_STANDINGS_19_20_ADDRESS, headers=NBA_STANDINGS_HEADERS).json()
        headers = response['resultSets'][0]['headers']
        teamcityIndex = headers.index('TeamCity')
        teamnameIndex = headers.index('TeamName')
        winsIndex = headers.index('WINS')
        dataRows = response['resultSets'][0]['rowSet']
        for row in dataRows:
            wins = row[winsIndex]
            teamname = row[teamcityIndex] + ' ' + row[teamnameIndex]
            if teamname in teams:
                teams[teamname].wins = wins
            else:
                logging.error(
                    'Found "wins" for a team not in the db: ' + teamname)

    def getPlayers(_, teamName):
        teamUrl = getTeamUrl(teamName)
        response = requests.get(teamUrl)
        soup = BeautifulSoup(response.text, 'html.parser')
        tableItems = soup.find_all('table')[0].contents[1].contents
        players = list(filter(lambda x: len(x.contents) > 1, tableItems))
        return list(map(lambda x: PlayerService.playerSoupToPlayer(x, teamName), players))

    def add20_21WinsLossesToTeams(self, teams):
        stats = NbaStats(requests.get(NBA_STANDINGS_20_21_ADDRESS, headers=NBA_STANDINGS_HEADERS).json())
        homeWinsIndex = stats.getColumnIndex('HOME')
        awayWinsIndex = stats.getColumnIndex('ROAD')
        for row in stats.getRows():
            teamName = self.getTeamName(stats, row)
            if teamName in teams:
                teams[teamName].year20_21.homeWins = row[homeWinsIndex]
                teams[teamName].year20_21.awayWins = row[awayWinsIndex]

    def getTeamName(_, stats, row):
        teamcityIndex = stats.getColumnIndex('TeamCity')
        teamnameIndex = stats.getColumnIndex('TeamName')
        teamname = row[teamcityIndex] + ' ' + row[teamnameIndex]

def getTeamUrl(teamName):
    kebabCaseName = parameterize(teamName)
    return BASE_RATINGS_ADDRESS + kebabCaseName
