# move.py
from board import get_piece_key  # Importer uniquement get_piece_key

# Variables globales pour suivre l'état du jeu
selected_piece = None
selected_pos = None

def on_square_click(event, canvas, pieces, board_size, square_size, create_board):
    """Gère les clics sur les cases de l'échiquier"""
    global selected_piece, selected_pos  # Déclarer selected_piece comme globale
    
    # Calculer la ligne et la colonne du clic
    col = event.x // square_size
    row = event.y // square_size
    
    # Si une pièce est sélectionnée, la déplacer
    if selected_piece:
        move_piece(row, col, canvas, pieces, square_size, create_board)
        selected_piece = None  # Désélectionner la pièce après le déplacement
    else:
        # Sélectionner une pièce si une case est cliquée
        selected_piece = get_piece_key(row, col)
        selected_pos = (row, col)
        print(f"Pièce sélectionnée : {selected_piece} à la position ({row}, {col})")

    # Recréer l'échiquier avec les pièces mises à jour
    create_board(canvas, board_size, square_size, pieces)


def move_piece(row, col, canvas, pieces, square_size, create_board):
    """Déplace la pièce sélectionnée à la nouvelle position"""
    global selected_piece, selected_pos  # Déclarer selected_piece comme globale
    
    # Vérifier si une pièce est bien sélectionnée
    if not selected_piece:
        return
    
    # Calculer la nouvelle clé de la pièce à déplacer
    piece_key = selected_piece
    if piece_key in pieces:
        # Mettre à jour la position de la pièce sur l'échiquier
        pieces[piece_key] = (row, col)
    
    # Recréer l'échiquier avec les pièces mises à jour
    create_board(canvas, pieces, square_size)  # Passer canvas, pieces, square_size correctement

    # Réinitialiser la position de sélection après le déplacement
    selected_pos = None
    selected_piece = None

