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
	setPlayers()
	setPlayers2kRatings()
	setTeam2kRatings
	setPlayersMinutesPlayedAndTeamsExpectedQuality()

def initialiseTeams():
	data.teams = teamService.getTeams()
	teamService.addWinsToTeams(data.teams)
	logging.info('Teams created')

def setPlayers():
	data.players = playerService.getAllPlayers()
	logging.info('Players created')

def setPlayers2kRatings():
	playerService.put2kRatingsOnPlayers(data.players)
	logging.info('Player 2k ratings added')

def setTeam2kRatings():
	for player in data.players.values():
		data.teams[player.teamName].2kRating += player.rating
	logging.info('Teams 2k ratings added')

def setPlayersMinutesPlayedAndTeamsExpectedQuality():
	for player in data.players.values():
		player.teamsMinutes = playerService.get2020Minutes(player.id)
		for teamMinutes in player.teamsMinutes:
			valueAdded = (player.rating ** 8) * teamMinutes.minutes
			data.teams[teamMinutes.teamName].2019_20ExpectedQuality += valueAdded
	logging.info('Players minutes and teams expected quality set')

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

data = Data()
threading.Thread(target=startAPI).start()
threading.Thread(target=main).start()
