from game.moves import get_legal_moves

class Game:
    def __init__(self, board, transport=None, debug=True):
        self.board = board
        self.transport = transport
        self.debug = debug
        self.selected = None
        self.legal_moves = []
        self.turn = 0  # 0 = white, 1 = black

    def log(self, msg):
        if self.debug:
            print(f"[GAME] {msg}")

    def select(self, x, y):
        if not (0 <= x < 8 and 0 <= y < 8):
            self.log(f"Click out of bounds ignored: ({x},{y})")
            return
        
        piece = self.board.grid[y][x]
        self.log(f"Click on ({x},{y}) piece={piece} turn={self.turn}")

        if self.selected and (x, y) in self.legal_moves:
            sx, sy = self.selected
            self.board.move(sx, sy, x, y)
            self.log(f"Moved piece from ({sx},{sy}) to ({x},{y})")

            self.selected = None
            self.legal_moves = []

            if self.debug:
                self.turn = 1 - self.turn
                self.log(f"Turn switched to {self.turn} ({'white' if self.turn==0 else 'black'})")

            if self.transport and not self.debug:
                self.transport.send_move(sx, sy, x, y)

            return

        if not piece:
            self.log("Clicked empty square, deselecting")
            self.selected = None
            self.legal_moves = []
            return

        if piece.color != self.turn:
            self.log(f"Cannot select piece, wrong turn. Piece color={piece.color}")
            return

        self.selected = (x, y)
        self.legal_moves = get_legal_moves(self.board, x, y)
        self.log(f"Selected piece at ({x},{y}) legal_moves={self.legal_moves}")

    def update(self):
        if self.transport and not self.debug:
            move = self.transport.poll()
            if move:
                x1, y1, x2, y2 = move
                self.board.move(x1, y1, x2, y2)
                self.turn = 1 - self.turn
                self.log(f"Received move from transport: ({x1},{y1}) -> ({x2},{y2}), turn now {self.turn}")
