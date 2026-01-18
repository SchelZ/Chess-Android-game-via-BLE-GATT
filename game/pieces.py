from dataclasses import dataclass

PIECES = {
    1: ("pawn",   "♙", "♟"),
    2: ("rook",   "♖", "♜"),
    3: ("knight", "♘", "♞"),
    4: ("bishop", "♗", "♝"),
    5: ("queen",  "♕", "♛"),
    6: ("king",   "♔", "♚"),
}

@dataclass
class Piece:
    id: int
    color: int

    @property
    def name(self):
        return PIECES[self.id][0]

    @property
    def symbol(self):
        return PIECES[self.id][1 if self.color == 0 else 2]
