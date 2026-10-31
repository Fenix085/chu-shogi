import enum
from dataclasses import dataclass, replace
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

@dataclass(frozen=True)
class Move:
    from_point: Point
    to_point: Point
    via: Point | None = None#for lion moves
    promote: bool = False

class PieceType(enum.Enum):
    king = 1
    queen = 2
    lion = 3
    dragon_king = 4
    dragon_horse = 5
    rook = 6
    bishop = 7
    kirin = 8
    phoenix = 9
    drunk_elephant = 10
    blind_tiger = 11
    ferocious_leopard = 12
    gold_general = 13
    silver_general = 14
    copper_general = 15
    vertical_mover = 16
    side_mover = 17
    reverse_chariot = 18
    lance = 19
    go_between = 20
    pawn = 21

    flying_stag = 22
    horned_falcon = 23
    soaring_eagle = 24
    prince = 25
    whale = 26
    white_horse = 27
    free_boar = 28
    flying_ox = 29
    

PROMOTED_MOVEMENT = {
    PieceType.pawn: PieceType.gold_general,
    PieceType.go_between: PieceType.drunk_elephant,
    PieceType.lance: PieceType.white_horse,
    PieceType.reverse_chariot: PieceType.whale,
    PieceType.side_mover: PieceType.free_boar,
    PieceType.vertical_mover: PieceType.flying_ox,
    PieceType.copper_general: PieceType.side_mover,
    PieceType.silver_general: PieceType.vertical_mover,
    PieceType.gold_general: PieceType.rook,
    PieceType.ferocious_leopard: PieceType.bishop,
    PieceType.blind_tiger: PieceType.flying_stag,
    PieceType.drunk_elephant: PieceType.prince,
    PieceType.phoenix: PieceType.queen,
    PieceType.kirin: PieceType.lion,
    PieceType.bishop: PieceType.dragon_horse,
    PieceType.rook: PieceType.dragon_king,
    PieceType.dragon_horse: PieceType.horned_falcon,
    PieceType.dragon_king: PieceType.soaring_eagle,
}

PROMOTED_ONLY: frozenset[PieceType] = frozenset({
    PieceType.flying_ox,
    PieceType.flying_stag,
    PieceType.free_boar,
    PieceType.horned_falcon,
    PieceType.prince,
    PieceType.soaring_eagle,
    PieceType.whale,
    PieceType.white_horse,
})

@dataclass(frozen=True)
class Piece:
    piece_type: PieceType
    colour: Player
    promoted: bool = False

    def __post_init__(self) -> None:
        if self.piece_type in PROMOTED_ONLY:
            raise ValueError(
                f"{self.piece_type.name} only exists as a promoted piece; "
                f"create the base piece with promoted=True instead"
            )
        if self.promoted and self.piece_type not in PROMOTED_MOVEMENT:
            raise ValueError(f"{self.piece_type.name} cannot be promoted")

    @property
    def can_promote(self) -> bool:
        return not self.promoted and self.piece_type in PROMOTED_MOVEMENT

    def promote(self) -> "Piece":
        if not self.can_promote:
            raise ValueError(f"{self} cannot promote")
        return replace(self, promoted=True)

    def is_royal(self) -> bool:
        return self.piece_type == PieceType.king or (
            self.piece_type == PieceType.drunk_elephant and self.promoted
        )
    
def movement_type(piece: Piece) -> PieceType:
    if not piece.promoted:
        return piece.piece_type
    try:
        return PROMOTED_MOVEMENT[piece.piece_type]
    except KeyError:
        raise ValueError(f"{piece.piece_type} cannot be promoted") from None