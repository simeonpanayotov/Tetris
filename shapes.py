import os
import pygame
from constants import *

def load_image(name):
    fullname = os.path.abspath(os.path.join(IMAGES, name))

    try:
        image = pygame.image.load(fullname)
    except pygame.error as err:
        print(CANNOT_LOAD_IMAGE, name)
        raise SystemExit(err.args)

    image = image.convert()
    scaled_image = pygame.Surface((BOX_LENGTH, BOX_LENGTH))
    pygame.transform.scale(image, (BOX_LENGTH, BOX_LENGTH), scaled_image)

    return scaled_image, scaled_image.get_rect()

class Block(pygame.sprite.Sprite):
    """Represents a block of which the various Tetris shapes
    are built from. Blocks are sprites and have a pari of coordinates,
    which represent their position in an arbitrary grid.

    """
    def __init__(self, x, y):
        """Creates a block on a given position."""
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image(BRICK_PNG)
        self.rect.topleft = (x * BOX_LENGTH, y * BOX_LENGTH)
        self.x = x
        self.y = y

    def move_down(self):
        self.y += 1

    def move_left(self):
        self.x -= 1

    def move_right(self):
        self.x += 1

    def move_up(self):
        self.y -= 1

    def update(self):
        self.rect.topleft = (self.x * BOX_LENGTH, self.y * BOX_LENGTH)

class Shape():
    def __init__(self):
        self.blocks = []
        self._center_block = None

    def _get_next_transform(self):
        return {}

    def _confirm_next_position(self):
        pass

    def _is_position_valid(self, grid):
        column_count = len(grid)
        row_count = len(grid[0])

        for box in self.blocks:
            if box.x < 0 or box.x >= column_count or\
               box.y >= row_count or\
               grid[box.x][box.y]:
                return 0
        return 1

    def _negate_transform(self, transform):
        negated_transform = {}

        for key in transform:
            negated_transform[key] = (transform[key][0] * -1,
                                      transform[key][1] * -1)

        return negated_transform

    def _rotate(self, transform):
        for key in transform:
            self.blocks[key].x += transform[key][0]
            self.blocks[key].y += transform[key][1]

    def move_down(self):
        for block in self.blocks:
            block.move_down()

    def move_left(self):
        for block in self.blocks:
            block.move_left()

    def move_right(self):
        for block in self.blocks:
            block.move_right()

    def move_up(self):
        for block in self.blocks:
            block.move_up()

    def clear_blocks(self):
        self.blocks = []
        self._center_block = None

    def move_right_to_position(self, x):
        while self._center_block.x != x:
            self.move_right()

    def rotate(self, grid, validate_new_position=True):
        transform = self._get_next_transform()
        self._rotate(transform)

        if not validate_new_position or self._is_position_valid(grid):
            self._confirm_next_position()
        else:
            transform = self._negate_transform(transform)
            self._rotate(transform)

class Square(Shape):
    def __init__(self, x, y):
        Shape.__init__(self)

        # upper left
        self.blocks.append(Block(x, y))
        # upper right
        self.blocks.append(Block(x + 1, y))
        # lower left
        self.blocks.append(Block(x, y + 1))
        # lower right
        self.blocks.append(Block(x + 1, y + 1))

        self._center_block = self.blocks[0]

class VerticalShape(Shape):
    def __init__(self):
        Shape.__init__(self)

    def _get_next_transform(self):
        pass

    def _confirm_next_position(self):
        self._vertical = not self._vertical

class Bar(VerticalShape):
    #TODO: check conventions!!!
    _vertical_transform = {
        0: (1, -1),
        1: (0, 0),
        2: (-1, 1),
        3: (-2, 2)
    }
    #TODO: check conventions!!!
    _horizontal_transform = {
        0: (-1, 1),
        1: (0, 0),
        2: (1, -1),
        3: (2, -2)
    }

    def __init__(self, x, y):
        VerticalShape.__init__(self)

        self._vertical = True

        self.blocks.append(Block(x, y))
        self.blocks.append(Block(x, y + 1))
        self.blocks.append(Block(x, y + 2))
        self.blocks.append(Block(x, y + 3))

        self._center_block = self.blocks[0]

    def _confirm_next_position(self):
        VerticalShape._confirm_next_position(self)

        if self._vertical:
            self._center_block = self.blocks[0]
        else:
            self._center_block = self.blocks[1]

    def _get_next_transform(self):
        if self._vertical:
            return Bar._horizontal_transform
        else:
            return Bar._vertical_transform

class ZigZag(VerticalShape):
    #TODO: check conventions!!!
    _vertical_transform = {
        0: (0, 1),
        1: (-1, 2),
        2: (0, -1),
        3: (-1, 0)
    }
    #TODO: check conventions!!!
    _horizontal_transform = {
        0: (0, -1),
        1: (1, -2),
        2: (0, 1),
        3: (1, 0)
    }

    def __init__(self, x, y):
        VerticalShape.__init__(self)

        self._vertical = False

        self.blocks.append(Block(x, y))
        self.blocks.append(Block(x + 1, y))
        self.blocks.append(Block(x - 1, y + 1))
        self.blocks.append(Block(x, y + 1))

        self._center_block = self.blocks[0]

    def _confirm_next_position(self):
        VerticalShape._confirm_next_position(self)

        if self._vertical:
            self._center_block = self.blocks[3]
        else:
            self._center_block = self.blocks[0]

    def _get_next_transform(self):
        if self._vertical:
            return ZigZag._horizontal_transform
        else:
            return ZigZag._vertical_transform

class Cane(Shape):
    _right_transform = {
        0: (1, 0),
        1: (0, 1),
        2: (0, -1),
        3: (-1, -2)
    }

    _bottom_transform = {
        0: (-1, 2),
        1: (0, 1),
        2: (1, 1),
        3: (2, 0)
    }

    _left_transform = {
        0: (-1, -1),
        1: (-2, -2),
        2: (-1, 0),
        3: (0, 1)
    }

    _top_transform = {
        0: (1, -1),
        1: (2, 0),
        2: (0, 0),
        3: (-1, 1)
    }

    def __init__(self, x, y):
        Shape.__init__(self)

        self._position = 0

        self.blocks.append(Block(x, y))
        self.blocks.append(Block(x + 1, y))
        self.blocks.append(Block(x, y + 1))
        self.blocks.append(Block(x, y + 2))

        self._center_block = self.blocks[0]

    def _confirm_next_position(self):
        self._position = self._get_next_position()

        if self._position == 0 or self._position == 2:
            self._center_block = self.blocks[0]
        elif self._position == 1 or self._position == 3:
            self._center_block = self.blocks[2]

    def _get_next_transform(self):
        next_position = self._get_next_position()

        if next_position == 0:
            return Cane._top_transform
        elif next_position == 1:
            return Cane._right_transform
        elif next_position == 2:
            return Cane._bottom_transform
        else:
            return Cane._left_transform

    def _get_next_position(self):
        next_position = self._position + 1

        if next_position > 3:
            next_position = 0

        return next_position