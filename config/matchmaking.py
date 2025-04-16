import tkinter as tk
from tkinter import ttk, messagebox
import socketio
import subprocess

SERVER_URL = "https://b84b-80-70-37-74.ngrok-free.app"

sio = socketio.Client()

def start_matchmaking(root, on_error_callback, user_info):
    """Configure l'interface de matchmaking dans la fenêtre principale."""
    def join_queue():
        join_button.config(state=tk.DISABLED)
        status_label.config(text="En attente d'un adversaire...")
        try:
            sio.emit('join_queue', {
                "id": user_info["id"],
                "elo": user_info["elo"],
                "guest": user_info["guest"]
            })
        except Exception as e:
            status_label.config(text=f"Erreur lors de la tentative de rejoindre la file : {e}")
            join_button.config(state=tk.NORMAL)

    def on_match_found(data):
        status_label.config(text=f"Match trouvé !\nAdversaire: {data['opponent']}\nVotre couleur : {data['color']}")
        join_button.config(state=tk.NORMAL)
        subprocess.Popen(["python", "game/game.py", data['color']])

    # Supprime les widgets existants dans la fenêtre
    for widget in root.winfo_children():
        widget.destroy()

    # Configuration du style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 14), padding=10, background="#3498db", foreground="white")
    style.map("TButton", background=[("active", "#2980b9")])

    # Configure l'interface de matchmaking
    sio.on('match_found', on_match_found)
    try:
        sio.connect(SERVER_URL, headers={"ngrok-skip-browser-warning": "true"})
    except socketio.exceptions.ConnectionError as e:
        messagebox.showerror("Erreur de connexion", f"Impossible de se connecter au serveur : {e}")
        sio.disconnect()
        root.destroy()
        on_error_callback()
        return
    except Exception as e:
        messagebox.showerror("Erreur", f"Une erreur inattendue s'est produite : {e}")
        sio.disconnect()
        root.destroy()
        on_error_callback()
        return

    title_label = tk.Label(root, text="Matchmaking", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white")
    title_label.pack(pady=20)

    join_button = ttk.Button(root, text="Rejoindre la file d'attente", command=join_queue)
    join_button.pack(pady=20)

    status_label = tk.Label(root, text="Cliquez sur le bouton pour rejoindre.", font=("Helvetica", 12), bg="#2c3e50", fg="white")
    status_label.pack(pady=20)

    # Déconnecte le client Socket.IO à la fermeture de la fenêtre
    root.protocol("WM_DELETE_WINDOW", lambda: (sio.disconnect(), root.destroy()))