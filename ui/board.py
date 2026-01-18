import pygame

TILE = 80

class BoardUI:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.font = pygame.font.SysFont("dejavusans", 48)

    def draw(self):
        for y in range(8):
            for x in range(8):
                color = (240,217,181) if (x+y)%2==0 else (181,136,99)
                pygame.draw.rect(self.screen, color,
                    (x*TILE, y*TILE, TILE, TILE))

                # highlight legal moves
                if (x,y) in self.game.legal_moves:
                    pygame.draw.rect(
                        self.screen,
                        (0,255,0),
                        (x*TILE, y*TILE, TILE, TILE),
                        4
                    )

                piece = self.game.board.grid[y][x]
                if piece:
                    text = self.font.render(piece.symbol, True, (0,0,0))
                    self.screen.blit(text, (x*TILE+20, y*TILE+10))

    def handle_click(self, pos):
        x = pos[0] // TILE
        y = pos[1] // TILE
        self.game.select(x, y)
