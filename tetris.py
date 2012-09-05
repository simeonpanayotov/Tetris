import pygame
from pygame.locals import *
import grid

TETRIS = "Tetris"
SPEED = 5
BG_COLOR = (219, 203, 138)

def run():
    pygame.init()

    # Create the game window.
    screen = pygame.display.set_mode((grid.SCREEN_WIDTH, grid.SCREEN_HEIGHT))
    pygame.display.set_caption(TETRIS)

    # Create the background surface.
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    tetris = grid.Grid()

    screen.blit(background, (0, 0))
    tetris.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        clock.tick(SPEED)

        key = None

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                key = event.key

        tetris.tick(key)

        screen.blit(background, (0, 0))
        tetris.update()
        tetris.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    run()