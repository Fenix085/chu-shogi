from . import zobrist
from .shogitypes import Piece, Point

BOARD_SIZE = 12


class Board:
    def __init__(self) -> None:
        self.num_rows = BOARD_SIZE
        self.num_cols = BOARD_SIZE
        self._grid: dict[Point, Piece] = {}
        self._hash = zobrist.EMPTY_BOARD

    def is_on_grid(self, point: Point) -> bool:
        return 1 <= point.row <= self.num_rows and 1 <= point.col <= self.num_cols

    def get(self, point: Point) -> Piece | None:
        return self._grid.get(point)

    def pieces(self):
        return self._grid.items()

    def zobrist_hash(self) -> int:
        return self._hash

    def place(self, point: Point, piece: Piece) -> None:
        if not self.is_on_grid(point):
            raise ValueError(f"{point} is not on the board")
        if point in self._grid:
            raise ValueError(f"{point} is already occupied")
        self._grid[point] = piece
        self._hash ^= zobrist.HASH_CODE[point, piece]

    def remove(self, point: Point) -> Piece:
        if not self.is_on_grid(point):
            raise ValueError(f"{point} is not on the board")
        if point not in self._grid:
            raise ValueError(f"no piece at {point}")
        piece = self._grid.pop(point)
        self._hash ^= zobrist.HASH_CODE[point, piece]
        return piece

    def move(
        self, from_point: Point, to_point: Point, promote: bool = False
    ) -> Piece | None:
        piece = self._grid.get(from_point)
        if piece is None:
            raise ValueError(f"no piece at {from_point}")
        target = self._grid.get(to_point)
        if target is not None and target.colour == piece.colour:
            raise ValueError(f"{to_point} has a friendly unit")
        if promote and not piece.can_promote:
            raise ValueError(f"{piece} cannot promote")

        self.remove(from_point)
        captured = self.remove(to_point) if target is not None else None
        self.place(to_point, piece.promote() if promote else piece)
        return captured

    def copy(self) -> "Board":
        new = Board()
        new._grid = dict(self._grid)
        new._hash = self._hash
        return new
