from .shogiboard import BOARD_SIZE, Board
from .shogitypes import Move, Piece, PieceType, Player, Point

RANKS = "abcdefghijkl"

PIECE_SYMBOLS: dict[PieceType, str] = {
    PieceType.bishop: "B",
    PieceType.blind_tiger: "BT",
    PieceType.copper_general: "C",
    PieceType.drunk_elephant: "DE",
    PieceType.dragon_horse: "DH",
    PieceType.dragon_king: "DK",
    PieceType.ferocious_leopard: "FL",
    PieceType.gold_general: "G",
    PieceType.go_between: "GB",
    PieceType.king: "K",
    PieceType.kirin: "KR",
    PieceType.lance: "L",
    PieceType.lion: "LN",
    PieceType.pawn: "P",
    PieceType.phoenix: "PH",
    PieceType.queen: "Q",
    PieceType.rook: "R",
    PieceType.reverse_chariot: "RC",
    PieceType.silver_general: "S",
    PieceType.side_mover: "SM",
    PieceType.vertical_mover: "VM",
}

SYMBOL_TO_TYPE = {s: pt for pt, s in PIECE_SYMBOLS.items()}

EMPTY = "."

def coords_from_point(point: Point) -> str:
    return f"{BOARD_SIZE + 1 - point.col}{RANKS[point.row - 1]}"

def point_from_coords(coords: str) -> Point:
    coords = coords.strip()
    file_str, rank = coords[:-1], coords[-1:]
    if not file_str.isdigit() or rank not in RANKS or not rank:
        raise ValueError(f"bad input {coords!r}")
    file = int(file_str)
    if not 1 <= file <= BOARD_SIZE:
        raise ValueError(f"bad input {coords!r}")
    return Point(row=RANKS.index(rank) + 1, col=BOARD_SIZE + 1 - file)

def piece_to_str(piece: Piece) -> str:
    s = ("+" if piece.promoted else "") + PIECE_SYMBOLS[piece.piece_type]
    return s if piece.colour == Player.black else s.lower()

def piece_from_str(s: str) -> Piece:
    promoted = s.startswith("+")
    body = s[1:] if promoted else s
    if body.isupper():
        colour = Player.black
    elif body.islower():
        colour = Player.white
    else:
        raise ValueError(f"bad piece {s!r}")

    try:
        piece_type = SYMBOL_TO_TYPE[body.upper()]
    except KeyError:
        raise ValueError(f"bad piece {s!r}") from None
    
    return Piece(piece_type, colour, promoted)


def move_to_str(move: Move) -> str:
    squares = [move.from_point] + ([move.via] if move.via else []) + [move.to_point]
    s = "-".join(coords_from_point(p) for p in squares)
    return s + ("+" if move.promote else "")

def move_from_str(s: str) -> Move:
    s = s.strip()
    promote = s.endswith("+")
    parts = (s[:-1] if promote else s).split("-")
    if len(parts) not in (2, 3):
        raise ValueError(f"bad move {s!r}")
    points = [point_from_coords(p) for p in parts]
    via = points[1] if len(points) == 3 else None
    return Move(points[0], points[-1], via, promote)

def print_move(player: Player, move: Move) -> None:
    print(f"{player.name} {move_to_str(move)}")


def board_to_str(board: Board) -> str:
    header = "".join(f"{BOARD_SIZE + 1 - col:>4}" for col in range(1, BOARD_SIZE + 1))
    lines = [header]
    for row in range(1, BOARD_SIZE + 1):
        cells = []
        for col in range(1, BOARD_SIZE + 1):
            piece = board.get(Point(row, col))
            cells.append(f"{piece_to_str(piece) if piece else EMPTY:>4}")
        lines.append("".join(cells) + f" {RANKS[row - 1]}")
    return "\n".join(lines)

def print_board(board: Board) -> None:
    print(board_to_str(board))

def board_from_str(text: str) -> Board:
    board = Board()
    rows = []
    for line in text.strip().splitlines():
        tokens = line.split()
        if not tokens or all(t.isdigit() for t in tokens):
            continue
        if len(tokens) == BOARD_SIZE + 1 and tokens[-1] in RANKS:
            tokens = tokens[:-1]
        if len(tokens) != BOARD_SIZE:
            raise ValueError(f"expected {BOARD_SIZE} cells, got {len(tokens)}: {line!r}")
        rows.append(tokens)
    if len(rows) != BOARD_SIZE:
        raise ValueError(f"expected {BOARD_SIZE} rows, got {len(rows)}")
    for row, tokens in enumerate(rows, start=1):
        for col, token in enumerate(tokens, start=1):
            if token != EMPTY:
                board.place(Point(row, col), piece_from_str(token))

    return board