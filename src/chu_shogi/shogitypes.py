import enum
from typing import NamedTuple

class Player(enum.Enum):
    white = 1
    black = 2

    @property
    def other(self):
        return Player.white if self == Player.black else Player.black

class Point(NamedTuple):
    row: int
    col: int

    def offset(self, dr: int, dc: int) -> "Point":
        return Point(self.row + dr, self.col + dc)