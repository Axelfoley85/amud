from world.room import Room

class World:
    def __init__(self):
        self.rooms = {}
        self.create_world()

    def create_world(self):
        r1 = Room("Tavern", "A smokey tavern with drunken pirates.",
                  items=[{"name": "tankard", "weight": 1},
                         {"name": "tent", "weight": 3}])
        r2 = Room("Docks", "Ships creak and waves crash at the docks.",
                  items=[{"name": "rope", "weight": 2}])
        r3 = Room("Jungle", "Dense trees and screechin’ monkeys surround ye.",
                  items=[{"name": "banana", "weight": 1}],
                  features=["tree"])  # tree is not pick-up-able

        r1.exits = {'east': 'docks'}
        r2.exits = {'west': 'tavern', 'south': 'jungle'}
        r3.exits = {'north': 'docks'}

        self.rooms['tavern'] = r1
        self.rooms['docks'] = r2
        self.rooms['jungle'] = r3

    def start_room(self):
        return self.rooms['tavern']
