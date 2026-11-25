from .shogitypes import Point, Move, Player
from .shogiboard import Board
from .pieces import Movement, rules_for


def piece_moves(board: Board, point: Point) -> list[Move]:
    piece = board.get(point)
    if piece is None:
        raise ValueError("no piece on this cell")
    moves = []
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

            case _:
                raise NotImplementedError(f"{rule} is not implemented")
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


if __name__ == "__main__":
    pass
