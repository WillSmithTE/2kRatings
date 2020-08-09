import os
import json
from util.util import kebabToSentence


def Controller(app, data):
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
    def hi(_):
        return 'salut'

    app.run(host='0.0.0.0', port=int(
            os.environ.get('PORT', 5000)), debug=False)
