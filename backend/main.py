import requests
import urllib.request
import time
import os
import json
import logging
import glob
from model.Data import Data
from model.Team import Team
from model.Player import Player
from bs4 import BeautifulSoup
from teams import teams as teamsUtil
from inflection import parameterize
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from time import time

REFRESH_RATE_SECONDS = 3600
BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'
BASKETBALL_REFERENCE_ADDRESS = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/'
NBA_STANDINGS_ADDRESS = 'https://stats.nba.com/stats/leaguestandingsv3?LeagueID=00&Season=2019-20&SeasonType=Regular+Season'
NBA_STANDINGS_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
	'x-nba-stats-origin': 'stats',
	'referer': 'https://stats.nba.com/standings/'
}
def getLineupsAddress(team):
	return ('https://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID='
		+ str(team.id) + '&VsConference=&VsDivision=')
LINEUPS_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
	'x-nba-stats-origin': 'stats',
	'Referer': 'https://stats.nba.com/lineups/advanced/?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612750'
}
data = Data()
newTime = 0

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

def getFormattedName(names, playerName):
	if playerName == 'clint capela':
		return 'capelca'
	return names[1][slice(5)] + names[0][slice(2)].lower()

def getTeamUrl(teamName):
	kebabCaseName = parameterize(teamName)
	return BASE_RATINGS_ADDRESS + kebabCaseName

def getBasketBallReferenceAddress(playerName):
	names = playerName.split(' ')
	formattedName = getFormattedName(names, playerName)
	lastnameInitial = names[1][slice(1)]
	return BASKETBALL_REFERENCE_ADDRESS + lastnameInitial + '/' + formattedName + '01.html&div=div_totals'

def setPlayers():
	lineupsResponses = {}
	for team in teamsUtil:
		teamName = team.fullName
		data.teams[teamName] = Team(team.id)
		teamUrl = getTeamUrl(teamName)
		response = requests.get(teamUrl)
		soup = BeautifulSoup(response.text, 'html.parser')
		playersTags = soup.find_all('td', class_='roster-entry')
		playerNamesForTeam = list(map(lambda x: x.contents[0].contents[1].lower(), playersTags))
		scoresTags = soup.find_all('span', class_='roster-rating')[::3]
		scores = list(map(lambda x: int(x.contents[0]), scoresTags))
		for i in range(len(playerNamesForTeam)):
			rating = scores[i]
			data.players[playerNamesForTeam[i]] = Player(teamName, rating)
			data.teams[teamName].totalRating += (rating ** 8)
		lineupsResponses[teamName] = requests.get(getLineupsAddress(team), headers=LINEUPS_HEADERS).json()
	for playerName in data.players.keys():
		teamName = data.players[playerName].teamName
		data.players[playerName].minutesPlayed = get2020MinutesPlayedForCurrentTeam(
			playerName,
			lineupsResponses[teamName]
		)
		data.teams[teamName].rating19_20 += (data.players[playerName].rating ** 8) * data.players[playerName].minutesPlayed
	setTeamWins()

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

def setTeamWins():
	response = requests.get(NBA_STANDINGS_ADDRESS, headers=NBA_STANDINGS_HEADERS).json()
	headers = response['resultSets'][0]['headers']
	teamcityIndex = headers.index('TeamCity')
	teamnameIndex = headers.index('TeamName')
	winsIndex = headers.index('WINS')
	dataRows = response['resultSets'][0]['rowSet']
	for row in dataRows:
		teamname = row[teamcityIndex] + ' ' + row[teamnameIndex]
		if teamname == 'LA Clippers':
			teamname = 'Los Angeles Clippers'
		wins = row[winsIndex]
		data.teams[teamname].wins = wins

app = Flask(__name__)
CORS(app)

# setPlayers()

@app.route('/api/player/<name>', methods=['GET'])
def getPrediction(name):
	return 'you searched for ' + name
    # return json.dumps(data.players[kebabToSentence(name)])

@app.route('/api/team', methods=['GET'])
def getTeams():
	return json.dumps(data.teams, default=lambda x: x.__dict__)

@app.route('/api/player', methods=['GET'])
def getPlayers():
	return json.dumps(data.players, default=lambda x: x.__dict__)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
