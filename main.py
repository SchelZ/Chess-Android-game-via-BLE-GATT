import pygame
import struct
import threading
import time
from jnius import autoclass, cast

pygame.init()
WIDTH, HEIGHT = 720, 720
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()

ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH // COLS
WHITE = (240, 217, 181)
BLACK = (181, 136, 99)

board = [[None for _ in range(8)] for _ in range(8)]
for i in range(8):
    board[1][i] = "bP"
    board[6][i] = "wP"

selected = None
player_turn = True

PythonActivity = autoclass('org.kivy.android.PythonActivity')
activity = PythonActivity.mActivity
BluetoothAdapter = autoclass('android.bluetooth.BluetoothAdapter')
UUID = autoclass('java.util.UUID')

adapter = BluetoothAdapter.getDefaultAdapter()
if not adapter.isEnabled():
    adapter.enable()

SERVICE_UUID = UUID.fromString("0000aaaa-0000-1000-8000-00805f9b34fb")
CHAR_UUID = UUID.fromString("0000bbbb-0000-1000-8000-00805f9b34fb")

ble_move_lock = threading.Lock()
received_move = None

def pack_move(src, dst, promo=0):
    return struct.pack('BBB', src, dst, promo)

def unpack_move(data):
    src, dst, promo = struct.unpack('BBB', data)
    return src, dst, promo

def coords_to_square(row, col):
    return row*8 + col

def square_to_coords(square):
    return square // 8, square % 8

def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            color = WHITE if (row+col)%2==0 else BLACK
            pygame.draw.rect(SCREEN, color, (col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces():
    font = pygame.font.SysFont(None, 48)
    for row in range(ROWS):
        for col in range(COLS):
            piece = board[row][col]
            if piece:
                text = font.render(piece, True, (0,0,0))
                SCREEN.blit(text, (col*SQUARE_SIZE + 10, row*SQUARE_SIZE + 10))


def ble_thread():
    global received_move
    while True:
        time.sleep(10)
        with ble_move_lock:
            received_move = pack_move(12, 28, 0)

threading.Thread(target=ble_thread, daemon=True).start()


running = True
while running:
    draw_board()
    draw_pieces()
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN, pygame.FINGERMOTION):
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
            else:
                x, y = int(event.x*WIDTH), int(event.y*HEIGHT)
            col, row = x//SQUARE_SIZE, y//SQUARE_SIZE

            if player_turn:
                if selected is None and board[row][col]:
                    selected = (row, col)
                elif selected:
                    src_sq = coords_to_square(*selected)
                    dst_sq = coords_to_square(row, col)
                    promo = 0  # handle promotion if needed
                    board[row][col] = board[selected[0]][selected[1]]
                    board[selected[0]][selected[1]] = None

                    # TODO: send move via BLE characteristic
                    move_data = pack_move(src_sq, dst_sq, promo)

                    player_turn = False
                    selected = None

    with ble_move_lock:
        if received_move:
            src, dst, promo = unpack_move(received_move)
            sr, sc = square_to_coords(src)
            dr, dc = square_to_coords(dst)
            board[dr][dc] = board[sr][sc]
            board[sr][sc] = None
            received_move = None
            player_turn = True

    CLOCK.tick(30)

pygame.quit()
