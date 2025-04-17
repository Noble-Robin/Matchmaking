import tkinter as tk
from tkinter import ttk
from config.auth_client import login_menu
from config.matchmaking import start_matchmaking

def show_menu():
    """Affiche le menu principal"""
    root = tk.Tk()
    root.title("Menu Principal")
    root.geometry("400x300")
    root.configure(bg="#2c3e50")

    # Configuration du style
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=("Helvetica", 14), padding=10, background="#3498db", foreground="white")
    style.map("TButton", background=[("active", "#2980b9")])

    def handle_login():
        def on_success(user_info):
            start_matchmaking(root, show_menu, user_info)
        login_menu(root, on_success)

    def draw_main_menu():
        for widget in root.winfo_children():
            widget.destroy()

        # Titre
        title_label = tk.Label(root, text="Menu Principal", font=("Helvetica", 18, "bold"), bg="#2c3e50", fg="white")
        title_label.pack(pady=20)

        # Boutons
        play_button = ttk.Button(root, text="Jouer", command=handle_login)
        play_button.pack(pady=10)

        quit_button = ttk.Button(root, text="Quitter", command=root.quit)
        quit_button.pack(pady=10)

    draw_main_menu()
    root.mainloop()