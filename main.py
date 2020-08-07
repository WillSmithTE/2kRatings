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

logging.basicConfig()
logging.root.setLevel(logging.INFO)

app = Flask(__name__)
CORS(app)
teamService = TeamService()
playerService = PlayerService()
data = Data()

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
		app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)

def main():
	initialiseTeams()
	print(1)
	setPlayers()
	print(2)

	setPlayers2kRatings()
	print(3)

	setTeam2kRatings
	print(4)

	setPlayersMinutesPlayedAndTeamsExpectedQuality()
	print(5)

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
	print('startTeam2kratings')
	for player in data.players.values():
		print()
		data.teams[player.teamName].rating2k += player.rating
	logging.info('Teams 2k ratings added')

def setPlayersMinutesPlayedAndTeamsExpectedQuality():
	for player in data.players.values():
		player.teamsMinutes = playerService.get2020Minutes(player.id)
		for teamMinutes in player.teamsMinutes:
			valueAdded = (player.rating ** 8) * teamMinutes.minutes
			data.teams[teamMinutes.teamName].expectedQuality19_20 += valueAdded
	logging.info('Players minutes and teams expected quality set')

def kebabToSentence(kebabCaseName):
	return ' '.join(kebabCaseName.split('-'))

threading.Thread(target=main).start()
threading.Thread(target=startAPI).start()
