"""Define game-running code.

Methods:
run - runs the game

"""

import pygame
from pygame.locals import *
import tetris

def run():
    """Run the game.

    The game advances with a step depending on the current game level.
    The game stops when no new shapes can be placed. Then, the
    game over message is displayed.
    The game quits when the user closes the window.

    """
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