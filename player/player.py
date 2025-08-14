import threading, time
from player.inventory import Inventory

class Player:
    def __init__(self, conn, addr, game):
        self.conn = conn
        self.addr = addr
        self.game = game
        self.name = f"{addr[0]}:{addr[1]}"
        self.room = game.world.start_room()
        self.inventory = Inventory()
        self._chopping = False
        self._chop_thread = None

    def send(self, msg):
        try:
            self.conn.sendall((msg + "\n").encode())
        except:
            pass

    def handle_input(self, text):
        text = text.lower().strip()
        if text in ['look', 'l']:
            return self.room.describe()
        elif text.startswith("pickup "):
            _, name = text.split(" ", 1)
            item = self.room.take_item(name)
            if not item:
                return f"There be no {name} here."
            msg = self.inventory.add_item(item["name"], item["weight"])
            if msg.startswith("Ye can't"):
                self.room.drop_item(item)
            return msg
        elif text in ['inventory', 'inv', 'i']:
            return self.inventory.list_items()
        elif text.startswith("drop "):
            _, name = text.split(" ", 1)
            for item in self.inventory.items:
                if item["name"] == name:
                    self.inventory.items.remove(item)
                    self.room.drop_item(item)
                    return f"Ye drop the {name}."
            return f"Ye don't have a {name}."
        elif text in ['north', 'south', 'east', 'west', 'n', 's' ,'e', 'w']:
            return self.move(text)
        elif text in ['chop tree']:
            return self.start_chopping()
        elif text in ['stop', 'stop chopping']:
            return self.stop_chopping()
        return "I don’t understand that, matey."

    def move(self, direction):
        next_room = self.room.exits.get(direction)
        if next_room:
            self.room = self.game.world.rooms[next_room]
            return self.room.describe()
        return "Ye can't go that way."

    def start_chopping(self):
        if "tree" not in self.room.features:
            return "There be no trees worth choppin’ here."
        if self._chopping:
            return "Ye are already choppin’!"
        self._chopping = True
        self._chop_thread = threading.Thread(target=self._chop_loop)
        self._chop_thread.start()
        return "Ye start choppin’ the tree…"

    def stop_chopping(self):
        if not self._chopping:
            return "Ye ain't choppin’ anything."
        self._chopping = False
        return "Ye stop choppin’."

    def _chop_loop(self):
        while self._chopping:
            msg = self.inventory.add_item("log", 3)
            self.send(msg)
            if msg.startswith("Ye can't"):  # inventory full
                self._chopping = False
                self.send("Ye inventory be full! Choppin’ stopped.")
                break
            time.sleep(2)  # chop interval in seconds
