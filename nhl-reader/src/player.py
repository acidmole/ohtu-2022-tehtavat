class Player:
    def __init__(self, name, nation, games, team, goals, assists, penalties):
        self.name = name
        self.nation = nation
        self.team = team
        self.goals = goals
        self.assists = assists
        self.penalties = penalties
        self.games = games
        self.points = goals + assists
    
    def __str__(self):
        potko = f"{self.name:20} {self.team}, {str(self.goals):2} + {str(self.assists):2} = {str(self.points):3}"
        return potko
