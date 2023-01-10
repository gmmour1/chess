from enum import Enum
import copy
from math import factorial


Piece = Enum('Piece', ['Q', 'K', 'B', 'R', 'N'])


class Board:
    def __init__(self, x, y):
        self._x = x
        self._y = y
        self._board = [[0 for i in range(y)] for i in range(x)]

    def copy(self):
        new_board = Board(self._x, self._y)
        new_board._board = copy.deepcopy(self._board)
        return new_board

    def cells(self):
        for i in range(self._x):
            for j in range(self._y):
                yield i, j

    def in_board(self, x, y):
        return (x in range(self._x)) and (y in range(self._y))

    def place_piece(self, piece, x, y):
        expand_piece_fns = {
            Piece.Q: self._place_queen,
            Piece.K: self._place_king,
            Piece.R: self._place_rook,
            Piece.B: self._place_bishop,
            Piece.N: self._place_knight,
        }
        if self._board[x][y] != 0:
            return False
        old_board = self.copy()
        if expand_piece_fns[piece](x, y):
            self._update_board()
            self._board[x][y] = 2
            return True
        else:
            self._board = old_board._board
            return False

    def _update_board(self):
        for i in range(self._x):
            for j in range(self._y):
                if self._board[i][j] == -1:
                    self._board[i][j] = 1

    def _place_queen(self, x, y):
        r = self._place_rook(x, y)
        if not r:
            return False
        b = self._place_bishop(x, y)
        return r and b

    def _place_rook(self, x, y):
        steps = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        return self.place_iterative_piece(steps, x, y)

    def _place_bishop(self, x, y):
        steps = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        return self.place_iterative_piece(steps, x, y)

    def place_iterative_piece(self, steps, x, y):
        for step in steps:
            a = step[0]
            b = step[1]
            for n in range(max([self._x, self._y])):
                i = x + (a * n)
                j = y + (b * n)
                if not self.in_board(i, j):
                    break
                if self._board[i][j] > 1:
                    return False
                self._board[i][j] = -1
        return True

    def _place_king(self, x, y):
        moves = [(-1, -1), (-1, 0), (-1, 1), (0, -1),
                 (0, 1), (1, -1), (1, 0), (1, 1)]
        return self._place_simple_piece(moves, x, y)

    def _place_knight(self, x, y):
        moves = [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                 (2, -1), (1, -2), (2, 1), (1, 2)]
        return self._place_simple_piece(moves, x, y)

    def _place_simple_piece(self, moves, x, y):
        for move in moves:
            i = x + move[0]
            j = y + move[1]
            if self.in_board(i, j):
                if self._board[i][j] > 1:
                    return False
                self._board[i][j] = -1
        return True


def calculate_layouts(x, y, k=0, q=0, b=0, r=0, n=0):
    board = Board(x, y)
    pieces = expand_pieces(b, k, n, q, r)
    permutations = place(board, pieces)
    denominator = factorial(k)*factorial(q) * \
        factorial(b)*factorial(r)*factorial(n)
    return permutations/denominator


def expand_pieces(b, k, n, q, r):
    pieces = []
    pieces.extend([Piece.Q for _ in range(q)])
    pieces.extend([Piece.R for _ in range(r)])
    pieces.extend([Piece.B for _ in range(b)])
    pieces.extend([Piece.N for _ in range(n)])
    pieces.extend([Piece.K for _ in range(k)])
    return pieces


def place(board, pieces):
    if len(pieces) > 1:
        permutations = 0
        piece = pieces[0]
        for x, y in board.cells():
            new_board = board.copy()
            if new_board.place_piece(piece, x, y):
                permutations += place(new_board, pieces[1:])
        return permutations
    elif len(pieces) == 1:
        permutations = 0
        piece = pieces[0]
        for x, y in board.cells():
            new_board = board.copy()
            if new_board.place_piece(piece, x, y):
                permutations += 1
        return permutations
    else:
        return 0


if __name__ == '__main__':
    val1 = calculate_layouts(3, 3, k=2, r=1)
    print(val1)

    val1 = calculate_layouts(4, 4, n=4, r=2)
    print(val1)
    #val1 = calculate_layouts(6, 9, q=1, k=2, b=1, r=1, n=1)
    # 20136752
