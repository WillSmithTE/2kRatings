import os
import json
import logging
from model.Data import Data
from model.Team import Team
from model.Player import Player
from service.TeamService import TeamService
from service.PlayerService import PlayerService
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
teamService = TeamService()
playerService = PlayerService()

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
	data.teams = teamService.getTeams()
	teamService.addWinsToTeams(data.teams)
	logging.info('Teams created')

def setPlayersAndTeamTotalRatings():
	for teamName in data.teams.keys():
		teamPlayers = teamService.getPlayers(teamName)
		for player in teamPlayers:
			data.players[player.name] = player
			data.teams[teamName].totalRating += (player.rating ** 8)
	logging.info('Players set')

def setPlayersMinutesPlayedAndTeamsSeasonRatings():
	for player in data.players.values():
		player.minutesPlayed = playerService.get2020MinutesPlayedForCurrentTeam(player)
		data.teams[player.teamName].rating19_20 += (player.rating ** 8) * player.minutesPlayed
	logging.info('Players minutes set')

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

BASKETBALL_REFERENCE_ADDRESS = 'https://widgets.sports-reference.com/wg.fcgi?css=1&site=bbr&url=/players/'

data = Data()
threading.Thread(target=startAPI).start()
threading.Thread(target=main).start()
