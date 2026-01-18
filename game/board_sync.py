def encode_board(board):
    data = bytearray(64)

    i = 0
    for row in board:
        for p in row:
            if p is None:
                data[i] = 0
            else:
                data[i] = (p.color << 3) | p.pid
            i += 1

    return bytes(data)

from game.pieces import PIECES
from game.chess_logic import Piece

def decode_board(data):
    board = []
    i = 0

    for y in range(8):
        row = []
        for x in range(8):
            v = data[i]
            i += 1

            if v == 0:
                row.append(None)
            else:
                color = (v >> 3) & 1
                pid = v & 0x7
                row.append(Piece(color, pid))

        board.append(row)

    return board
