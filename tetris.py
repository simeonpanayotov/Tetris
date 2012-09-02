__author__ = 'simeon'

import random
import pygame
from pygame.locals import *
import shapes

#TODO: move the constants to a separate module
TETRIS = "Tetris"
SPEED = 5
BOX_LENGTH = shapes.BOX_LENGTH
COLUMN_COUNT = 10
ROW_COUNT = COLUMN_COUNT * 2
SCREEN_WIDTH = COLUMN_COUNT * BOX_LENGTH
SCREEN_HEIGHT = SCREEN_WIDTH * 2
BG_COLOR = (219, 203, 138)

# The tallest shape is the bar, which is 4 boxes high.
# Its bottom box is always rendered, so the buffer is three rows high (4 - 1).
NEW_SHAPE_BUFFER_LENGTH = 3
GRID_ROW_COUNT = ROW_COUNT + NEW_SHAPE_BUFFER_LENGTH
START_X = COLUMN_COUNT // 2 - 1
START_Y = ROW_COUNT - 1
START_POS_SCREEN = (START_X * BOX_LENGTH, ROW_COUNT - START_Y)
START_POS_GRID = (START_X, START_Y)

class Grid():
    def __init__(self):
        # Create the grid that defines the positioned and movable shapes.
        self.grid = []

        for x in range(COLUMN_COUNT):
            self.grid.append([None] * GRID_ROW_COUNT)

    def is_shape_placed(self, shape):
        if self.has_box_at_grid_bottom(shape):
            return 1
        elif self.has_box_below(shape):
            return 1
        return 0

    def has_box_at_grid_bottom(self, shape):
        for box in shape.boxes:
            if not box.grid_pos[1]:
                return 1
        return 0

    def has_box_below(self, shape):
        for box in shape.boxes:
            if self.grid[box.grid_pos[0]][box.grid_pos[1] - 1]:
                return 1
        return 0

    def mark_shape_place(self, shape):
        for box in shape.boxes:
            self.grid[box.grid_pos[0]][box.grid_pos[1]] = box

    def can_shape_move_left(self, shape):
        for box in shape.boxes:
            if not box.grid_pos[0] or\
               self.grid[box.grid_pos[0] - 1][box.grid_pos[1]]:
                return 0
        return 1

    def can_shape_move_right(self, shape):
        for box in shape.boxes:
            if box.grid_pos[0] == (COLUMN_COUNT - 1) or\
               self.grid[box.grid_pos[0] + 1][box.grid_pos[1]]:
                return 0
        return 1

def create_active_shape():
    shape_type = random.randrange(1, 3)

    if shape_type == 1:
        return shapes.BarShape(START_POS_GRID)

    return shapes.SquareShape(START_POS_GRID)

def run():
    pygame.init()

    # Create the game window.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TETRIS)

    # Create the background surface.
    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(BG_COLOR)

    grid = Grid()
    active_shape = create_active_shape()
    active_boxes = pygame.sprite.RenderPlain(active_shape.boxes)
    placed_boxes = pygame.sprite.RenderPlain()

    screen.blit(background, (0, 0))
    active_boxes.draw(screen)
    pygame.display.flip()

    clock = pygame.time.Clock()

    while 1:
        clock.tick(SPEED)

        if grid.is_shape_placed(active_shape):
            active_boxes.remove(active_shape.boxes)
            placed_boxes.add(active_shape.boxes)
            grid.mark_shape_place(active_shape)

            active_shape = create_active_shape()
            active_boxes.add(active_shape.boxes)
            continue

        for event in pygame.event.get():
            if event.type == QUIT:
                return
            elif event.type == KEYDOWN:
                if event.key == K_LEFT and grid.can_shape_move_left(active_shape):
                    active_shape.move_left()
                elif event.key == K_RIGHT and grid.can_shape_move_right(active_shape):
                    active_shape.move_right()

        active_shape.move_down()

        screen.blit(background, (0, 0))
        active_boxes.update()
        active_boxes.draw(screen)
        placed_boxes.draw(screen)
        pygame.display.flip()

if __name__ == "__main__":
    run()