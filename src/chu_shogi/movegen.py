from .shogitypes import Point, Move, Player
from .shogiboard import Board
from .pieces import Movement, rules_for, ALL_DIRECTIONS

LION_OFFSETS = tuple(
    (dr, dc) for dr in range(-2, 3) for dc in range(-2, 3) if (dr, dc) != (0, 0)
)


def _lion_area_moves(board: Board, point: Point, colour: Player) -> list[Move]:
    moves = []
    for dr, dc in LION_OFFSETS:
        target = point.offset(dr, dc)
        if _can_land(board, target, colour):
            moves.append(Move(point, target))

    for dr, dc in ALL_DIRECTIONS:
        a = point.offset(dr, dc)
        p = board.get(a)
        if p is None or p.colour == colour:
            continue
        for dr2, dc2 in ALL_DIRECTIONS:
            b = a.offset(dr2, dc2)
            if b == point:
                moves.append(Move(point, point, via=a))  # igui
            elif _can_land(board, b, colour):
                moves.append(Move(point, b, via=a))
    return moves


def _lion_line_moves(
    board: Board, point: Point, colour: Player, dr: int, dc: int
) -> list[Move]:
    moves = []
    d1 = point.offset(dr, dc)
    d2 = point.offset(2 * dr, 2 * dc)
    if _can_land(board, d1, colour):
        moves.append(Move(point, d1))
    if _can_land(board, d2, colour):
        moves.append(Move(point, d2))
    p = board.get(d1)
    if p is not None and p.colour != colour:
        moves.append(Move(point, point, via=d1))  # igui
        if _can_land(board, d2, colour):
            moves.append(Move(point, d2, via=d1))
    return moves


def piece_moves(board: Board, point: Point) -> list[Move]:
    piece = board.get(point)
    if piece is None:
        raise ValueError("no piece on this cell")
    moves = []
    can_pass = False
    for rule in rules_for(piece):
        match rule:
            case (Movement.step, (dr, dc)) | (Movement.jump, (dr, dc)):
                target = point.offset(dr, dc)
                if _can_land(board, target, piece.colour):
                    moves.append(Move(point, target))

            case (Movement.line, (dr, dc)):
                target = point.offset(dr, dc)

                while _can_land(board, target=target, colour=piece.colour):
                    t_cell = board.get(target)
                    moves.append(Move(point, target))
                    if t_cell is None:
                        target = Point.offset(target, dr, dc)
                    else:
                        break
            case (Movement.lion_area, None):
                moves += _lion_area_moves(board, point, colour=piece.colour)
                can_pass = can_pass or _any_empty(board, point, ALL_DIRECTIONS)

            case (Movement.lion_line, (dr, dc)):
                moves += _lion_line_moves(
                    board, point, colour=piece.colour, dr=dr, dc=dc
                )
                can_pass = can_pass or _any_empty(board, point, ((dr, dc),))

            case _:
                raise NotImplementedError(f"{rule} is not implemented")
    if can_pass:
        moves.append(Move(point, point))
    return moves


def _can_land(board: Board, target: Point, colour: Player) -> bool:
    """
    True if `target` is on the board and not occupied by a piece of `colour`.
    """
    if board.is_on_grid(target):
        t_cell = board.get(target)
        if t_cell is None:
            return True
        elif t_cell.colour != colour:
            return True
        else:
            return False
    else:
        return False


def _any_empty(board: Board, point: Point, dirs: tuple) -> bool:
    for dr, dc in dirs:
        p = point.offset(dr, dc)
        if board.is_on_grid(p) and board.get(p) is None:
            return True
    return False


if __name__ == "__main__":
    pass
