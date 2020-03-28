import requests
import urllib.request
import time
from bs4 import BeautifulSoup
from teams import teams
from inflection import parameterize

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
