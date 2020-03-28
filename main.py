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

BASE_RATINGS_ADDRESS = 'https://www.2kratings.com/nba2k20-team/'

def getTeamUrl(teamName):
	kebabCaseName = parameterize(teamName)
	return BASE_RATINGS_ADDRESS + kebabCaseName

for team in teams:
	teamUrl = getTeamUrl(team['teamName'])
	response = requests.get(teamUrl)
	soup = BeautifulSoup(response.text, 'html.parser')
	rosterEntries = soup.find_all('td', class_='roster-entry')
	print(rosterEntries[0].contents)

app = Flask(__name__)
CORS(app)

@app.route('/api/2k/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(100)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=os.environ.get('PORT', '5000'))