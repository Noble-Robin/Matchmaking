import socketio
from config.matchmaking import SERVER_URL

sio = socketio.Client()
try:
    sio.connect(SERVER_URL, headers={"ngrok-skip-browser-warning": "true"})
    print("[socket_client] Connecté au serveur Socket.IO")
except Exception as e:
    print("[socket_client] Erreur de connexion :", e)

# Événement à connecter depuis le jeu
game_handler = {
    "on_opponent_move": lambda data: None
}

@sio.on("opponent_move")
def handle_opponent_move(data):
    if game_handler["on_opponent_move"]:
        game_handler["on_opponent_move"](data)
