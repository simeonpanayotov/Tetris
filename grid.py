import shapes
import random
import pygame
from pygame import *

BOX_LENGTH = shapes.BOX_LENGTH
COLUMN_COUNT = 10
ROW_COUNT = COLUMN_COUNT * 2
SCREEN_WIDTH = COLUMN_COUNT * BOX_LENGTH
SCREEN_HEIGHT = SCREEN_WIDTH * 2

START_X = COLUMN_COUNT // 2 - 1
START_Y = 0
START_POS_SCREEN = (START_X * BOX_LENGTH, START_Y)
START_POS_GRID = [START_X, START_Y]

# TODO: Rename to Tetris and try renaming the module as well but not to Tetris.
class Grid():
    def __init__(self):
        """
        Create the grid that represents the Tetris logical surface.
        """
        self.grid = []

        while len(self.grid) <= COLUMN_COUNT:
            self.grid.append([None] * ROW_COUNT)

        active_shape = self.active_shape = self._place_new_shape()
        self.active_boxes = pygame.sprite.RenderPlain(active_shape.boxes)
        self.placed_boxes = pygame.sprite.RenderPlain()

    def tick(self, key):
        if key:
            if key == K_LEFT and self.can_shape_move_left(self.active_shape):
                self.active_shape.move_left()
            elif key == K_RIGHT and self.can_shape_move_right(self.active_shape):
                self.active_shape.move_right()
            elif key == K_UP:
                self.active_shape.rotate(self.grid)
            elif key == K_SPACE:
                self.place_active_shape()

        if self.is_shape_placed(self.active_shape):
            self.active_boxes.remove(self.active_shape.boxes)
            self.placed_boxes.add(self.active_shape.boxes)
            self.mark_shape_place(self.active_shape)

            self.active_shape = self._place_new_shape()
            self.active_boxes.add(self.active_shape.boxes)
        else:
            self.active_shape.move_down()

    def is_game_over(self):
        for box in self.active_shape.boxes:
            if self.grid[box.x][box.y]:
                return 1
        return 0

    def place_active_shape(self):
        while not self.is_shape_placed(self.active_shape):
            self.active_shape.move_down()

    def draw(self, screen):
        self.active_boxes.draw(screen)
        self.placed_boxes.draw(screen)

    def update(self):
        self.active_boxes.update()
        self.placed_boxes.update()

    def is_shape_placed(self, shape):
        if self.has_box_at_grid_bottom(shape):
            return 1
        elif self.has_box_below(shape):
            return 1
        return 0

    def has_box_at_grid_bottom(self, shape):
        for box in shape.boxes:
            if box.y == ROW_COUNT - 1:
                return 1
        return 0

    def has_box_below(self, shape):
        for box in shape.boxes:
            if self.grid[box.x][box.y + 1]:
                return 1
        return 0

    def mark_shape_place(self, shape):
        for box in shape.boxes:
            self.grid[box.x][box.y] = box

    def can_shape_move_left(self, shape):
        for box in shape.boxes:
            if not box.x or\
               self.grid[box.x - 1][box.y]:
                return 0
        return 1

    def can_shape_move_right(self, shape):
        for box in shape.boxes:
            if box.x == (COLUMN_COUNT - 1) or\
               self.grid[box.x + 1][box.y]:
                return 0
        return 1

    def _place_new_shape(self):
        shape_type = random.choice(
            [shapes.Bar, shapes.Square,
             shapes.Cane, shapes.ZigZag])

        return shape_type(START_X, START_Y)