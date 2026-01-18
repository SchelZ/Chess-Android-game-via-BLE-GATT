from game.moves import get_legal_moves

class Game:
    def __init__(self, board, transport=None):
        self.board = board
        self.transport = transport
        self.selected = None
        self.legal_moves = []

    def select(self, x, y):
        if self.selected:
            sx, sy = self.selected
            if (x, y) in self.legal_moves:
                self.board.move(sx, sy, x, y)
                # send move via transport
                if self.transport:
                    self.transport.send_move(sx, sy, x, y)
            self.selected = None
            self.legal_moves = []
            return

        piece = self.board.grid[y][x]
        if piece:
            self.selected = (x, y)
            self.legal_moves = get_legal_moves(self.board, x, y)

    def update(self):
        if self.transport:
            move = self.transport.poll()
            if move:
                x1, y1, x2, y2 = move
                self.board.move(x1, y1, x2, y2)
