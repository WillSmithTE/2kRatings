import requests
import urllib.request
import time
import os
import json
import logging
import pickle
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

data = Data()

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

def pickleDump(toDump):
	pickleFile = open(str(time()).split('.')[0] + '.pickle', 'wb')
	pickle.dump(data, pickleFile)
	pickleFile.close()

def setPlayers():
	for team in teamsUtil:
		teamName = team.fullName
		data.teams[teamName] = Team()
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
			data.teams[teamName].rating += rating
	
	for playerName in data.players.keys():
		data.players[playerName].minutesPlayed = get2020MinutesPlayedForCurrentTeam(playerName)
	setTeamWins()

	pickleDump(data)

def get2020MinutesPlayedForCurrentTeam(playerName):
	response = requests.get(getBasketBallReferenceAddress(playerName))
	soup = BeautifulSoup(response.text, 'html.parser')
	totals = soup.find_all(id='totals.2020')
	try:
		yearRow = totals[len(totals) - 1]
		statTags = yearRow.find_all('td')
		minutesPlayed = int(list(filter(lambda tag: tag['data-stat']=='mp',statTags))[0].contents[0])
		return minutesPlayed
	except:
		logging.error('failed to get 2019-2020 minutes for ' + playerName)
		return 0

def setTeamWins():
	response = requests.get(NBA_STANDINGS_ADDRESS, headers=NBA_STANDINGS_HEADERS).json()
	headers = response['resultSets'][0]['headers']
	teamcityIndex = headers.index('TeamCity')
	teamnameIndex = headers.index('TeamName')
	winsIndex = headers.index('WINS')
	dataRows = response['resultSets'][0]['rowSet']
	for row in dataRows:
		teamname = row[teamcityIndex] + ' ' + row[teamnameIndex]
		wins = row[winsIndex]
		data.teams[teamname].wins = wins

app = Flask(__name__)
CORS(app)
savedPickleFileName = glob.glob('*.pickle')[0]
timeOfLastUpdate = int(savedPickleFileName.split('.')[0])

if time() - timeOfLastUpdate > REFRESH_RATE_SECONDS:
	setPlayers()
	os.remove(savedPickleFileName)

@app.route('/api/player/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(data.players[kebabToSentence(name)])

@app.route('/api/team', methods=['GET'])
def getTeam2kScores():
	return json.dumps(data.teams)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
