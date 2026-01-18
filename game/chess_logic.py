from game.protocol import PACKET, encode_move, decode_move
from game.pieces import PIECES
from game.moves import get_legal_moves

EMPTY = None

class Piece:
    __slots__ = ("color", "pid")

    def __init__(self, color: int, pid: int):
        self.color = color
        self.pid = pid


class ChessGame:
    def __init__(self, transport, local_player=True):
        self.transport = transport
        self.local_player = local_player
        self.turn = 0
        self.selected = None
        self.board = self._create_board()
        self.legal_moves = []

    def _create_board(self):
        board = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            board[1][i] = Piece(0, 1)  # pawn
            board[6][i] = Piece(1, 1)

        for i, pid in enumerate(PIECES):
            board[0][i] = Piece(0, pid)
            board[7][i] = Piece(1, pid)

        return board
    def is_legal(self, fx, fy, tx, ty):
        p = self.board[fy][fx]
        if not p:
            return False
        if p.color != self.turn:
            return False
        if fx == tx and fy == ty:
            return False
        return True

    def select(self, x, y):
        if self.selected:
            sx, sy = self.selected
            if (x, y) in self.legal_moves:
                self.board.move(sx, sy, x, y)
            self.selected = None
            self.legal_moves = []
            return

        piece = self.board.grid[y][x]
        if piece:
            self.selected = (x, y)
            self.legal_moves = get_legal_moves(self.board, x, y)

    def send_move(self, fx, fy, tx, ty):
        packet = bytes([PACKET.MOVE]) + encode_move(fx, fy, tx, ty)
        self.transport.send(packet)

    def apply_move(self, fx, fy, tx, ty):
        self.board[ty][tx] = self.board[fy][fx]
        self.board[fy][fx] = EMPTY
        self.turn ^= 1

    def update(self):
        pkt = self.transport.poll()
        if not pkt:
            return

        if pkt[0] == PACKET.MOVE:
            fx, fy, tx, ty = decode_move(pkt[1:])
            self.apply_move(fx, fy, tx, ty)
