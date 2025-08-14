import socket, threading
from player.player import Player
from game.engine import Game

HOST = '0.0.0.0'
PORT = 4000

game = Game()

TELNET_IAC = 255  # telnet "Interpret As Command" byte

def strip_telnet_control(data_bytes):
    result = bytearray()
    skip = 0
    for b in data_bytes:
        if skip > 0:
            skip -= 1
            continue
        if b == TELNET_IAC:
            skip = 2  # skip telnet command + option bytes
            continue
        result.append(b)
    return bytes(result)

def handle_client(conn, addr):
    player = Player(conn, addr, game)
    game.add_player(player)
    player.send("Welcome to the MUD, ye scallywag!\n")
    try:
        while True:
            raw = conn.recv(1024)
            if not raw:  # client closed connection
                break
            raw = strip_telnet_control(raw)
            if not raw:
                continue
            data = raw.decode(errors='ignore').strip()
            if data == "":
                # just a blank line, send nothing but keep connection
                continue
            if data in ("quit", "exit"):
                player.send("Fair winds to ye, matey!")
                break
            response = player.handle_input(data)
            if response:
                player.send(response)
    finally:
        game.remove_player(player)
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"MUD server runnin’ on {HOST}:{PORT}")
    try:
        while True:
            conn, addr = s.accept()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
    except KeyboardInterrupt:
        print("\nShutting down the server...")
        s.close()
