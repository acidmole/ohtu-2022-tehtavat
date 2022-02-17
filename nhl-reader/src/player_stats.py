from player import Player
from player_reader import PlayerReader

class PlayerStats:

    def __init__(self, reader):
        self.players = reader.get_players()
    
    def top_scorers_by_nationality(self, nation):

        n_players = []

        for player in self.players:
            if player.nation == nation:
                n_players.append(player)

        n_players.sort(key=lambda x: x.points, reverse=True)
        
        return n_players