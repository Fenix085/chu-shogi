from .shogitypes import Piece, PieceType, Player, Point
from .shogiboard import Board

from .utils import print_board

BOARD_SIZE = 12

BLACK_SETUP: tuple[tuple[PieceType, Point], ...] = (
    (PieceType.lance, Point(12, 1)),
    (PieceType.lance, Point(12, 12)),
    (PieceType.ferocious_leopard, Point(12, 2)),
    (PieceType.ferocious_leopard, Point(12, 11)),
    (PieceType.copper_general, Point(12, 3)),
    (PieceType.copper_general, Point(12, 10)),
    (PieceType.silver_general, Point(12, 4)),
    (PieceType.silver_general, Point(12, 9)),
    (PieceType.gold_general, Point(12, 5)),
    (PieceType.gold_general, Point(12, 8)),
    (PieceType.king, Point(12, 6)),
    (PieceType.drunk_elephant, Point(12, 7)),

    (PieceType.reverse_chariot, Point(11, 1)),
    (PieceType.reverse_chariot, Point(11, 12)),
    (PieceType.bishop, Point(11, 3)),
    (PieceType.bishop, Point(11, 10)),
    (PieceType.blind_tiger, Point(11, 5)),
    (PieceType.blind_tiger, Point(11, 8)),
    (PieceType.kirin, Point(11, 6)),
    (PieceType.phoenix, Point(11, 7)),

    (PieceType.side_mover, Point(10, 1)),
    (PieceType.side_mover, Point(10, 12)),
    (PieceType.vertical_mover, Point(10, 2)),
    (PieceType.vertical_mover, Point(10, 11)),
    (PieceType.rook, Point(10, 3)),
    (PieceType.rook, Point(10, 10)),
    (PieceType.dragon_horse, Point(10, 4)),
    (PieceType.dragon_horse, Point(10, 9)),
    (PieceType.dragon_king, Point(10, 5)),
    (PieceType.dragon_king, Point(10, 8)),
    (PieceType.lion, Point(10, 6)),
    (PieceType.queen, Point(10, 7)),

    (PieceType.pawn, Point(9, 1)),
    (PieceType.pawn, Point(9, 2)),
    (PieceType.pawn, Point(9, 3)),
    (PieceType.pawn, Point(9, 4)),
    (PieceType.pawn, Point(9, 5)),
    (PieceType.pawn, Point(9, 6)),
    (PieceType.pawn, Point(9, 7)),
    (PieceType.pawn, Point(9, 8)),
    (PieceType.pawn, Point(9, 9)),
    (PieceType.pawn, Point(9, 10)),
    (PieceType.pawn, Point(9, 11)),
    (PieceType.pawn, Point(9, 12)),

    (PieceType.go_between, Point(8, 4)),
    (PieceType.go_between, Point(8, 9)),
)


def rotate(p: Point) -> Point:
    return Point(BOARD_SIZE + 1 - p.row, BOARD_SIZE + 1 - p.col)

def starting_board() -> Board:
    board = Board()
    for i in range(2): #first iter for black, second for white; TODO rewrite more normal
        colour = Player.black
        if i:
            colour = Player.white
        for ptype, point in BLACK_SETUP:
            if i:
                point = rotate(point)
            piece = Piece(ptype, colour, promoted=False)
            board.place(point, piece)
    return board

if __name__ == "__main__":
    print_board(starting_board())
