def in_bounds(x, y):
    return 0 <= x < 8 and 0 <= y < 8

def get_legal_moves(board, x, y):
    piece = board.grid[y][x]
    if not piece:
        return []

    moves = []

    def add_if_valid(nx, ny):
        if 0 <= nx < 8 and 0 <= ny < 8:
            target = board.grid[ny][nx]
            if not target or target.color != piece.color:
                moves.append((nx, ny))
            return target is None
        return False

    if piece.name == "pawn":
        direction = -1 if piece.color == 0 else 1
        ny = y + direction
        if 0 <= ny < 8:
            if board.grid[ny][x] is None:
                moves.append((x, ny))
            for dx in (-1, 1):
                nx = x + dx
                if 0 <= nx < 8:
                    target = board.grid[ny][nx]
                    if target and target.color != piece.color:
                        moves.append((nx, ny))

    elif piece.name in ("rook", "bishop", "queen"):
        dirs = []
        if piece.name in ("rook", "queen"):
            dirs += [(1,0), (-1,0), (0,1), (0,-1)]
        if piece.name in ("bishop", "queen"):
            dirs += [(1,1), (1,-1), (-1,1), (-1,-1)]
        for dx, dy in dirs:
            nx, ny = x, y
            while add_if_valid(nx + dx, ny + dy):
                nx += dx
                ny += dy

    elif piece.name == "knight":
        for dx, dy in [(1,2),(2,1),(-1,2),(-2,1),(1,-2),(2,-1),(-1,-2),(-2,-1)]:
            nx, ny = x+dx, y+dy
            add_if_valid(nx, ny)

    elif piece.name == "king":
        for dx in (-1,0,1):
            for dy in (-1,0,1):
                if dx==dy==0:
                    continue
                add_if_valid(x+dx, y+dy)
    return moves


def get_sliding_moves(board, x, y, directions):
    moves = []
    color = board.grid[y][x].color
    for dx, dy in directions:
        nx, ny = x+dx, y+dy
        while in_bounds(nx, ny):
            t = board.grid[ny][nx]
            if t:
                if t.color != color:
                    moves.append((nx, ny))
                break
            moves.append((nx, ny))
            nx += dx
            ny += dy
    return moves
