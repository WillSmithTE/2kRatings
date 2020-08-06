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
from service.TeamService import TeamService
from service.PlayerService import PlayerService
from bs4 import BeautifulSoup
from util.teams import teams as teamsUtil
from flask import Flask, request, redirect, url_for, flash, jsonify
from flask_cors import CORS
from time import time
import threading

logging.root.setLevel(logging.INFO)

import sys
sys.setrecursionlimit(100000)

app = Flask(__name__)
CORS(app)

@app.route('/api/player/<name>', methods=['GET'])
def getPrediction(name):
    return json.dumps(data.players[kebabToSentence(name)])

@app.route('/api/team', methods=['GET'])
def getTeams():
	return json.dumps(data.teams, default=lambda x: x.__dict__)

@app.route('/api/player', methods=['GET'])
def getPlayers():
	return json.dumps(data.players, default=lambda x: x.__dict__)


@app.route('/hi', methods=['GET'])
def hi():
	return 'salut'

def startAPI():
	if __name__ == '__main__':
		app.run(host='0.0.0.0', port=os.environ.get('5000'))

def main():
	initialiseTeams()
	setPlayersAndTeamTotalRatings()
	setPlayersMinutesPlayedAndTeamsSeasonRatings()

def initialiseTeams():
	data.teams = TeamService.getTeams()
	TeamService.addWinsToTeams(data.teams)
	logging.info('Teams created')

def setPlayersAndTeamTotalRatings():
	for teamName in data.teams.keys():
		teamPlayers = TeamService.getPlayers(teamName)
		for player in teamPlayers:
			data.players[player.name] = player
			data.teams[teamName].totalRating += (player.rating ** 8)
	logging.info('Players set')

def setPlayersMinutesPlayedAndTeamsSeasonRatings():
	lineupsResponses = {}
	for team in teamsUtil:
		lineupsResponses[team.fullName] = requests.get(getLineupsAddress(team.id), headers=LINEUPS_HEADERS).json()
	for player in data.players.values():
		teamName = player.teamName
		player.minutesPlayed = PlayerService.get2020MinutesPlayedForCurrentTeam(
			player.name,
			lineupsResponses[teamName]
		)
		data.teams[teamName].rating19_20 += (player.rating ** 8) * player.minutesPlayed

	logging.info('Players minutes set')

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

BASKETBALL_REFERENCE_ADDRESS = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/'

def getLineupsAddress(teamId):
	return ('https://stats.nba.com/stats/leaguedashlineups?Conference=&DateFrom=&DateTo=&Division=&GameID=&GameSegment=&GroupQuantity=5&LastNGames=0&LeagueID=00&Location=&MeasureType=Advanced&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlusMinus=N&Rank=N&Season=2019-20&SeasonSegment=&SeasonType=Regular+Season&ShotClockRange=&TeamID='
		+ str(teamId) + '&VsConference=&VsDivision=')

LINEUPS_HEADERS = {
	'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
	'x-nba-stats-origin': 'stats',
	'Referer': 'https://stats.nba.com/lineups/advanced/?Season=2019-20&SeasonType=Regular%20Season&TeamID=1610612750'
}

data = Data()
threading.Thread(target=startAPI).start()
threading.Thread(target=main).start()
