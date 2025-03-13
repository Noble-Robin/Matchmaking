# main.py
import tkinter as tk
from config import BOARD_SIZE, SQUARE_SIZE
from board import create_board
from pieces import load_piece_images
from move import on_square_click

# Initialiser la fenêtre Tkinter
root = tk.Tk()
root.title("Jeu d'Échecs")

# Créer un canevas pour dessiner l'échiquier
canvas = tk.Canvas(root, width=BOARD_SIZE * SQUARE_SIZE, height=BOARD_SIZE * SQUARE_SIZE)
canvas.pack()

# Charger les images des pièces
pieces = load_piece_images(BOARD_SIZE, SQUARE_SIZE)

# Créer l'échiquier et afficher les pièces
create_board(canvas, BOARD_SIZE, SQUARE_SIZE, pieces)

# Lier les clics de souris à la fonction on_square_click et envoyer create_board comme paramètre
canvas.bind("<Button-1>", lambda event: on_square_click(event, canvas, pieces, BOARD_SIZE, SQUARE_SIZE, create_board))

# Lancer l'application
root.mainloop()
