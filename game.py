import pygame
from pygame.locals import *
import tetris

SPEED = 5

def run():
    pygame.init()
    game = tetris.Tetris()
    game.update()
    game.draw()
    pygame.display.flip()
    clock = pygame.time.Clock()

    while 1:
        clock.tick(SPEED)

        if game.is_game_over():
            return

        key = None

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                key = event.key

        game.tick(key)
        game.update()
        game.draw()
        pygame.display.flip()

if __name__ == "__main__":
    run()