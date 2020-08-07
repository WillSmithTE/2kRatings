from service.PlayerService import PlayerService
from model.Player import Player

playerService = PlayerService()

def testGet2020MinutesPlayedForCurrentTeam():
   player = Player("Trae Young", "Atlanta Hawks", 90)
   print(player)
   minutes = playerService.get2020MinutesPlayedForCurrentTeam(player)
   assert minutes == 100

players = {
   "Trae Young":{
      "id":"dummyid",
      "name":"Trae Young",
      "teamName":"Atlanta Hawks",
      "rating":90,
      "minutesPlayed":0
   },
   "John Collins":{
      "id":"dummyid",
      "name":"John Collins",
      "teamName":"Atlanta Hawks",
      "rating":86,
      "minutesPlayed":0
   },
   "Clint Capela":{
      "id":"dummyid",
      "name":"Clint Capela",
      "teamName":"Atlanta Hawks",
      "rating":86,
      "minutesPlayed":0
   },
   "Jeff Teague":{
      "id":"dummyid",
      "name":"Jeff Teague",
      "teamName":"Atlanta Hawks",
      "rating":78,
      "minutesPlayed":0
   },
   "De\u2019Andre Hunter":{
      "id":"dummyid",
      "name":"De\u2019Andre Hunter",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "Kevin Huerter":{
      "id":"dummyid",
      "name":"Kevin Huerter",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "Bruno Fernando":{
      "id":"dummyid",
      "name":"Bruno Fernando",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "DeAndre\u2019 Bembry":{
      "id":"dummyid",
      "name":"DeAndre\u2019 Bembry",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "Damian Jones":{
      "id":"dummyid",
      "name":"Damian Jones",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "Skal Labissiere":{
      "id":"dummyid",
      "name":"Skal Labissiere",
      "teamName":"Atlanta Hawks",
      "rating":75,
      "minutesPlayed":0
   },
   "Cameron Reddish":{
      "id":"dummyid",
      "name":"Cameron Reddish",
      "teamName":"Atlanta Hawks",
      "rating":73,
      "minutesPlayed":0
   },
   "Dewayne Dedmon":{
      "id":"dummyid",
      "name":"Dewayne Dedmon",
      "teamName":"Atlanta Hawks",
      "rating":73,
      "minutesPlayed":0
   },
   "Vince Carter":{
      "id":"dummyid",
      "name":"Vince Carter",
      "teamName":"Atlanta Hawks",
      "rating":72,
      "minutesPlayed":0
   },
   "Treveon Graham":{
      "id":"dummyid",
      "name":"Treveon Graham",
      "teamName":"Atlanta Hawks",
      "rating":71,
      "minutesPlayed":0
   },
   "Brandon Goodwin":{
      "id":"dummyid",
      "name":"Brandon Goodwin",
      "teamName":"Atlanta Hawks",
      "rating":70,
      "minutesPlayed":0
   },
   "Charles Brown Jr.":{
      "id":"dummyid",
      "name":"Charles Brown Jr.",
      "teamName":"Atlanta Hawks",
      "rating":69,
      "minutesPlayed":0
   },
   "Jayson Tatum":{
      "id":"dummyid",
      "name":"Jayson Tatum",
      "teamName":"Boston Celtics",
      "rating":88,
      "minutesPlayed":0
   },
   "Kemba Walker":{
      "id":"dummyid",
      "name":"Kemba Walker",
      "teamName":"Boston Celtics",
      "rating":87,
      "minutesPlayed":0
   },
   "Jaylen Brown":{
      "id":"dummyid",
      "name":"Jaylen Brown",
      "teamName":"Boston Celtics",
      "rating":85,
      "minutesPlayed":0
   }
}