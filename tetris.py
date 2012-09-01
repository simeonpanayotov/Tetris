__author__ = 'simeon'

import pygame
from pygame.locals import *

#TODO: move the constants to a separate module
BOX_LENGTH = 40
COLUMN_COUNT = 10
ROW_COUNT = COLUMN_COUNT * 2
SCREEN_WIDTH = COLUMN_COUNT * BOX_LENGTH
SCREEN_HEIGHT = SCREEN_WIDTH * 2
BG_COLOR = (219, 203, 138)

def run():
    pygame.init()

    # Setup the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Tetris")

    # Setup the background surface
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    screen.blit(background, (0, 0))
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                return

if __name__ == "__main__":
    run()