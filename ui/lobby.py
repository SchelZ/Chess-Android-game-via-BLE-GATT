import pygame

class Lobby:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 42)
        self.sessions = []

    def draw(self):
        self.screen.fill((25,25,25))
        t = self.font.render("BLE CHESS LOBBY", True, (255,255,255))
        self.screen.blit(t, (120, 80))

        y = 200
        for s in self.sessions:
            txt = self.font.render(s, True, (0,255,0))
            self.screen.blit(txt, (150, y))
            y += 70
