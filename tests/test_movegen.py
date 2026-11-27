import pytest

from chu_shogi.movegen import piece_moves
from chu_shogi.shogiboard import Board
from chu_shogi.shogitypes import Point, Player, Piece, PieceType
from chu_shogi.utils import coords_from_point, point_from_coords
from chu_shogi.layout import rotate


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
        # --------------------------------------------------
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


def test_blocked_piece_friendly():
    board = board_with((Point(6, 6), Piece(PieceType.rook, Player.black)), (Point(3, 6), Piece(PieceType.pawn, Player.black)))
    _targets = targets(board, Point(6, 6))
    assert len(_targets) == 19
    assert "7c" not in _targets

def test_blocked_piece_hostile():
    board = board_with((Point(6, 6), Piece(PieceType.rook, Player.black)), (Point(3, 6), Piece(PieceType.pawn, Player.white)))
    _targets = targets(board, Point(6, 6))
    assert len(_targets) == 20
    assert "7b" not in _targets
    assert "7c" in _targets

def test_pawn_directions_black():
    board = board_with((Point(6, 6), Piece(PieceType.pawn, Player.black)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"7e"}
 
def test_pawn_directions_white():
    board = board_with((Point(6, 6), Piece(PieceType.pawn, Player.white)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"7g"}

def test_gold_directions_black():
    board = board_with((Point(6, 6), Piece(PieceType.gold_general, Player.black)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"6e", "7e", "8e", "6f", "8f", "7g"}  

def test_gold_directions_white():
    board = board_with((Point(6, 6), Piece(PieceType.gold_general, Player.white)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"6g", "7e", "8g", "6f", "8f", "7g"}  

@pytest.mark.parametrize(
    "piece_type, promoted",
    [
        (PieceType.king, False),
        (PieceType.queen, False),
        # lion skipped
        (PieceType.rook, False),
        (PieceType.bishop, False),
        (PieceType.dragon_king, False),
        (PieceType.dragon_horse, False),
        (PieceType.kirin, False),
        (PieceType.phoenix, False),
        (PieceType.drunk_elephant, False),
        (PieceType.blind_tiger, False),
        (PieceType.ferocious_leopard, False),
        (PieceType.gold_general, False),
        (PieceType.silver_general, False),
        (PieceType.copper_general, False),
        (PieceType.vertical_mover, False),
        (PieceType.side_mover, False),
        (PieceType.reverse_chariot, False),
        (PieceType.lance, False),
        (PieceType.go_between, False),
        (PieceType.pawn, False),
        # --------------------------------------------------
        (PieceType.blind_tiger, True),  # flying stag
        # horned_falcon skipped
        # soaring_eagle skipped
        (PieceType.drunk_elephant, True),  # prince
        (PieceType.reverse_chariot, True),  # whale
        (PieceType.lance, True),  # white horse
        (PieceType.side_mover, True),  # free boar
        (PieceType.vertical_mover, True),  # flying ox
    ],
)
def test_mirror(piece_type, promoted):
    board_black = board_with((Point(4, 3), Piece(piece_type, Player.black, promoted)))
    board_white = board_with((rotate(Point(4, 3)), Piece(piece_type, Player.white, promoted)))

    _targets_black = targets(board_black, Point(4, 3))
    _targets_white = targets(board_white, rotate(Point(4, 3)))

    _targets_black_rotated = set()
    for i in range(len(_targets_black)):
        _targets_black_rotated.add(coords_from_point(rotate(point_from_coords(list(_targets_black)[i]))))

    assert _targets_black_rotated == _targets_white

def test_pawn_last_rank_black():
    board = board_with((Point(1, 1), Piece(PieceType.pawn, Player.black, False)))
    _targets = targets(board, Point(1, 1))
    assert _targets == set()

def test_pawn_last_rank_white():
    board = board_with((Point(12, 12), Piece(PieceType.pawn, Player.white, False)))
    _targets = targets(board, Point(12, 12))
    assert _targets == set()