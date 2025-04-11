import sys
import pygame
from board import ChessBoard, King, Queen, Rook, Bishop, Knight, Pawn

# Paramètres
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
SQUARE_SIZE = SCREEN_WIDTH // 8
WHITE = (255, 255, 255)
BLACK = (0, 120, 0)

# Initialisation de pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jeu d'Échecs")

# Classe pour gérer l'UI du jeu
class Game:
    def __init__(self, player_color):
        self.board = ChessBoard(player_color)
        self.selected_piece = None
        self.valid_moves = []
        self.current_player = "white"

    def draw_board(self):
        """Dessine l'échiquier sur l'écran."""
        for row in range(8):
            for col in range(8):
                # Déterminer la couleur de la case
                color = WHITE if (row + col) % 2 == 0 else BLACK
                # Dessiner la case
                pygame.draw.rect(screen, color, pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    
                # Si la pièce sélectionnée est sur cette case, dessiner un rectangle bleu clair autour de la case
                if self.selected_piece == (row, col):
                    pygame.draw.rect(screen, (173, 216, 230), pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)
    
                # Si le roi est en échec, dessiner la case du roi en rouge
                if isinstance(self.board.board[row][col], King):
                    king = self.board.board[row][col]
                    if self.board.is_check(king.color):  # Vérifier si le roi est en échec
                        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

    def draw_pieces(self):
        """Dessine toutes les pièces sur l'échiquier."""
        for row in range(8):
            for col in range(8):
                piece = self.board.board[row][col]
                if piece:
                    self.draw_piece(piece, row, col)

    def draw_piece(self, piece, row, col):
        """Dessine une pièce spécifique à une position donnée."""
        piece_image = pygame.image.load(f"game/assets/{piece.color}_{type(piece).__name__.lower()}.png")
        piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
        screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    def handle_click(self, pos):
        """Gère le clic de la souris."""
        row, col = pos[1] // SQUARE_SIZE, pos[0] // SQUARE_SIZE

        # Si une pièce est déjà sélectionnée
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                # Déplacer la pièce
                self.board.move_piece(self.selected_piece, (row, col))
                self.switch_turn()  # Changer de joueur après chaque mouvement
                self.selected_piece = None
                self.valid_moves = []
            else:
                # Deselect the current piece if clicked again
                piece = self.board.board[row][col]
                if piece and piece.color == self.current_player:
                    self.selected_piece = (row, col)
                    self.valid_moves = piece.get_moves((row, col), self.board.board)
                else:
                    self.selected_piece = None
                    self.valid_moves = []
        else:
            # Aucune pièce sélectionnée, essayer de sélectionner une nouvelle pièce
            piece = self.board.board[row][col]
            if piece and piece.color == self.current_player:
                self.selected_piece = (row, col)
                self.valid_moves = piece.get_moves((row, col), self.board.board)
            else:
                self.selected_piece = None
                self.valid_moves = []

    def switch_turn(self):
        """Change de joueur après chaque tour."""
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'

    def game_loop(self):
        """Boucle principale du jeu."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.handle_click(pos)

            # Dessiner le jeu
            self.draw_board()
            self.draw_pieces()

            # Afficher le joueur actuel
            font = pygame.font.Font(None, 36)
            text = font.render(f"Tour: {self.current_player.capitalize()}", True, (255, 0, 0))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 20))

            pygame.display.flip()

        pygame.quit()

if __name__ == "__main__":
    player_color = sys.argv[1] if len(sys.argv) > 1 else 'white'
    game = Game(player_color)
    game.game_loop()
