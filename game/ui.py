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
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Jeu d'Échecs")
        self.board = ChessBoard()
        self.selected_piece = None
        self.valid_moves = []
        self.running = True
        load_piece_images()

    def draw_board(self):
        """Dessine l'échiquier"""
        for row in range(8):
            for col in range(8):
                color = WHITE if (row + col) % 2 == 0 else BLACK
                pygame.draw.rect(self.screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

                # Met en surbrillance les cases valides
                if (row, col) in self.valid_moves:
                    highlight_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                    highlight_surface.fill(HIGHLIGHT_COLOR)
                    self.screen.blit(highlight_surface, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def draw_pieces(self):
        """Affiche les pièces avec des images"""
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    piece_name = f"{piece.color}_{type(piece).__name__.lower()}"
                    if piece_name in PIECE_IMAGES:
                        self.screen.blit(PIECE_IMAGES[piece_name], (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def handle_click(self, pos):
        """Gère le clic de la souris"""
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

        if self.selected_piece is None:
            # Sélection d'une pièce
            piece = self.board.board[row][col]
            if piece:
                self.selected_piece = (row, col)
                self.valid_moves = piece.get_moves((row, col), self.board.board)  # Obtenir les déplacements possibles
        else:
            # Déplacement ou prise
            if (row, col) in self.valid_moves:
                target_piece = self.board.board[row][col]
                if target_piece:
                    if target_piece.color != self.board.board[self.selected_piece[0]][self.selected_piece[1]].color:
                        # Capture d'une pièce ennemie
                        print(f"{target_piece.color} {type(target_piece).__name__} capturé !")

            self.board.move_piece(self.selected_piece, (row, col))

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
