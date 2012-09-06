import shapes
import random
import pygame
from pygame import *
from constants import *

class Grid:
    """A Base class for all grids used in the game."""
    def __init__(self, row_count, column_count):
        self.grid = []
        self._row_count = row_count
        self._column_count = column_count
        self.active_shape = None
        self._active_boxes = pygame.sprite.RenderPlain()

        while len(self.grid) < column_count:
            self.grid.append([None] * row_count)

    def draw(self, screen):
        self._active_boxes.draw(screen)

    def update(self):
        self._active_boxes.update()

    def _has_shape_block_outside_top(self, shape):
        for block in shape.boxes:
            if block.y < 0:
                return True
        return False

    def _has_shape_block_at_top(self, shape):
        for block in shape.boxes:
            if block.y == 0:
                return True
        return False

    def _move_shape_to_top(self, shape):
        while self._has_shape_block_outside_top(shape):
            shape.move_down()

        while not self._has_shape_block_at_top(shape):
            shape.move_up()

    def _create_new_shape(self):
        shape_type = random.choice(
            [shapes.Square, shapes.Bar,
             shapes.ZigZag, shapes.Cane])
        shape = shape_type(START_X, START_Y)

        rotations_count = random.choice(range(1, 5))

        while rotations_count > 0:
            shape.rotate(self.grid, False)
            rotations_count -= 1

        return shape

class NextShapeGrid(Grid):
    """A grid used to display the next shape."""
    def __init__(self, row_count, column_count):
        Grid.__init__(self, row_count, column_count)

    def create_new_shape(self):
        """Creates a new shape and places it at the top left corner.
        The previous shape is cleared.

        """
        self._clear()

        shape = self._create_new_shape()
        self._move_shape_to_left(shape)
        self._move_shape_to_top(shape)
        self.active_shape = shape
        self._active_boxes.add(shape.boxes)

    def _clear(self):
        """Clears the grid from all blocks/shapes currently in it."""
        if self.active_shape:
            self._active_boxes.remove(self.active_shape.boxes)
            self.active_shape = None

    def _has_shape_block_outside_left(self, shape):
        for block in shape.boxes:
            if block.x < 0:
                return True
        return False

    def _has_shape_block_at_left(self, shape):
        for block in shape.boxes:
            if block.x == 0:
                return True
        return False

    def _move_shape_to_left(self, shape):
        while self._has_shape_block_outside_left(shape):
            shape.move_right()

        while not self._has_shape_block_at_left(shape):
            shape.move_left()

class GameGrid:
    def __init__(self):
        """
        Create the grid that represents the Tetris logical surface.
        """
        self.grid = []

        while len(self.grid) < COLUMN_COUNT:
            self.grid.append([None] * ROW_COUNT)

        self.active_shape = None
        self.has_active_shape = False
        self.active_boxes = pygame.sprite.RenderPlain()
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
            self._collapse_blocks()
            self.has_active_shape = False
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

    def add_new_shape(self, shape):
        self.active_shape = shape
        self.active_boxes.add(shape.boxes)
        self.has_active_shape = True

        shape.move_right_to_position(START_X)

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