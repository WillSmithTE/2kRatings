from model.Team import Team
from service.PlayerService import PlayerService
from util.teams import teams as teamsUtil
import logging
import requests
from bs4 import BeautifulSoup
from inflection import parameterize

NBA_STANDINGS_ADDRESS = 'https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2019-20&SeasonType=Regular+Season'
NBA_STANDINGS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-nba-stats-origin': 'stats',
    'referer': 'https://stats.nba.com/standings/'
}
BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'


class TeamService:
    def getTeams(_):
        teams = {}
        for team in teamsUtil:
            teamName = team.fullName
            teams[teamName] = Team(team.id)
        return teams

    def addWinsToTeams(_, teams):
        response = requests.get(NBA_STANDINGS_ADDRESS, headers=NBA_STANDINGS_HEADERS).json()
        headers = response['resultSets'][0]['headers']
        teamcityIndex = headers.index('TeamCity')
        teamnameIndex = headers.index('TeamName')
        winsIndex = headers.index('WINS')
        dataRows = response['resultSets'][0]['rowSet']
        for row in dataRows:
            teamname = row[teamcityIndex] + ' ' + row[teamnameIndex]
            wins = row[winsIndex]
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


def getTeamUrl(teamName):
    kebabCaseName = parameterize(teamName)
    return BASE_RATINGS_ADDRESS + kebabCaseName
