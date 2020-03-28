import requests
import urllib.request
import time
import os
import json
from bs4 import BeautifulSoup
from teams import teams
from inflection import parameterize
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'

POSTGRES_CONFIG = {
	'user': 'nbaratings',
	'pw': 'nbaratings',
	'db': 'nbaratings',
	'host': 'localhost',
	'port': '5432'
}

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

def getTeamUrl(teamName):
	kebabCaseName = parameterize(teamName)
	return BASE_RATINGS_ADDRESS + kebabCaseName

def getScoresAndPlayers():
	data = {}
	for team in teams:
		teamName = team['teamName']
		teamData = {}
		teamUrl = getTeamUrl(teamName)
		response = requests.get(teamUrl)
		soup = BeautifulSoup(response.text, 'html.parser')
		playersTags = soup.find_all('td', class_='roster-entry')
		players = list(map(lambda x: x.contents[0].contents[1], playersTags))
		scoresTags = soup.find_all('span', class_='roster-rating')[::3]
		scores = list(map(lambda x: int(x.contents[0]), scoresTags))
		for i in range(len(players)):
			teamData[players[i]] = scores[i]
		data[teamName] = teamData
	return data

app = Flask(__name__)
CORS(app)

db = SQLAlchemy()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES_CONFIG

db.init_app(app)

@app.route('/api/2k/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(kebabToSentence(name))

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))