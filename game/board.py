### game/board.py

from pieces import *

class Board:
    def __init__(self):
        self.en_passant_target = None
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup_pieces()

    def setup_pieces(self):
        for col in range(8):
            self.grid[1][col] = Pawn("black")
            self.grid[6][col] = Pawn("white")

        order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_cls in enumerate(order):
            self.grid[0][col] = piece_cls("black")
            self.grid[7][col] = piece_cls("white")

    def get_piece(self, row, col):
        return self.grid[row][col] if self.is_within_bounds(row, col) else None

    def move_piece(self, start_pos, end_pos):
        piece = self.get_piece(*start_pos)
        target = self.get_piece(*end_pos)
        if piece:
            # Roque : déplace aussi la tour
            if isinstance(piece, King) and abs(start_pos[1] - end_pos[1]) == 2:
                row = start_pos[0]
                if end_pos[1] == 6:
                    rook = self.get_piece(row, 7)
                    self.grid[row][5] = rook
                    self.grid[row][7] = None
                    rook.has_moved = True
                elif end_pos[1] == 2:
                    rook = self.get_piece(row, 0)
                    self.grid[row][3] = rook
                    self.grid[row][0] = None
                    rook.has_moved = True

            # Prise en passant
            if isinstance(piece, Pawn):
                if self.en_passant_target and end_pos == self.en_passant_target:
                    self.grid[start_pos[0]][end_pos[1]] = None

                # Mise à jour de en_passant_target si le pion avance de deux cases
                if abs(start_pos[0] - end_pos[0]) == 2:
                    mid_row = (start_pos[0] + end_pos[0]) // 2
                    self.en_passant_target = (mid_row, start_pos[1])
                else:
                    self.en_passant_target = None
            else:
                self.en_passant_target = None

            self.grid[end_pos[0]][end_pos[1]] = piece
            self.grid[start_pos[0]][start_pos[1]] = None
            piece.has_moved = True

    def is_empty(self, row, col):
        return self.is_within_bounds(row, col) and self.grid[row][col] is None

    def is_enemy(self, row, col, color):
        return self.is_within_bounds(row, col) and self.grid[row][col] is not None and self.grid[row][col].color != color

    def is_ally(self, row, col, color):
        return self.is_within_bounds(row, col) and self.grid[row][col] is not None and self.grid[row][col].color == color

    def is_within_bounds(self, row, col):
        return 0 <= row < 8 and 0 <= col < 8

    def get_linear_moves(self, position, color, directions):
        row, col = position
        moves = []
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while self.is_within_bounds(r, c):
                if self.is_empty(r, c):
                    moves.append((r, c))
                elif self.is_enemy(r, c, color):
                    moves.append((r, c))
                    break
                else:
                    break
                r += dr
                c += dc
        return moves

    def is_in_check(self, color):
        king_pos = None
        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and isinstance(piece, King) and piece.color == color:
                    king_pos = (r, c)
                    break
            if king_pos:
                break

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and piece.color != color and not isinstance(piece, King):
                    if king_pos in piece.get_possible_moves((r, c), self):
                        return True
        return False

    def is_in_check_path(self, color, positions):
        for pos in positions:
            row, col = pos
            for r in range(8):
                for c in range(8):
                    piece = self.get_piece(r, c)
                    if piece and piece.color != color:
                        if (row, col) in piece.get_possible_moves((r, c), self):
                            return True
        return False
