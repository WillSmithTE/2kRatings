import requests
import urllib.request
import time
import os
import json
import psycopg2
from bs4 import BeautifulSoup
from teams import teams
from inflection import parameterize
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
import logging

BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'
players = {}

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

def getTeamUrl(teamName):
	kebabCaseName = parameterize(teamName)
	return BASE_RATINGS_ADDRESS + kebabCaseName

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

app = Flask(__name__)
CORS(app)
setPlayers()

@app.route('/api/2k/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(players[kebabToSentence(name)])

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))
