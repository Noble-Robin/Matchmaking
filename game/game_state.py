### game/game_state.py

from board import Board
from pieces import Queen, Rook, Bishop, Knight
import copy

class GameState:
    def __init__(self):
        self.board = Board()
        self.current_turn = "white"
        self.move_history = []
        self.winner = None

    def get_valid_moves(self, row, col):
        piece = self.board.get_piece(row, col)
        if piece and piece.color == self.current_turn:
            possible_moves = piece.get_possible_moves((row, col), self.board)
            return [move for move in possible_moves if self.is_move_safe((row, col), move)]
        return []

    def is_move_safe(self, start_pos, end_pos):
        test_board = copy.deepcopy(self.board)
        piece = test_board.get_piece(*start_pos)
        test_board.move_piece(start_pos, end_pos)
        return not test_board.is_in_check(piece.color)

    def has_any_valid_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece(row, col)
                if piece and piece.color == self.current_turn:
                    if self.get_valid_moves(row, col):
                        return True
        return False

    def is_game_over(self):
        if not self.has_any_valid_moves():
            if self.board.is_in_check(self.current_turn):
                self.winner = "black" if self.current_turn == "white" else "white"
            else:
                self.winner = "draw"
            return True
        return False

    def play_move(self, start_pos, end_pos):
        valid_moves = self.get_valid_moves(*start_pos)
        if end_pos in valid_moves:
            self.board.move_piece(start_pos, end_pos)
            self.move_history.append((start_pos, end_pos))

            piece = self.board.get_piece(*end_pos)
            promotion_pos = None
            if piece and piece.__class__.__name__ == "Pawn":
                if (piece.color == "white" and end_pos[0] == 0) or (piece.color == "black" and end_pos[0] == 7):
                    promotion_pos = end_pos

            # Inverse le tour ici après tout traitement
            self.current_turn = "black" if self.current_turn == "white" else "white"
            return True, promotion_pos
        return False, None

    def promote_pawn(self, position, choice):
        print(f"[PROMOTION] Promotion en {choice} pour {self.board.get_piece(*position).color}")
        row, col = position
        color = self.board.get_piece(row, col).color
        piece_map = {
            "queen": Queen,
            "rook": Rook,
            "bishop": Bishop,
            "knight": Knight
        }
        if choice in piece_map:
            self.board.grid[row][col] = piece_map[choice](color)

        # Ne pas changer le tour ici — il est déjà changé dans play_move