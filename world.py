class Room:
    def __init__(self, name, desc):
        self.name = name
        self.desc = desc
        self.exits = {}

    def describe(self):
        exits = ', '.join(self.exits.keys())
        return f"{self.name}\n{self.desc}\nExits: {exits}"

class World:
    def __init__(self):
        self.rooms = {}
        self.create_world()

    def create_world(self):
        r1 = Room("Tavern", "A smokey tavern with drunken pirates.")
        r2 = Room("Docks", "Ships creak and waves crash at the docks.")
        r3 = Room("Jungle", "Dense trees and screechin’ monkeys surround ye.")

        r1.exits = {'east': 'docks'}
        r2.exits = {'west': 'tavern', 'south': 'jungle'}
        r3.exits = {'north': 'docks'}

        self.rooms['tavern'] = r1
        self.rooms['docks'] = r2
        self.rooms['jungle'] = r3

    def start_room(self):
        return self.rooms['tavern']
