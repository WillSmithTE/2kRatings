from service.PlayerService import PlayerService
from model.Player import Player
from model.Player import TeamMinutes

playerService = PlayerService()

def testGetMinutesTraeYoung():
   player = Player("1629027", "Trae Young", "Atlanta Hawks")
   teamsMinutes = playerService.get2020Minutes(player.id)
   assert teamsMinutes == [TeamMinutes('Atlanta Hawks', 2118)]

def testGetMinutesMalikBeasley():
   player = Player("1627736", "Malik Beasley", "Minnesota Timberwolves")
   actual = playerService.get2020Minutes(player.id)
   
   assert actual == [
      TeamMinutes('Minnesota Timberwolves', 463),
      TeamMinutes('Denver Nuggets', 746)
   ]

def testGetAllPlayers():
   assert len(playerService.getAllPlayers().values()) > 100

def testPut2kRatingsOnPlayers():
   player = Player("1627736", "Malik Beasley", "Minnesota Timberwolves")

   playerService.put2kRatingsOnPlayers({ 'Malik Beasley': player })

   assert player.rating == 77
