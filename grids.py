import shapes
import random
import pygame
from pygame import *
from constants import *

class Grid:
    """A Base class for all grids used in the game."""
    def __init__(self):
        self._active_shape = None
        self._active_blocks = pygame.sprite.RenderPlain()

    def _has_shape_block_outside_top(self, shape):
        for block in shape.blocks:
            if block.y < 0:
                return True
        return False

    def _has_shape_block_at_top(self, shape):
        for block in shape.blocks:
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
            shape.rotate(None, False)
            rotations_count -= 1

        return shape

    def update(self):
        self._active_blocks.update()

    def draw(self, screen):
        self._active_blocks.draw(screen)

class NextShapeGrid(Grid):
    """A grid used to display the next shape."""
    def __init__(self):
        Grid.__init__(self)

    def _clear(self):
        """Clears the grid from all blocks/shapes currently in it."""
        if self._active_shape:
            self._active_blocks.remove(self._active_shape.blocks)
            self._active_shape = None

    def _has_shape_block_outside_left(self, shape):
        for block in shape.blocks:
            if block.x < 0:
                return True
        return False

    def _has_shape_block_at_left(self, shape):
        for block in shape.blocks:
            if block.x == 0:
                return True
        return False

    def _move_shape_to_left(self, shape):
        while self._has_shape_block_outside_left(shape):
            shape.move_right()

        while not self._has_shape_block_at_left(shape):
            shape.move_left()

    def create_new_shape(self):
        """Creates a new shape and places it at the top left corner.
        The previous shape is cleared.

        """
        self._clear()

        shape = self._create_new_shape()
        self._move_shape_to_left(shape)
        self._move_shape_to_top(shape)
        self._active_shape = shape
        self._active_blocks.add(shape.blocks)

class GameGrid(Grid):
    def __init__(self):
        """
        Create the grid that represents the Tetris logical surface.
        """
        Grid.__init__(self)

        self._grid = []
        self._placed_blocks = pygame.sprite.RenderPlain()
        self.has_active_shape = False

        while len(self._grid) < COLUMN_COUNT:
            self._grid.append([None] * ROW_COUNT)

    def _place_active_shape(self):
        while not self._is_shape_placed(self._active_shape):
            self._active_shape.move_down()

    def _is_shape_placed(self, shape):
        if self._has_box_at_bottom(shape):
            return 1
        elif self._has_box_below(shape):
            return 1
        return 0

    def _has_box_at_bottom(self, shape):
        for block in shape.blocks:
            if block.y == ROW_COUNT - 1:
                return 1
        return 0

    def _has_box_below(self, shape):
        for block in shape.blocks:
            if self._grid[block.x][block.y + 1]:
                return 1
        return 0

    def _mark_shape_blocks_as_placed(self, shape):
        for block in shape.blocks:
            self._grid[block.x][block.y] = block

    def _can_shape_move_left(self, shape):
        for block in shape.blocks:
            if not block.x or\
               self._grid[block.x - 1][block.y]:
                return 0
        return 1

    def _can_shape_move_right(self, shape):
        for block in shape.blocks:
            if block.x == (COLUMN_COUNT - 1) or\
               self._grid[block.x + 1][block.y]:
                return 0
        return 1

    def _get_blocks(self, row_index):
        blocks = []
        for column_index in range(COLUMN_COUNT):
            block = self._grid[column_index][row_index]

            if block:
                blocks.append(block)

        return blocks

    def _remove_placed_blocks(self, blocks):
        for block in blocks:
            self._grid[block.x][block.y] = None

        self._placed_blocks.remove(blocks)

    def _move_above_blocks_down(self, start_row_index):
        for column_index in range(COLUMN_COUNT):
            row_index = start_row_index
            while row_index >= 0:
                block = self._grid[column_index][row_index]

                if block:
                    block.move_down()
                    self._grid[column_index][row_index] = None
                    self._grid[block.x][block.y] = block

                row_index -= 1

    def _collapse_blocks(self):
        row_index = 0
        collapsed_row_count = 0

        while row_index <= ROW_COUNT - 1:
            blocks = self._get_blocks(row_index)

            if len(blocks) == COLUMN_COUNT:
                self._remove_placed_blocks(blocks)
                self._move_above_blocks_down(row_index - 1)
                collapsed_row_count += 1

            row_index += 1

        return collapsed_row_count

    def tick(self, key):
        if key:
            if key == K_LEFT and self._can_shape_move_left(self._active_shape):
                self._active_shape.move_left()
            elif key == K_RIGHT and self._can_shape_move_right(self._active_shape):
                self._active_shape.move_right()
            elif key == K_UP:
                self._active_shape.rotate(self._grid)
            elif key == K_SPACE:
                self._place_active_shape()

        if self._is_shape_placed(self._active_shape):
            self._active_blocks.remove(self._active_shape.blocks)
            self._placed_blocks.add(self._active_shape.blocks)
            self._mark_shape_blocks_as_placed(self._active_shape)
            self._active_shape.clear_blocks()
            self.has_active_shape = False

            return self._collapse_blocks()
        else:
            self._active_shape.move_down()

        return 0

    def add_new_shape(self, shape):
        self._active_shape = shape
        self._active_blocks.add(shape.blocks)
        self.has_active_shape = True

        shape.move_right_to_position(START_X)

    def is_game_over(self):
        for block in self._active_shape.blocks:
            if self._grid[block.x][block.y]:
                return 1
        return 0

    def update(self):
        self._active_blocks.update()
        self._placed_blocks.update()

    def draw(self, screen):
        self._active_blocks.draw(screen)
        self._placed_blocks.draw(screen)