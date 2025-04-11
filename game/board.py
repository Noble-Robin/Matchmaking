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
    def __init__(self, player_color):
        self.player_color = player_color
        self.board = self.create_board(player_color)

    def create_board(self, player_color):
        """Crée l'échiquier avec les pièces placées initialement, en fonction de la couleur du joueur."""
        board = [[None] * 8 for _ in range(8)]

        # Déterminer les couleurs des joueurs
        opponent_color = 'white' if player_color == 'black' else 'black'

        # Placement des pièces du joueur (en bas)
        player_row, player_pawn_row = (7, 6) 
        board[player_row][0] = Rook(player_color)
        board[player_row][1] = Knight(player_color)
        board[player_row][2] = Bishop(player_color)
        board[player_row][3] = Queen(player_color)
        board[player_row][4] = King(player_color)
        board[player_row][5] = Bishop(player_color)
        board[player_row][6] = Knight(player_color)
        board[player_row][7] = Rook(player_color)
        for col in range(8):
            board[player_pawn_row][col] = Pawn(player_color)

        # Placement des pièces de l'adversaire (en haut)
        opponent_row, opponent_pawn_row = (0, 1)
        board[opponent_row][0] = Rook(opponent_color)
        board[opponent_row][1] = Knight(opponent_color)
        board[opponent_row][2] = Bishop(opponent_color)
        board[opponent_row][3] = Queen(opponent_color)
        board[opponent_row][4] = King(opponent_color)
        board[opponent_row][5] = Bishop(opponent_color)
        board[opponent_row][6] = Knight(opponent_color)
        board[opponent_row][7] = Rook(opponent_color)
        for col in range(8):
            board[opponent_pawn_row][col] = Pawn(opponent_color)

        return board

    def is_check(self, color):
        """Retourne True si le roi de la couleur donnée est en échec."""
        king_pos = None
        # Trouver la position du roi
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

    def is_checkmate(self, color):
        """Retourne True si le roi de la couleur donnée est en échec et mat."""
        # Vérifier si le roi est en échec
        if not self.is_check(color):
            return False

        # Trouver la position du roi
        king_pos = None
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if isinstance(piece, King) and piece.color == color:
                    king_pos = (row, col)
                    break
            if king_pos:
                break

        # Vérifier si le roi peut se déplacer pour sortir de l'échec
        possible_moves = King(color).get_moves(king_pos, self.board)
        for move in possible_moves:
            if not self.is_check_after_move(king_pos, move, color):
                return False

        # Vérifier si d'autres pièces peuvent intercepter l'attaque
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece.color == color:
                    if piece != self.board[king_pos[0]][king_pos[1]]:  # Ignorer le roi
                        piece_moves = piece.get_moves((row, col), self.board)
                        for move in piece_moves:
                            if not self.is_check_after_move((row, col), move, color):
                                return False

        return True

    def is_check_after_move(self, start_pos, end_pos, color):
        """Vérifie si le roi serait toujours en échec après un mouvement."""
        # Simuler le mouvement et vérifier si le roi serait en échec
        temp_board = self.clone_board()
        temp_board.move_piece(start_pos, end_pos)
        return temp_board.is_check(color)

    def clone_board(self):
        """Crée une copie de l'échiquier actuel pour simuler un mouvement."""
        new_board = ChessBoard()
        new_board.board = [row[:] for row in self.board]
        return new_board

    def move_piece(self, start_pos, end_pos):
        """Déplace une pièce de start_pos à end_pos."""
        piece = self.board[start_pos[0]][start_pos[1]]
        self.board[end_pos[0]][end_pos[1]] = piece
        self.board[start_pos[0]][start_pos[1]] = None
