import tkinter as tk
from tkinter import ttk
from config.matchmaking import start_matchmaking

def show_menu():
    """Affiche le menu principal avec un style modernisé."""
    root = tk.Tk()
    root.title("Menu Principal")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")  # Couleur de fond

    # Configuration du style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 14), padding=10, background="#3498db", foreground="white")
    style.map("TButton", background=[("active", "#2980b9")])

    def switch_to_matchmaking():
        """Remplace le contenu de la fenêtre par l'interface de matchmaking."""
        for widget in root.winfo_children():
            widget.destroy()
        start_matchmaking(root, show_menu)

    # Titre
    title_label = tk.Label(root, text="Menu Principal", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white")
    title_label.pack(pady=20)

    # Boutons
    play_button = ttk.Button(root, text="Jouer", command=switch_to_matchmaking)
    play_button.pack(pady=10)

    quit_button = ttk.Button(root, text="Quitter", command=root.quit)
    quit_button.pack(pady=10)

    root.mainloop()