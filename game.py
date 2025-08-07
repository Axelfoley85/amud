from world import World

class Game:
    def __init__(self):
        self.world = World()
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def remove_player(self, player):
        if player in self.players:
            self.players.remove(player)
