import tkinter as tk
from tkinter import ttk, messagebox
import socketio
import subprocess
import requests
import time

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
        def update_ui():
            try:
                if not data['opponent_guest']:
                    response = requests.get(f"{SERVER_URL}/api/user/{data['opponent']}")
                    if response.status_code == 200:
                        opponent_data = response.json()
                        opponent_info = f"{opponent_data['username']} (ELO: {opponent_data['elo']})"
                    else:
                        opponent_info = "Joueur inconnu"
                else:
                    opponent_info = "Invité"
            except Exception as e:
                opponent_info = f"Erreur de récupération : {e}"

            status_label.config(text=f"Match trouvé !\nAdversaire: {opponent_info}\nVotre couleur : {data['color']}")
            join_button.config(state=tk.NORMAL)
            
            time.sleep(1)
            
            subprocess.Popen(["python", "-m", "game.game", data['color'], data['gameId'], str(user_info["id"] or "")])

        root.after(0, update_ui)

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