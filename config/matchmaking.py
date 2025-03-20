import tkinter as tk
import socketio

SERVER_URL = "https://17d6-80-70-37-74.ngrok-free.app"  

sio = socketio.Client()

def join_queue():
    status_label.config(text="En attente d'un adversaire...")
    sio.emit('join_queue')

def on_match_found(data):
    status_label.config(text=f"Match trouvé ! Adversaire: {data['opponent']}")

sio.on('match_found', on_match_found)

sio.connect(SERVER_URL, headers={"ngrok-skip-browser-warning": "true"})

root = tk.Tk()
root.title("Matchmaking Queue")

join_button = tk.Button(root, text="Rejoindre la file d'attente", command=join_queue)
join_button.pack(pady=20)

status_label = tk.Label(root, text="Cliquez sur le bouton pour rejoindre.")
status_label.pack(pady=20)

root.mainloop()

sio.disconnect()
