class Player:
    def __init__(self, conn, addr, game):
        self.conn = conn
        self.addr = addr
        self.game = game
        self.name = f"{addr[0]}:{addr[1]}"
        self.room = game.world.start_room()

    def send(self, msg):
        try:
            self.conn.sendall((msg + "\n").encode())
        except:
            pass

    def handle_input(self, text):
        text = text.lower()
        if text in ['look', 'l']:
            return self.room.describe()
        elif text in ['north', 'south', 'east', 'west']:
            return self.move(text)
        return "I don’t understand that, matey."

    def move(self, direction):
        next_room = self.room.exits.get(direction)
        if next_room:
            self.room = self.game.world.rooms[next_room]
            return self.room.describe()
        return "Ye can't go that way."
