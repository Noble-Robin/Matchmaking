import tkinter as tk
from config.matchmaking import start_matchmaking

def show_menu():
    """Affiche le menu principal."""
    root = tk.Tk()
    root.title("Menu Principal")

    def switch_to_matchmaking():
        """Remplace le contenu de la fenêtre par l'interface de matchmaking."""
        for widget in root.winfo_children():
            widget.destroy()
        start_matchmaking(root)

    play_button = tk.Button(root, text="Jouer", command=switch_to_matchmaking)
    play_button.pack(pady=20)

    quit_button = tk.Button(root, text="Quitter", command=root.quit)
    quit_button.pack(pady=20)

    root.mainloop()