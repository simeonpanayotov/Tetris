import pygame
from pygame.locals import *
import tetris

def run():
    pygame.init()
    game = tetris.Tetris()
    game.update()
    game.draw()
    pygame.display.flip()
    clock = pygame.time.Clock()

    while 1:
        clock.tick(game.level)

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