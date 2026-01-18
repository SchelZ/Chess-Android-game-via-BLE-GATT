import pygame
from game.config import SCREEN_W, SCREEN_H
from transport import create_transport  ## for debuging
from game.game import Game
from ui.board import BoardUI
from game.board import Board

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Chess Debug Mode")
    
    transport = create_transport()
    board = Board()

    game = Game(board, transport)
    ui = BoardUI(screen, game)

    clock = pygame.time.Clock()
    running = True

    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if e.type in (pygame.MOUSEBUTTONDOWN, pygame.FINGERDOWN):
                if hasattr(e, 'pos'):
                    ui.handle_click(e.pos)
                else:
                    x = int(e.x * SCREEN_W)
                    y = int(e.y * SCREEN_H)
                    ui.handle_click((x, y))

        game.update()
        ui.draw()
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
