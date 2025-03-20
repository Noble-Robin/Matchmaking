class Piece:
    """Classe de base pour toutes les pièces."""
    def __init__(self, color):
        self.color = color

    def get_moves(self, position, board):
        """Retourne les déplacements possibles d'une pièce."""
        raise NotImplementedError

class King(Piece):
    """Classe pour le roi."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board[r][c]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((r, c))
        return moves

class Queen(Piece):
    """Classe pour la reine."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                target_piece = board[r][c]
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

class Rook(Piece):
    """Classe pour la tour."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                target_piece = board[r][c]
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

class Bishop(Piece):
    """Classe pour le fou."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            r, c = row, col
            while 0 <= r + dr < 8 and 0 <= c + dc < 8:
                r += dr
                c += dc
                target_piece = board[r][c]
                if target_piece is None:
                    moves.append((r, c))
                elif target_piece.color != self.color:
                    moves.append((r, c))
                    break
                else:
                    break
        return moves

class Knight(Piece):
    """Classe pour le cavalier."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        directions = [(-2, -1), (-1, -2), (1, -2), (2, -1), (2, 1), (1, 2), (-1, 2), (-2, 1)]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board[r][c]
                if target_piece is None or target_piece.color != self.color:
                    moves.append((r, c))
        return moves

class Pawn(Piece):
    """Classe pour le pion."""
    def get_moves(self, position, board):
        row, col = position
        moves = []
        direction = -1 if self.color == 'white' else 1
        if 0 <= row + direction < 8:
            if board[row + direction][col] is None:
                moves.append((row + direction, col))
                if (row == 1 and self.color == 'white') or (row == 6 and self.color == 'black'):
                    if board[row + 2 * direction][col] is None:
                        moves.append((row + 2 * direction, col))

        for dc in [-1, 1]:
            r, c = row + direction, col + dc
            if 0 <= r < 8 and 0 <= c < 8:
                target_piece = board[r][c]
                if target_piece and target_piece.color != self.color:
                    moves.append((r, c))

        return moves

class ChessBoard:
    """Classe représentant l'échiquier."""
    def __init__(self):
        # Initialisation de l'échiquier avec les pièces
        self.board = [
            [Rook('black'), Knight('black'), Bishop('black'), Queen('black'), King('black'), Bishop('black'), Knight('black'), Rook('black')],
            [Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black'), Pawn('black')],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white'), Pawn('white')],
            [Rook('white'), Knight('white'), Bishop('white'), Queen('white'), King('white'), Bishop('white'), Knight('white'), Rook('white')],
        ]

    def move_piece(self, start, end):
        """Déplace une pièce de start à end."""
        piece = self.board[start[0]][start[1]]
        self.board[end[0]][end[1]] = piece
        self.board[start[0]][start[1]] = None

    def is_in_check(self, color):
        """Vérifie si le roi d'une couleur est en échec"""
        king_position = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color and isinstance(piece, King):
                    king_position = (row, col)
                    break

        if not king_position:
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    possible_moves = piece.get_moves((row, col), self.board)
                    if king_position in possible_moves:
                        return True

        return False

    def is_checkmate(self, color):
        """Vérifie si le joueur est en échec et mat"""
        if not self.is_in_check(color):
            return False

        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    possible_moves = piece.get_moves((row, col), self.board)
                    for move in possible_moves:
                        original_piece = self.board[move[0]][move[1]]
                        self.board[move[0]][move[1]] = piece
                        self.board[row][col] = None
                        in_check = self.is_in_check(color)

                        self.board[row][col] = piece
                        self.board[move[0]][move[1]] = original_piece

                        if not in_check:
                            return False

        return True
    
    def is_check(self, color):
        """Retourne True si le roi de la couleur donnée est en échec."""
        # Trouver le roi de la couleur donnée
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        # Vérifier si une pièce ennemie peut attaquer le roi
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color != color:
                    if (row, col) in piece.get_moves((row, col), self.board):
                        return True
        return False
