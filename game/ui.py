import pygame
import os
from board import ChessBoard

# Paramètres de la fenêtre
WIDTH, HEIGHT = 600, 600
SQUARE_SIZE = WIDTH // 8

# Couleurs
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)
HIGHLIGHT_COLOR = (255, 255, 0, 128)  # Jaune transparent pour la sélection

# Chargement des images des pièces
ASSETS_PATH = "assets/"
PIECE_IMAGES = {}

def load_piece_images():
    """Charge toutes les images des pièces"""
    pieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]
    colors = ["white", "black"]
    for color in colors:
        for piece in pieces:
            filename = f"{color}_{piece}.png"
            path = os.path.join(ASSETS_PATH, filename)
            if os.path.exists(path):
                image = pygame.image.load(path)
                PIECE_IMAGES[f"{color}_{piece}"] = pygame.transform.scale(image, (SQUARE_SIZE, SQUARE_SIZE))

class ChessUI:
    def __init__(self, player_color):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeu d'Échecs")
        self.player_color = player_color
        self.board = ChessBoard(player_color)
        self.selected_piece = None
        self.valid_moves = []
        self.running = True
        load_piece_images()

    def draw_board(self):
        """Dessine l'échiquier"""
        for row in range(8):
            for col in range(8):
                # Inverser les coordonnées si le joueur est noir
                display_row = 7 - row if self.player_color == 'black' else row
                display_col = 7 - col if self.player_color == 'black' else col

                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Met en surbrillance les cases valides
                if (row, col) in self.valid_moves:
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight_surface, (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE))

    def draw_pieces(self):
        """Affiche les pièces avec des images"""
        for row in range(8):
            for col in range(8):
                # Inverser les coordonnées si le joueur est noir
                display_row = 7 - row if self.board.player_color == 'black' else row
                display_col = 7 - col if self.board.player_color == 'black' else col

                piece = self.board.board[row][col]
                if piece:
                    piece_name = f"{piece.color}_{type(piece).__name__.lower()}"
                    if piece_name in PIECE_IMAGES:
                        self.screen.blit(PIECE_IMAGES[piece_name], (display_col * SQUARE_SIZE, display_row * SQUARE_SIZE))

    def handle_click(self, pos):
        """Gère le clic de la souris"""
        col, row = pos[0] // SQUARE_SIZE, pos[1] // SQUARE_SIZE

        # Inverser les coordonnées si le joueur est noir
        actual_row = 7 - row if self.board.player_color == 'black' else row
        actual_col = 7 - col if self.board.player_color == 'black' else col

        if self.selected_piece is None:
            # Sélection d'une pièce
            piece = self.board.board[actual_row][actual_col]
            if piece and piece.color == self.board.player_color:  # Vérifier que la pièce appartient au joueur
                self.selected_piece = (actual_row, actual_col)
                self.valid_moves = piece.get_moves((actual_row, actual_col), self.board.board)  # Obtenir les déplacements possibles
        else:
            # Déplacement ou prise
            if (actual_row, actual_col) in self.valid_moves:
                self.board.move_piece(self.selected_piece, (actual_row, actual_col))

            # Réinitialiser la sélection après le déplacement
            self.selected_piece = None
            self.valid_moves = []


    def run(self):
        """Boucle principale du jeu"""
        while self.running:
            self.screen.fill((0, 0, 0))
            self.draw_board()
            self.draw_pieces()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)

            pygame.display.flip()

        pygame.quit()


# Lancer l'interface graphique
if __name__ == "__main__":
    ChessUI().run()
