from .shogitypes import Point, Move, Player
from .shogiboard import Board
from .pieces import Movement, rules_for, ALL_DIRECTIONS

LION_OFFSETS = tuple((dr, dc) for dr in range(-2, 3) for dc in range(-2, 3) if (dr, dc) != (0, 0))

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
                for dr, dc in LION_OFFSETS:
                    target = point.offset(dr, dc)
                    if _can_land(board, target, piece.colour):
                        moves.append(Move(point, target))
                can_pass = can_pass or _any_empty(board, point, ALL_DIRECTIONS)
                
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
