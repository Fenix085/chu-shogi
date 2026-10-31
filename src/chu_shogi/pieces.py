import enum

from .shogitypes import Piece, PieceType, Player, movement_type


class Movement(enum.Enum):
    step = "step"
    line = "line"
    jump = "jump"
    lion_line = "lion_line"
    lion_area = "lion_area"


Direction = tuple[int, int]
Rule = tuple[Movement, Direction | None]

N, S, E, W = (-1, 0), (1, 0), (0, 1), (0, -1)
NE, NW, SE, SW = (-1, 1), (-1, -1), (1, 1), (1, -1)

ORTHOGONAL = (N, S, E, W)
DIAGONAL = (NE, NW, SE, SW)
ALL_DIRECTIONS = ORTHOGONAL + DIAGONAL


def steps(*dirs: Direction) -> list[Rule]:
    return [(Movement.step, d) for d in dirs]


def lines(*dirs: Direction) -> list[Rule]:
    return [(Movement.line, d) for d in dirs]


def jumps(*dirs: Direction) -> list[Rule]:
    return [(Movement.jump, (2 * dr, 2 * dc)) for dr, dc in dirs]


def lion_lines(*dirs: Direction) -> list[Rule]:
    return [(Movement.lion_line, d) for d in dirs]


PT = PieceType

MOVES: dict[PieceType, list[Rule]] = {
    PT.king: steps(*ALL_DIRECTIONS),
    PT.queen: lines(*ALL_DIRECTIONS),
    PT.lion: [(Movement.lion_area, None)],
    PT.dragon_king: steps(*DIAGONAL) + lines(*ORTHOGONAL),
    PT.dragon_horse: steps(*ORTHOGONAL) + lines(*DIAGONAL),
    PT.rook: lines(*ORTHOGONAL),
    PT.bishop: lines(*DIAGONAL),
    PT.kirin: steps(*DIAGONAL) + jumps(*ORTHOGONAL),
    PT.phoenix: steps(*ORTHOGONAL) + jumps(*DIAGONAL),
    PT.drunk_elephant: steps(NE, N, NW, W, SW, SE, E),
    PT.blind_tiger: steps(NE, E, SE, S, SW, W, NW),
    PT.ferocious_leopard: steps(NE, N, NW, SE, S, SW),
    PT.gold_general: steps(NE, N, NW, S, W, E),
    PT.silver_general: steps(NE, N, NW, SE, SW),
    PT.copper_general: steps(NE, N, NW, S),
    PT.vertical_mover: steps(E, W) + lines(N, S),
    PT.side_mover: steps(N, S) + lines(E, W),
    PT.reverse_chariot: lines(N, S),
    PT.lance: lines(N),
    PT.go_between: steps(N, S),
    PT.pawn: steps(N),
    
    PT.flying_stag: steps(NW, NE, W, E, SW, SE) + lines(N, S),
    PT.horned_falcon: lion_lines(N) + lines(NW, NE, W, E, SW, S, SE),
    PT.soaring_eagle: lion_lines(NW, NE) + lines(N, W, E, SW, S, SE),
    PT.prince: steps(*ALL_DIRECTIONS),
    PT.whale: lines(N, SW, S, SE),
    PT.white_horse: lines(NW, N, NE, S),
    PT.free_boar: lines(NW, W, SW, NE, E, SE),
    PT.flying_ox: lines(NW, N, NE, SW, S, SE),
}

assert set(MOVES) == set(PieceType)


def _rotate(rule: Rule) -> Rule:
    kind, d = rule
    return (kind, None if d is None else (-d[0], -d[1]))


_MOVES_BY_PLAYER: dict[Player, dict[PieceType, list[Rule]]] = {
    Player.black: MOVES,
    Player.white: {pt: [_rotate(r) for r in rules] for pt, rules in MOVES.items()},
}


def rules_for(piece: Piece) -> list[Rule]:
    return _MOVES_BY_PLAYER[piece.colour][movement_type(piece)]
