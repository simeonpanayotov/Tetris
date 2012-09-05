__author__ = 'simeon'

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
    active_shape = tetris.create_active_shape()
    active_boxes = pygame.sprite.RenderPlain(active_shape.boxes)
    placed_boxes = pygame.sprite.RenderPlain()

    screen.blit(background, (0, 0))
    active_boxes.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        clock.tick(SPEED)

        if tetris.is_shape_placed(active_shape):
            active_boxes.remove(active_shape.boxes)
            placed_boxes.add(active_shape.boxes)
            tetris.mark_shape_place(active_shape)

            active_shape = tetris.create_active_shape()
            active_boxes.add(active_shape.boxes)
            continue

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and tetris.can_shape_move_left(active_shape):
                    active_shape.move_left()
                elif event.key == K_RIGHT and tetris.can_shape_move_right(active_shape):
                    active_shape.move_right()

        active_shape.move_down()

        screen.blit(background, (0, 0))
        active_boxes.update()
        active_boxes.draw(screen)
        placed_boxes.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    run()