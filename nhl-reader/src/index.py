import requests
from player import Player

def main():
    url = "https://nhlstatisticsforohtu.herokuapp.com/players"
    response = requests.get(url).json()

    #print("JSON-muotoinen vastaus:")
    #print(response)

    players = []

    for player_dict in response:
        player = Player(
            player_dict['name'], player_dict['nationality'], player_dict['games'], player_dict['team'], player_dict['goals'], player_dict['assists'],
            player_dict['penalties']
       )

        players.append(player)

    print("Suomalaiset:")

    finns = []
    for player in players:
        if player.nation == 'FIN':
            finns.append(player)

    finns.sort(key=lambda x: x.points, reverse=True)

    for player in finns:
        print(player)

    #def takeNation(player):
    #    return player.nation
    
if __name__ == "__main__":
    main()
