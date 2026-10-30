import random

from .shogitypes import Player, Point, Piece, PieceType, PROMOTED_MOVEMENT, PROMOTED_ONLY

BOARD_SIZE = 12

def _all_pieces():
    for player in Player:
        for piece_type in PieceType:
            if piece_type in PROMOTED_ONLY:
                continue
            yield Piece(piece_type, player)
            if piece_type in PROMOTED_MOVEMENT:
                yield Piece(piece_type, player, promoted=True)

_rng = random.Random(42)

HASH_CODE: dict[tuple[Point, Piece], int] = {
    (Point(row, col), piece): _rng.getrandbits(64)
    for row in range(1, BOARD_SIZE + 1)
    for col in range(1, BOARD_SIZE + 1)
    for piece in _all_pieces()
}

BLACK_TO_MOVE: int = _rng.getrandbits(64)

EMPTY_BOARD = 0