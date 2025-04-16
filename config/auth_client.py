import requests
import tkinter as tk
from tkinter import messagebox

def login_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    root.title("Connexion au Jeu d'Échecs")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")

    result = {}

    tk.Label(root, text="Connexion / Inscription", font=("Helvetica", 16, "bold"), bg="#2c3e50", fg="white").pack(pady=15)

    tk.Label(root, text="Nom d'utilisateur :", font=("Helvetica", 12), bg="#2c3e50", fg="white").pack()
    username_entry = tk.Entry(root, font=("Helvetica", 12))
    username_entry.pack(pady=5)

    tk.Label(root, text="Mot de passe :", font=("Helvetica", 12), bg="#2c3e50", fg="white").pack()
    password_entry = tk.Entry(root, show="*", font=("Helvetica", 12))
    password_entry.pack(pady=5)

    def do_connect():
        username = username_entry.get()
        password = password_entry.get()
        if not username or not password:
            messagebox.showwarning("Champs manquants", "Merci de remplir tous les champs.")
            return
        try:
            response = requests.post("https://b84b-80-70-37-74.ngrok-free.app/api/auth", json={
                "username": username,
                "password": password
            })
            if response.status_code == 200:
                data = response.json()
                result.update({
                    "id": data["id"],
                    "username": username,
                    "elo": data["elo"],
                    "guest": False
                })
                root.quit()
            else:
                messagebox.showerror("Erreur", response.json().get("error", "Erreur inconnue."))
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de se connecter : {e}")

    def play_guest():
        result.update({
            "id": None,
            "username": "Invité",
            "elo": 1200,
            "guest": True
        })
        root.quit()

    tk.Button(root, text="Connexion / Inscription", command=do_connect, bg="#3498db", fg="white", font=("Helvetica", 12)).pack(pady=10)
    tk.Button(root, text="Jouer en tant qu'invité", command=play_guest, bg="#95a5a6", fg="white", font=("Helvetica", 12)).pack(pady=5)

    root.mainloop()
    return result if result else None