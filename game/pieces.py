### game/pieces.py

class Piece:
    def __init__(self, color):
        self.color = color
        self.has_moved = False

    def get_possible_moves(self, position, board):
        raise NotImplementedError("Cette méthode doit être implémentée par les sous-classes.")

class Pawn(Piece):
    def get_possible_moves(self, position, board):
        direction = -1 if self.color == "white" else 1
        moves = []
        row, col = position

        if board.is_empty(row + direction, col):
            moves.append((row + direction, col))
            start_row = 6 if self.color == "white" else 1
            if row == start_row and board.is_empty(row + 2 * direction, col):
                moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            target_row = row + direction
            target_col = col + dc
            if board.is_enemy(target_row, target_col, self.color):
                moves.append((target_row, target_col))
            elif board.en_passant_target == (target_row, target_col):
                moves.append((target_row, target_col))

        return moves

class Rook(Piece):
    def get_possible_moves(self, position, board):
        return board.get_linear_moves(position, self.color, directions=[(1, 0), (-1, 0), (0, 1), (0, -1)])

class Bishop(Piece):
    def get_possible_moves(self, position, board):
        return board.get_linear_moves(position, self.color, directions=[(1, 1), (-1, -1), (-1, 1), (1, -1)])

class Queen(Piece):
    def get_possible_moves(self, position, board):
        return board.get_linear_moves(position, self.color, directions=[
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (-1, -1), (-1, 1), (1, -1)
        ])

class Knight(Piece):
    def get_possible_moves(self, position, board):
        row, col = position
        offsets = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        moves = []
        for dr, dc in offsets:
            if board.is_within_bounds(row + dr, col + dc) and not board.is_ally(row + dr, col + dc, self.color):
                moves.append((row + dr, col + dc))
        return moves

class King(Piece):
    def get_possible_moves(self, position, board):
        row, col = position
        moves = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                if board.is_within_bounds(row + dr, col + dc) and not board.is_ally(row + dr, col + dc, self.color):
                    moves.append((row + dr, col + dc))

        # Roque
        if not self.has_moved and not board.is_in_check(self.color):
            row_roque = 7 if self.color == "white" else 0
            # Petit roque (côté roi)
            if isinstance(board.get_piece(row_roque, 7), Rook):
                rook = board.get_piece(row_roque, 7)
                if rook and not rook.has_moved:
                    if all(board.is_empty(row_roque, c) for c in [5, 6]):
                        if not board.is_in_check_path(self.color, [(row_roque, 5), (row_roque, 6)]):
                            moves.append((row_roque, 6))

            # Grand roque (côté dame)
            if isinstance(board.get_piece(row_roque, 0), Rook):
                rook = board.get_piece(row_roque, 0)
                if rook and not rook.has_moved:
                    if all(board.is_empty(row_roque, c) for c in [1, 2, 3]):
                        if not board.is_in_check_path(self.color, [(row_roque, 3), (row_roque, 2)]):
                            moves.append((row_roque, 2))

        return moves
