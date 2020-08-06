# Team data from https://github.com/bttmly/nba/blob/master/data/teams.json

class TeamInfo:
  def __init__(self, id, abbreviation, fullName, simpleName, location):
    self.id = id
    self.abbreviation = abbreviation
    self.fullName = fullName
    self.simpleName = simpleName
    self.location = location

teams = [
  TeamInfo(1610612737, "ATL", "Atlanta Hawks", "Hawks", "Atlanta"),
  TeamInfo(1610612738, "BOS", "Boston Celtics", "Celtics", "Boston"),
  TeamInfo(1610612751, "BKN", "Brooklyn Nets", "Nets", "Brooklyn"),
  TeamInfo(1610612766, "CHA", "Charlotte Hornets", "Hornets", "Charlotte"),
  TeamInfo(1610612741, "CHI", "Chicago Bulls", "Bulls", "Chicago"),
  TeamInfo(1610612739, "CLE", "Cleveland Cavaliers", "Cavaliers", "Cleveland"),
  TeamInfo(1610612742, "DAL", "Dallas Mavericks", "Mavericks", "Dallas"),
  TeamInfo(1610612743, "DEN", "Denver Nuggets", "Nuggets", "Denver"),
  TeamInfo(1610612765, "DET", "Detroit Pistons", "Pistons", "Detroit"),
  TeamInfo(1610612744, "GSW", "Golden State Warriors", "Warriors", "Golden State"),
  TeamInfo(1610612745, "HOU", "Houston Rockets", "Rockets", "Houston"),
  TeamInfo(1610612754, "IND", "Indiana Pacers", "Pacers", "Indiana"),
  TeamInfo(1610612746, "LAC", "Los Angeles Clippers", "Clippers", "Los Angeles"),
  TeamInfo(1610612747, "LAL", "Los Angeles Lakers", "Lakers", "Los Angeles"),
  TeamInfo(1610612763, "MEM", "Memphis Grizzlies", "Grizzlies", "Memphis"),
  TeamInfo(1610612748, "MIA", "Miami Heat", "Heat", "Miami"),
  TeamInfo(1610612749, "MIL", "Milwaukee Bucks", "Bucks", "Milwaukee"),
  TeamInfo(1610612750, "MIN", "Minnesota Timberwolves", "Timberwolves", "Minnesota"),
  TeamInfo(1610612740, "NOP", "New Orleans Pelicans", "Pelicans", "New Orleans"),
  TeamInfo(1610612752, "NYK", "New York Knicks", "Knicks", "New York"),
  TeamInfo(1610612760, "OKC", "Oklahoma City Thunder", "Thunder", "Oklahoma City"),
  TeamInfo(1610612753, "ORL", "Orlando Magic", "Magic", "Orlando"),
  TeamInfo(1610612755, "PHI", "Philadelphia 76ers", "76ers", "Philadelphia"),
  TeamInfo(1610612756, "PHX", "Phoenix Suns", "Suns", "Phoenix"),
  TeamInfo(1610612757, "POR", "Portland Trail Blazers", "Trail Blazers", "Portland"),
  TeamInfo(1610612758, "SAC", "Sacramento Kings", "Kings", "Sacramento"),
  TeamInfo(1610612759, "SAS", "San Antonio Spurs", "Spurs", "San Antonio"),
  TeamInfo(1610612761, "TOR", "Toronto Raptors", "Raptors", "Toronto"),
  TeamInfo(1610612762, "UTA", "Utah Jazz", "Jazz", "Utah"),
  TeamInfo(1610612764, "WAS", "Washington Wizards", "Wizards", "Washington")
]
