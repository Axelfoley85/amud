import socket, threading
from player import Player
from game import Game

HOST = '0.0.0.0'
PORT = 4000

game = Game()

def handle_client(conn, addr):
    player = Player(conn, addr, game)
    game.add_player(player)
    player.send("Welcome to the MUD, ye scallywag!\n")
    try:
        while True:
            data = conn.recv(1024).decode().strip()
            if not data:
                break
            response = player.handle_input(data)
            if response:
                player.send(response)
    finally:
        game.remove_player(player)
        conn.close()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    print(f"MUD server runnin’ on {HOST}:{PORT}")
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
