import os
import json
from util.util import kebabToSentence
from flask import request, render_template_string


def Controller(app, data):
    @app.route('/', methods=['GET'])
    def landing():
        return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>NBA Ratings API</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            color: white;
            overflow: hidden;
        }
        .container {
            text-align: center;
            z-index: 1;
        }
        h1 {
            font-size: 3rem;
            margin-bottom: 1rem;
            animation: fadeInDown 1s ease-out;
        }
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            margin-bottom: 2rem;
            animation: fadeInUp 1s ease-out 0.3s both;
        }
        .basketball {
            width: 120px;
            height: 120px;
            margin: 2rem auto;
            position: relative;
            animation: bounce 1s ease-in-out infinite;
        }
        .basketball svg {
            width: 100%;
            height: 100%;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.3));
        }
        .court-line {
            width: 200px;
            height: 4px;
            background: rgba(255,255,255,0.3);
            border-radius: 2px;
            margin: 0 auto 2rem;
            animation: pulse 1s ease-in-out infinite;
        }
        .api-links {
            display: flex;
            gap: 1rem;
            flex-wrap: wrap;
            justify-content: center;
            animation: fadeInUp 1s ease-out 0.6s both;
        }
        .api-link {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            color: white;
            text-decoration: none;
            transition: all 0.3s ease;
        }
        .api-link:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-30px); }
        }
        @keyframes pulse {
            0%, 100% { opacity: 0.3; transform: scaleX(1); }
            50% { opacity: 0.6; transform: scaleX(1.1); }
        }
        @keyframes fadeInDown {
            from { opacity: 0; transform: translateY(-30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .stars {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            pointer-events: none;
            overflow: hidden;
        }
        .star {
            position: absolute;
            width: 3px;
            height: 3px;
            background: white;
            border-radius: 50%;
            animation: twinkle 2s ease-in-out infinite;
        }
    </style>
</head>
<body>
    <div class="stars" id="stars"></div>
    <div class="container">
        <div class="basketball">
            <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                <circle cx="50" cy="50" r="45" fill="#ee6730" stroke="#000" stroke-width="2"/>
                <path d="M50 5 Q50 50 50 95" stroke="#000" stroke-width="2" fill="none"/>
                <path d="M5 50 Q50 50 95 50" stroke="#000" stroke-width="2" fill="none"/>
                <path d="M15 20 Q50 35 85 20" stroke="#000" stroke-width="2" fill="none"/>
                <path d="M15 80 Q50 65 85 80" stroke="#000" stroke-width="2" fill="none"/>
            </svg>
        </div>
        <div class="court-line"></div>
        <h1>🏀 NBA Ratings API</h1>
        <p class="subtitle">Get NBA2K20 player ratings and team data</p>
        <div class="api-links">
            <a href="/api/player" class="api-link">All Players</a>
            <a href="/api/team" class="api-link">All Teams</a>
        </div>
    </div>
    <script>
        // Create animated stars background
        const starsContainer = document.getElementById('stars');
        for (let i = 0; i < 50; i++) {
            const star = document.createElement('div');
            star.className = 'star';
            star.style.left = Math.random() * 100 + '%';
            star.style.top = Math.random() * 100 + '%';
            star.style.animationDelay = Math.random() * 2 + 's';
            star.style.opacity = Math.random() * 0.5 + 0.2;
            starsContainer.appendChild(star);
        }
    </script>
</body>
</html>
        ''')

    @app.route('/api/player/<name>', methods=['GET'])
    def getPlayer(name):
        return json.dumps(data.players[kebabToSentence(name)])

    @app.route('/api/team', methods=['GET'])
    def getTeams():
        return json.dumps(data.teams, default=lambda x: x.__dict__)

    @app.route('/api/player', methods=['GET'])
    def getPlayers():
        return json.dumps(data.players, default=lambda x: x.__dict__)

    @app.route('/api/feedback', methods=['GET'])
    def getFeedback():
        return json.dumps(data.feedback, default=lambda x: x.__dict__)

    @app.route('/api/feedback', methods=['POST'])
    def addFeedback():
        data.feedback.append(request.json['feedback'])
        return 'feedback received, thanks mate'

    @app.route('/hi', methods=['GET'])
    def hi(_):
        return 'salut'

    app.run(host='0.0.0.0', port=int(
            os.environ.get('PORT', 5000)), debug=False)
