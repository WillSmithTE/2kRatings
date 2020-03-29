import requests
import urllib.request
import time
import os
import json
import logging
import pickle
import glob

from bs4 import BeautifulSoup
from teams import teams
from inflection import parameterize
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from time import time

REFRESH_RATE_SECONDS = 3600
BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'
BASKETBALL_REFERENCE_ADDRESS = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/'
players = {}

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
	for team in teams:
		teamName = team['teamName']
		teamUrl = getTeamUrl(teamName)
		response = requests.get(teamUrl)
		soup = BeautifulSoup(response.text, 'html.parser')
		playersTags = soup.find_all('td', class_='roster-entry')
		playersForTeam = list(map(lambda x: x.contents[0].contents[1].lower(), playersTags))
		scoresTags = soup.find_all('span', class_='roster-rating')[::3]
		scores = list(map(lambda x: int(x.contents[0]), scoresTags))
		for i in range(len(playersForTeam)):
			players[playersForTeam[i]] = { 'team': teamName, 'rating': scores[i] }
	
	for playerName in players.keys():
		players[playerName]['minutesPlayed'] = getTotalMinutes(playerName)

	pickleFile = open(str(time()).split('.')[0] + '.pickle', 'wb')
	pickle.dump(players, pickleFile)
	pickleFile.close()

def getTotalMinutes(playerName):
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

app = Flask(__name__)
CORS(app)
savedPickleFileName = glob.glob('*.pickle')[0]
timeOfLastUpdate = int(savedPickleFileName.split('.')[0])

if time() - timeOfLastUpdate > REFRESH_RATE_SECONDS:
	setPlayers()
	os.remove(savedPickleFileName)

@app.route('/api/2k/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(players[kebabToSentence(name)])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
