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

        key = None

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                key = event.key

        if game.is_game_over():
            pygame.display.flip()
        else:
            game.tick(key)
            game.update()
            game.draw()
            pygame.display.flip()

if __name__ == "__main__":
    run()