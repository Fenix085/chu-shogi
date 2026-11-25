import pytest

from chu_shogi.movegen import piece_moves
from chu_shogi.shogiboard import Board
from chu_shogi.shogitypes import Point, Player, Piece, PieceType
from chu_shogi.utils import coords_from_point


def board_with(*placements) -> Board:
    board = Board()
    for point, piece in placements:
        board.place(point, piece)
    return board


def targets(board: Board, point: Point) -> set[str]:
    moves = piece_moves(board, point)
    return {coords_from_point(m.to_point) for m in moves}


def test_king_in_middle():
    board = board_with((Point(6, 6), Piece(PieceType.king, Player.black)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"6g", "6e", "7e", "7g", "8g", "8f", "8e", "6f"}


@pytest.mark.parametrize(
    "piece_type, promoted, expected",
    [
        (PieceType.king, False, 8),
        (PieceType.queen, False, 43),
        # lion skipped
        (PieceType.rook, False, 22),
        (PieceType.bishop, False, 21),
        (PieceType.dragon_king, False, 26),
        (PieceType.dragon_horse, False, 25),
        (PieceType.kirin, False, 8),
        (PieceType.phoenix, False, 8),
        (PieceType.drunk_elephant, False, 7),
        (PieceType.blind_tiger, False, 7),
        (PieceType.ferocious_leopard, False, 6),
        (PieceType.gold_general, False, 6),
        (PieceType.silver_general, False, 5),
        (PieceType.copper_general, False, 4),
        (PieceType.vertical_mover, False, 13),
        (PieceType.side_mover, False, 13),
        (PieceType.reverse_chariot, False, 11),
        (PieceType.lance, False, 5),
        (PieceType.go_between, False, 2),
        (PieceType.pawn, False, 1),
        #--------------------------------------------------
        (PieceType.blind_tiger, True, 17),  # flying stag
        # horned_falcon skipped
        # soaring_eagle skipped
        (PieceType.drunk_elephant, True, 8),  # prince
        (PieceType.reverse_chariot, True, 22),  # whale
        (PieceType.lance, True, 21),  # white horse
        (PieceType.side_mover, True, 32),  # free boar
        (PieceType.vertical_mover, True, 32),  # flying ox
    ],
)
def test_empty_board_count(piece_type, promoted, expected):
    board = board_with((Point(6, 6), Piece(piece_type, Player.black, promoted)))
    _targets = targets(board, Point(6, 6))
    assert len(_targets) == expected
