import pytest

from chu_shogi.movegen import piece_moves
from chu_shogi.shogiboard import Board
from chu_shogi.shogitypes import Point, Player, Piece, PieceType, Move
from chu_shogi.utils import coords_from_point, move_to_str
from chu_shogi.layout import rotate


def board_with(*placements) -> Board:
    board = Board()
    for point, piece in placements:
        board.place(point, piece)
    return board


def targets(board: Board, point: Point) -> set[str]:
    moves = piece_moves(board, point)
    return {coords_from_point(m.to_point) for m in moves}

def targets_lion(board: Board, point: Point) -> list[str]:
    return [move_to_str(m) for m in piece_moves(board, point)]

def assert_no_duplicates(moves) -> None:
    assert len(moves) == len(set(moves))

def rotate_move(m: Move) -> Move:
    from_point, to_point, via = m.from_point, m.to_point, m.via
    return Move(rotate(from_point), rotate(to_point), (rotate(via) if via is not None else None), m.promote)

# ------ TESTS --------------------------------------------------------

def test_king_in_middle():
    board = board_with((Point(6, 6), Piece(PieceType.king, Player.black)))
    _targets = targets(board, Point(6, 6))
    assert _targets == {"6g", "6e", "7e", "7g", "8g", "8f", "8e", "6f"}


@pytest.mark.parametrize(
    "piece_type, promoted, expected",
    [
        (PieceType.king, False, 8),
        (PieceType.queen, False, 43),
        (PieceType.lion, False, 25),
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
        (PieceType.go_between, True, 7), # drunk elephant
        (PieceType.pawn, True, 6), # gold general
        (PieceType.bishop, True, 25), # dragon horse
        (PieceType.rook, True, 26), # dragon king
        (PieceType.ferocious_leopard, True, 21), # bishop
        (PieceType.copper_general, True, 13), # side mover
        (PieceType.silver_general, True, 13), # vertical mover
        (PieceType.gold_general, True, 22), # rook
        (PieceType.kirin, True, 25), # lion
        (PieceType.phoenix, True, 43), # queen
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
    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    assert len(_targets) == expected


def test_blocked_piece_friendly():
    board = board_with(
        (Point(6, 6), Piece(PieceType.rook, Player.black)),
        (Point(3, 6), Piece(PieceType.pawn, Player.black)),
    )
    _targets = targets(board, Point(6, 6))
    assert len(_targets) == 19
    assert "7c" not in _targets


def test_blocked_piece_hostile():
    board = board_with(
        (Point(6, 6), Piece(PieceType.rook, Player.black)),
        (Point(3, 6), Piece(PieceType.pawn, Player.white)),
    )
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
        (PieceType.lion, False),
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
        (PieceType.go_between, True), # drunk elephant
        (PieceType.pawn, True), # gold general
        (PieceType.bishop, True), # dragon horse
        (PieceType.rook, True), # dragon king
        (PieceType.ferocious_leopard, True), # bishop
        (PieceType.copper_general, True), # side mover
        (PieceType.silver_general, True), # vertical mover
        (PieceType.gold_general, True), # rook
        (PieceType.kirin, True), # lion
        (PieceType.phoenix, True), # queen
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
    board_white = board_with(
        (rotate(Point(4, 3)), Piece(piece_type, Player.white, promoted))
    )

    moves_black = piece_moves(board_black, Point(4, 3))
    moves_white = piece_moves(board_white, rotate(Point(4, 3)))

    rotated_black = {rotate_move(m) for m in moves_black}
        
    assert rotated_black == set(moves_white)


def test_pawn_last_rank_black():
    board = board_with((Point(1, 1), Piece(PieceType.pawn, Player.black, False)))
    _targets = targets(board, Point(1, 1))
    assert _targets == set()


def test_pawn_last_rank_white():
    board = board_with((Point(12, 12), Piece(PieceType.pawn, Player.white, False)))
    _targets = targets(board, Point(12, 12))
    assert _targets == set()

def test_lion_in_middle():
    board = board_with((Point(6, 6), Piece(PieceType.lion, Player.black, False)))
    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    LION_7F_SQUARE = {f"7f-{sq}" for sq in ["5d", "5e", "5f", "5g", "5h", 
                                            "6d", "6e", "6f", "6g", "6h", 
                                            "7d", "7e", "7g", "7h", 
                                            "8d", "8e", "8f", "8g", "8h", 
                                            "9d", "9e", "9f", "9g", "9h"]}
    assert set(_targets) == LION_7F_SQUARE | {"7f-7f"}

def test_lion_with_friends():
    board = board_with((Point(6, 6), Piece(PieceType.lion, Player.black, False)), 
    (Point(5, 5), Piece(PieceType.copper_general, Player.black, False)),
    (Point(5, 6), Piece(PieceType.copper_general, Player.black, False)),
    (Point(5, 7), Piece(PieceType.copper_general, Player.black, False)),
    (Point(6, 5), Piece(PieceType.copper_general, Player.black, False)),
    (Point(6, 7), Piece(PieceType.copper_general, Player.black, False)),
    (Point(7, 5), Piece(PieceType.copper_general, Player.black, False)),
    (Point(7, 6), Piece(PieceType.copper_general, Player.black, False)),
    (Point(7, 7), Piece(PieceType.copper_general, Player.black, False)),)
    
    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    LION_7F_SQUARE = {f"7f-{sq}" for sq in ["5d", "5e", "5f", "5g", "5h", 
                                            "6d", "6h", 
                                            "7d", "7h", 
                                            "8d", "8h", 
                                            "9d", "9e", "9f", "9g", "9h"]}
    assert set(_targets) == LION_7F_SQUARE

def test_lion_with_foe():
    board = board_with((Point(6, 6), Piece(PieceType.lion, Player.black, False)), 
    (Point(5, 6), Piece(PieceType.copper_general, Player.white, False)),)
    plain = {f"7f-{sq}" for sq in ["5d", "5e", "5f", "5g", "5h", 
                                    "6d", "6e", "6f", "6g", "6h", 
                                    "7d", "7e", "7g", "7h", 
                                    "8d", "8e", "8f", "8g", "8h", 
                                    "9d", "9e", "9f", "9g", "9h"]}
    
    via_moves = {f"7f-7e-{sq}" for sq in ["6d", "6e", "6f",
                                        "7d",
                                        "8d", "8e", "8f",]}

    igui = {"7f-7e-7f"}

    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    assert set(_targets) == plain | via_moves | igui | {"7f-7f"}

def test_lion_with_2_foes():
    board = board_with((Point(6, 6), Piece(PieceType.lion, Player.black, False)), 
    (Point(5, 6), Piece(PieceType.copper_general, Player.white, False)),
    (Point(5, 7), Piece(PieceType.copper_general, Player.white, False)),)
    plain = {f"7f-{sq}" for sq in ["5d", "5e", "5f", "5g", "5h", 
                                    "6d", "6e", "6f", "6g", "6h", 
                                    "7d", "7e", "7g", "7h", 
                                    "8d", "8e", "8f", "8g", "8h", 
                                    "9d", "9e", "9f", "9g", "9h"]}
    
    via_moves = {f"7f-7e-{sq}" for sq in ["6d", "6e", "6f",
                                        "7d",
                                        "8d", "8e", "8f",]}
    
    via_moves_2 = {f"7f-6e-{sq}" for sq in ["5d", "5e", "5f",
                                            "6d", "6f",
                                            "7d", "7e", ]}

    igui = {"7f-7e-7f"}
    igui2 = {"7f-6e-7f"}

    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    assert set(_targets) == plain | via_moves | via_moves_2 | igui | igui2 | {"7f-7f"}


def test_lion_with_foe_2_squares_away():
    board = board_with((Point(6, 6), Piece(PieceType.lion, Player.black, False)), 
    (Point(4, 6), Piece(PieceType.copper_general, Player.white, False)),)
    plain = {f"7f-{sq}" for sq in ["5d", "5e", "5f", "5g", "5h", 
                                    "6d", "6e", "6f", "6g", "6h", 
                                    "7d", "7e", "7g", "7h", 
                                    "8d", "8e", "8f", "8g", "8h", 
                                    "9d", "9e", "9f", "9g", "9h"]}

    _targets = targets_lion(board, Point(6, 6))
    assert_no_duplicates(_targets)
    assert set(_targets) == plain | {"7f-7f"}

def test_lion_in_corner():
    board = board_with((Point(1, 12), Piece(PieceType.lion, Player.black, False)))
    _targets = targets_lion(board, Point(1, 12))
    assert_no_duplicates(_targets)
    LION_1A_SQUARE = {f"1a-{sq}" for sq in ["1c", "1b", 
                                            "2c", "2b", "2a", 
                                            "3c", "3b", "3a", ]}
    assert set(_targets) == LION_1A_SQUARE | {"1a-1a"}

def test_lion_in_corner_with_friends():
    board = board_with((Point(1, 12), Piece(PieceType.lion, Player.black, False)),
                       (Point(1, 11), Piece(PieceType.copper_general, Player.black, False)),
                       (Point(2, 11), Piece(PieceType.copper_general, Player.black, False)),
                       (Point(2, 12), Piece(PieceType.copper_general, Player.black, False)),
                       )
    _targets = targets_lion(board, Point(1, 12))
    assert_no_duplicates(_targets)
    LION_1A_SQUARE = {f"1a-{sq}" for sq in ["1c", 
                                            "2c", 
                                            "3c", "3b", "3a", ]}
    assert set(_targets) == LION_1A_SQUARE 