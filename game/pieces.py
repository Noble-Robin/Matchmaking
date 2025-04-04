class Piece:
    def __init__(self, color):
        self.color = color  # 'white' ou 'black'

    def get_moves(self, position, board):
        """Méthode à redéfinir pour chaque pièce."""
        raise NotImplementedError("Cette méthode doit être implémentée dans les sous-classes")


class Pawn(Piece):
    def get_moves(self, position, board):
        moves = []
        row, col = position
        direction = -1 if self.color == 'white' else 1  # Blancs montent (-1), Noirs descendent (+1)

        # Avancer d'une case
        if board[row + direction][col] == ' ':
            moves.append((row + direction, col))

        # Prise en diagonale
        for dc in [-1, 1]:  
            new_col = col + dc
            if 0 <= new_col < 8 and board[row + direction][new_col] not in (' ', self.color):
                moves.append((row + direction, new_col))

        return moves


class Rook(Piece):
    def get_moves(self, position, board):
        moves = []
        row, col = position

        # Déplacements en ligne droite (horizontal et vertical)
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ' ':
                moves.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != self.color:
                moves.append((r, c))

        return moves


class Knight(Piece):
    def get_moves(self, position, board):
        moves = []
        row, col = position

        # Déplacements en L
        directions = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != self.color:
                moves.append((r, c))

        return moves


class Bishop(Piece):
    def get_moves(self, position, board):
        moves = []
        row, col = position

        # Déplacements en diagonale
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == ' ':
                moves.append((r, c))
                r, c = r + dr, c + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != self.color:
                moves.append((r, c))

        return moves


class Queen(Piece):
    def get_moves(self, position, board):
        # La dame combine les mouvements de la tour et du fou
        return Rook(self.color).get_moves(position, board) + Bishop(self.color).get_moves(position, board)


class King(Piece):
    def get_moves(self, position, board):
        moves = []
        row, col = position

        # Déplacements d'une case dans toutes les directions
        directions = [
            (1, 0), (-1, 0), (0, 1), (0, -1),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        for dr, dc in directions:
            r, c = row + dr, col + dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] != self.color:
                moves.append((r, c))

        return moves


# Test des pièces
if __name__ == "__main__":
    from board import ChessBoard

    chess = ChessBoard()
    rook = Rook('white')

    position = (7, 0)  # Exemple : tour en a1 (7e ligne, 0e colonne)
    moves = rook.get_moves(position, chess.board)
    print("Déplacements possibles de la tour :", moves)
