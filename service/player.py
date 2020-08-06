import requests

response = requests.get('https://stats.nba.com/players/list/')
soup = BeautifulSoup(response.text, 'html.parser')