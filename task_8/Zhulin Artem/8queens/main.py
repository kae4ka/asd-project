class ChessPiece:
    def __init__(self, row: int, col: int):
        """
        Represents a chess piece
        """
        self.row = row
        self.col = col

    def conflicts_with(self, row: int, col: int) -> bool:
        """
        Checks if this piece threatens the given position
        """
        pass

    def get_symbol(self) -> str:
        """
        Returns the symbol of this piece
        """
        pass


class Queen(ChessPiece):
    def __init__(self, row, col):
        """
        Represents a queen on the board.
        """
        super().__init__(row, col)

    def conflicts_with(self, row: int, col: int) -> bool:
        return self.row == row or self.col == col or abs(self.row - row) == abs(self.col - col)

    def get_symbol(self) -> str:
        return 'Q'


class Board:
    def __init__(self, size=8):
        """
        Represents the chessboard.
        """
        self.size = size
        self.chess_pieces = []

    def position_is_safe(self, new_piece: ChessPiece) -> bool:
        """
        Checks if placing a piece at board in chosen place is safe.
        """
        for piece in self.chess_pieces:
            if new_piece.conflicts_with(piece.row, piece.col) or piece.conflicts_with(new_piece.row, new_piece.col):
                return False
        return True

    def place_piece(self, piece: ChessPiece):
        """
        Places a queen at the specified position.
        """
        self.chess_pieces.append(piece)

    def remove_piece_at(self, row, col):
        """
        Removes a piece from the specified position.
        """
        self.chess_pieces = [piece for piece in self.chess_pieces if not (piece.row == row and piece.col == col)]

    def clear(self):
        self.chess_pieces = []

    def print_board(self):
        """
        Prints the current state of the board.
        """
        lines = [['.' for _ in range(self.size)] for _ in range(self.size)]

        for piece in self.chess_pieces:
            lines[piece.row][piece.col] = piece.get_symbol()

        for line in lines:
            print(' '.join(line))


class QueenSolver:
    def __init__(self, board):
        """
        Solves the queen problem.
        """
        self.board = board
        self.solutions = []

    def solve(self, col=0):
        """
        Method to solve the problem using backtracking.
        """
        if col >= self.board.size:
            self.solutions.append([queen for queen in self.board.chess_pieces])
            return
        for row in range(self.board.size):
            queen = Queen(row, col)
            if self.board.position_is_safe(queen):
                self.board.place_piece(queen)
                self.solve(col + 1)
                self.board.remove_piece_at(queen.row, queen.col)

    def print_solutions(self):
        print(f"Found {len(self.solutions)} solutions.")
        for index, solution in enumerate(self.solutions, 1):
            print(f"Solution #{index}:")
            self.board.clear()
            for piece in solution:
                self.board.place_piece(piece)
            self.board.print_board()
            print("\n")


def main():
    board = Board(size=8)
    solver = QueenSolver(board)
    solver.solve()
    solver.print_solutions()


if __name__ == "__main__":
    main()
