# pieces.py
import os
from tkinter import PhotoImage

# Fonction pour charger les images des pièces
def load_piece_images(board_size, square_size):
    pieces = {}
    image_dir = "../pieces"  # Répertoire où sont stockées les images des pièces
    
    # Charger les images pour chaque type de pièce
    for piece in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
        for color in ["white", "black"]:
            image_path = os.path.join(image_dir, f"{color}_{piece}.png")
            if os.path.exists(image_path):
                img = PhotoImage(file=image_path)
                pieces[f"{color}_{piece}"] = img
            else:
                print(f"Image manquante: {image_path}")
    
    return pieces
