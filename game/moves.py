def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_legal_moves(board, x, y):
    piece = board.grid[y][x]
    if not piece:
        return []

    moves = []

    if piece.name == "pawn":
        direction = -1 if piece.color == 0 else 1
        ny = y + direction

        if in_bounds(x, ny) and board.grid[ny][x] is None:
            moves.append((x, ny))

        for dx in (-1, 1):
            nx = x + dx
            if in_bounds(nx, ny):
                target = board.grid[ny][nx]
                if target and target.color != piece.color:
                    moves.append((nx, ny))

    elif piece.name == "rook":
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            nx, ny = x+dx, y+dy
            while in_bounds(nx, ny):
                t = board.grid[ny][nx]
                if t:
                    if t.color != piece.color:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
                nx += dx
                ny += dy

    elif piece.name == "bishop":
        for dx, dy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
            nx, ny = x+dx, y+dy
            while in_bounds(nx, ny):
                t = board.grid[ny][nx]
                if t:
                    if t.color != piece.color:
                        moves.append((nx, ny))
                    break
                moves.append((nx, ny))
                nx += dx
                ny += dy

    elif piece.name == "queen":
        # combine rook + bishop moves
        moves.extend(get_legal_moves_rook(board, x, y))
        moves.extend(get_legal_moves_bishop(board, x, y))

    elif piece.name == "knight":
        for dx, dy in [
            (1,2),(2,1),(-1,2),(-2,1),
            (1,-2),(2,-1),(-1,-2),(-2,-1)
        ]:
            nx, ny = x+dx, y+dy
            if in_bounds(nx, ny):
                t = board.grid[ny][nx]
                if not t or t.color != piece.color:
                    moves.append((nx, ny))

    elif piece.name == "king":
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx == dy == 0:
                    continue
                nx, ny = x+dx, y+dy
                if in_bounds(nx, ny):
                    t = board.grid[ny][nx]
                    if not t or t.color != piece.color:
                        moves.append((nx, ny))

    return moves

# helpers for queen
def get_legal_moves_rook(board, x, y):
    moves = []
    for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
        nx, ny = x+dx, y+dy
        while 0<=nx<8 and 0<=ny<8:
            t = board.grid[ny][nx]
            if t:
                if t.color != board.grid[y][x].color:
                    moves.append((nx, ny))
                break
            moves.append((nx, ny))
            nx += dx
            ny += dy
    return moves

def get_legal_moves_bishop(board, x, y):
    moves = []
    for dx, dy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        nx, ny = x+dx, y+dy
        while 0<=nx<8 and 0<=ny<8:
            t = board.grid[ny][nx]
            if t:
                if t.color != board.grid[y][x].color:
                    moves.append((nx, ny))
                break
            moves.append((nx, ny))
            nx += dx
            ny += dy
    return moves
