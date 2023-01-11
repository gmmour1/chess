from enum import Enum
import copy
from math import factorial


class Piece(Enum):
    Queen = 0
    King = 1
    Bishop = 2
    Rook = 3
    Knight = 4

    def moves(self):
        piece_moves = {
            self.Queen: [(1, 0), (-1, 0), (0, 1), (0, -1),
                         (1, 1), (-1, -1), (1, -1), (-1, 1)],
            self.King: [(1, 0), (-1, 0), (0, 1), (0, -1),
                        (1, 1), (-1, -1), (1, -1), (-1, 1)],
            self.Rook: [(1, 0), (-1, 0), (0, 1), (0, -1)],
            self.Bishop: [(1, 1), (-1, -1), (1, -1), (-1, 1)],
            self.Knight: [(-2, -1), (-1, -2), (-2, 1), (-1, 2),
                          (2, -1), (1, -2), (2, 1), (1, 2)],
        }
        return piece_moves[self]

    def iterative(self):
        piece_iterative = {
            self.Queen: True,
            self.King: False,
            self.Rook: True,
            self.Bishop: True,
            self.Knight: False,
        }
        return piece_iterative[self]


class Board:
    def __init__(self, x: int, y: int):
        self._x = x
        self._y = y
        self._board = [[0 for i in range(y)] for i in range(x)]

    def copy(self):
        new_board = Board(self._x, self._y)
        new_board._board = copy.deepcopy(self._board)
        return new_board

    def square_coordinates(self):
        for i in range(self._x):
            for j in range(self._y):
                yield i, j

    def _in_board(self, x, y) -> bool:
        return (x in range(self._x)) and (y in range(self._y))

    def try_place_piece(self, piece, x, y) -> bool:
        if self._board[x][y] != 0:
            return False
        old_board = self.copy()
        if self._try_expand_piece(piece, x, y):
            self._board[x][y] = piece.value + 2
            return True
        else:
            self._board = old_board._board
            return False

    def _try_expand_piece(self, piece, x, y) -> bool:
        max_iterations = max([self._x, self._y]) if piece.iterative() else 1
        for move in piece.moves():
            a = move[0]
            b = move[1]
            for n in range(max_iterations):
                i = x + (a * (n+1))
                j = y + (b * (n+1))
                if not self._in_board(i, j):
                    break
                if self._board[i][j] > 1:
                    return False
                self._board[i][j] = -1
        return True


def calculate_layouts(m, n, king=0, queen=0, bishop=0, rook=0, knight=0) -> int:
    board = Board(m, n)
    pieces = _expand_pieces(bishop=bishop, king=king,
                            knight=knight, queen=queen, rook=rook)
    permutations = _calculate_permutations(board, pieces)
    denominator = factorial(king) * factorial(queen) * \
        factorial(bishop) * factorial(rook) * factorial(knight)
    return permutations//denominator


def _expand_pieces(bishop, king, knight, queen, rook):
    pieces = []
    pieces.extend([Piece.Queen for _ in range(queen)])
    pieces.extend([Piece.Rook for _ in range(rook)])
    pieces.extend([Piece.Bishop for _ in range(bishop)])
    pieces.extend([Piece.Knight for _ in range(knight)])
    pieces.extend([Piece.King for _ in range(king)])
    return pieces


def _calculate_permutations(board, pieces) -> int:
    no_pieces = len(pieces)
    if no_pieces == 0:
        return 0
    else:
        permutations = 0
        piece = pieces[0]
        for x, y in board.square_coordinates():
            new_board = board.copy()
            if new_board.try_place_piece(piece, x, y):
                if no_pieces > 1:
                    permutations += _calculate_permutations(
                        new_board, pieces[1:])
                else:
                    permutations += 1
        return permutations


if __name__ == '__main__':
    val1 = calculate_layouts(3, 3, king=2, rook=1)
    print(val1)

    val1 = calculate_layouts(4, 4, knight=4, rook=2)
    print(val1)

    val1 = calculate_layouts(3, 3, queen=3)
    print(val1)

    print('=========')
    val1 = calculate_layouts(6, 9, queen=1, king=2, bishop=1, rook=1, knight=1)
    print(val1)
    print('+++++++++')
    # 20136752
