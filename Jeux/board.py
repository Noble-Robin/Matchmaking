# board.py
import tkinter as tk

def create_board(canvas, board_size, square_size, pieces):
    """Fonction pour dessiner l'échiquier et afficher les pièces"""
    canvas.delete("all")  # Supprimer tous les éléments précédents sur le canevas
    
    # Dessiner les cases
    for row in range(board_size):
        for col in range(board_size):
            x1 = col * square_size
            y1 = row * square_size
            x2 = (col + 1) * square_size
            y2 = (row + 1) * square_size
            color = "white" if (row + col) % 2 == 0 else "grey"
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="grey")
            
            # Placer les pièces
            piece_key = get_piece_key(row, col)
            if piece_key in pieces:
                canvas.create_image(x1, y1, anchor=tk.NW, image=pieces[piece_key])

def get_piece_key(row, col):
    """Retourne la clé correspondant à la pièce à la position (row, col)"""
    if row == 1:
        return "black_pawn"  # Pions noirs
    elif row == 6:
        return "white_pawn"  # Pions blancs
    elif row == 0:
        if col == 0 or col == 7:
            return "black_rook"  # Tours noires
        elif col == 1 or col == 6:
            return "black_knight"  # Cavaliers noirs
        elif col == 2 or col == 5:
            return "black_bishop"  # Fous noirs
        elif col == 3:
            return "black_queen"  # Reine noire
        elif col == 4:
            return "black_king"  # Roi noir
    elif row == 7:
        if col == 0 or col == 7:
            return "white_rook"  # Tours blanches
        elif col == 1 or col == 6:
            return "white_knight"  # Cavaliers blancs
        elif col == 2 or col == 5:
            return "white_bishop"  # Fous blancs
        elif col == 3:
            return "white_queen"  # Reine blanche
        elif col == 4:
            return "white_king"  # Roi blanc
    return None
