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

        while len(self.grid) < COLUMN_COUNT:
            self.grid.append([None] * ROW_COUNT)

        active_shape = self.active_shape = self._add_new_shape()
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
            self.active_shape.clear_blocks()

            self.active_shape = self._add_new_shape()
            self.active_boxes.add(self.active_shape.boxes)
            self._collapse_blocks()
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

    def _get_blocks(self, row_index):
        blocks = []
        for column_index in range(COLUMN_COUNT):
            block = self.grid[column_index][row_index]

            if block:
                blocks.append(block)

        return blocks

    def _remove_placed_blocks(self, blocks):
        for block in blocks:
            self.grid[block.x][block.y] = None

        self.placed_boxes.remove(blocks)

    def _move_above_blocks_down(self, start_row_index):
        for column_index in range(COLUMN_COUNT):
            row_index = start_row_index
            while row_index >= 0:
                block = self.grid[column_index][row_index]

                if block:
                    block.move_down()
                    self.grid[column_index][row_index] = None
                    self.grid[block.x][block.y] = block

                row_index -= 1

    def _collapse_blocks(self):
        row_index = 0

        while row_index <= ROW_COUNT - 1:
            blocks = self._get_blocks(row_index)

            if len(blocks) == COLUMN_COUNT:
                self._remove_placed_blocks(blocks)
                self._move_above_blocks_down(row_index - 1)

            row_index += 1

    def _add_new_shape(self):
        shape_type = random.choice(
            [shapes.Square, shapes.Bar,
             shapes.ZigZag, shapes.Cane])
        shape = shape_type(START_X, START_Y)

        rotations_count = random.choice(range(1, 5))

        while rotations_count > 0:
            shape.rotate(self.grid, False)
            rotations_count -= 1

        self._place_shape_at_top(shape)

        return shape

    def _has_shape_block_above_top(self, shape):
        for block in shape.boxes:
            if block.y < 0:
                return True
        return False

    def _has_shape_block_at_top(self, shape):
        for block in shape.boxes:
            if block.y == 0:
                return True
        return False

    def _place_shape_at_top(self, shape):
        while self._has_shape_block_above_top(shape):
            shape.move_down()

        while not self._has_shape_block_at_top(shape):
            shape.move_up()