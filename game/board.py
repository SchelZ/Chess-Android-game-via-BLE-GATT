from game.pieces import Piece

START_ROW = (2,3,4,5,6,4,3,2)

class Board:
    def __init__(self, debug=True):
        self.debug = debug
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.setup()

    def log(self, msg):
        if self.debug:
            print(f"[BOARD] {msg}")

    def setup(self):
        for x in range(8):
            self.grid[1][x] = Piece(1, 1)  # black pawns
            self.grid[6][x] = Piece(1, 0)  # white pawns

            self.grid[0][x] = Piece(START_ROW[x], 1)  # black back rank
            self.grid[7][x] = Piece(START_ROW[x], 0)  # white back rank

        self.log("Board setup complete")

    def move(self, x1, y1, x2, y2):
        piece = self.grid[y1][x1]
        if piece:
            self.grid[y2][x2] = piece
            self.grid[y1][x1] = None
            self.log(f"Piece {piece.name} moved from ({x1},{y1}) to ({x2},{y2})")
