import pygame, sys
from level import Level
from settings import *

# Create an game class with init inside
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Prison Island')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick() / 1000
            self.level.run(dt)
            pygame.display.update()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL] and keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()
