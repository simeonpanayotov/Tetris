"""Define shapes and their building blocks.

load_image(name) - loads an image from the 'images' folder
Block - represents a positioned sprite
Shape - implements the base shape operations
VerticalShape - an abstract shape with two states - vertical and horizontal
Square - a square shape
Bar - a four-block bar
ZigZag - a zig zag shape
Cane - a shape in the form of a cane

"""
import os
import pygame
from constants import *

def load_image(name):
    """Load an image from the 'images' folder in the project.

    Arguments:
    name - the name of the image

    Returns:
    image - the loaded image, scaled to the BOX_LENGTH value
    rectangle - the rectangle of the image

    """
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

    """Represents the building block of all shapes.

    Blocks are sprites and have a pair of coordinates,
    which represent their position in an arbitrary grid.

    Attributes:
    image - holds the loaded sprite
    rect - the rectangle of the image used by pygame
    x - the x-coordinate
    y - the y-coordinate

    Methods:
    move_down - moves the block downards by one
    move_left - moves the block on the left by one
    move_right - moves the block on the right by one
    move_up - moves the block upwards by one
    update - updates the image rectangle with the new coordinates

    """

    def __init__(self, x, y):
        """Create a block on a given position.

        Load the default brick image as the image of the sprite.

        """
        pygame.sprite.Sprite.__init__(self)

        self.image, self.rect = load_image(BRICK_PNG)
        self.rect.topleft = (x * BOX_LENGTH, y * BOX_LENGTH)
        self.x = x
        self.y = y

    def move_down(self):
        """Increase the y-coordinate with one."""
        self.y += 1

    def move_left(self):
        """Decrease the x-coordinate with one."""
        self.x -= 1

    def move_right(self):
        """Increase the x-coordinate with one."""
        self.x += 1

    def move_up(self):
        """Decrease the y-coordinate with one."""
        self.y -= 1

    def update(self):
        """Update the block image rectangle with the new coordinates."""
        self.rect.topleft = (self.x * BOX_LENGTH, self.y * BOX_LENGTH)

class Shape():

    """Define the base operations of all shapes.

    Use one of the concrete shapes - Bar, Square, ZigZag or Cane.

    Attributes:
    blocks - holds the blocks that the shape consists of

    Methods:
    move_down - moves the shape and all its blocks downwards by one
    move_left - moves the shape and all its blocks on the left by one
    move_right - moves the shape and all its blocks on the right by one
    move_up - moves the shape and all its blocks upwards by one
    move_right_to_position - moves the shape to the right to a position
    clear_blocks - clears block references of the shape
    rotate - rotates the shape by a predefined step

    """

    def __init__(self):
        """Create a new shape."""
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
        """Move the shape blocks downwards by one."""
        for block in self.blocks:
            block.move_down()

    def move_left(self):
        """Move the shape blocks on the left by one."""
        for block in self.blocks:
            block.move_left()

    def move_right(self):
        """Move the shape blocks on the right by one."""
        for block in self.blocks:
            block.move_right()

    def move_up(self):
        """Move the shape blocks upwards by one."""
        for block in self.blocks:
            block.move_up()

    def clear_blocks(self):
        """Remove all references to the shape's blocks."""
        self.blocks = []
        self._center_block = None

    def move_right_to_position(self, x):
        """"Move the shape to the right until it reaches the given x-coord.

        The shape reaches the destination when its center block
        reaches the given x-coord.

        """
        while self._center_block.x != x:
            self.move_right()

    def rotate(self, grid, validate_new_position=True):
        """Rotate the shape.

        The shape rotates by a predetermined step.
        If the new shape position is invalid in the parent grid,
        the shape returns to its original position.

        Arguments:
        grid - the grid where the shape lives

        Keyword arguments:
        validate_new_position - indicates where the new position
        is to be validated in the parent grid (Default: True).

        """

        transform = self._get_next_transform()
        self._rotate(transform)

        if not validate_new_position or self._is_position_valid(grid):
            self._confirm_next_position()
        else:
            transform = self._negate_transform(transform)
            self._rotate(transform)

class Square(Shape):
    """A square shape consisting of 4 blocks."""
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

    """An abstract shape with two states - horizontal and vertical.

    Use one of the concrete shapes inheriting it - Bar and ZigZag.

    """

    def __init__(self):
        Shape.__init__(self)

    def _get_next_transform(self):
        pass

    def _confirm_next_position(self):
        self._vertical = not self._vertical

class Bar(VerticalShape):

    """A bar shape consisting of 4 blocks.

    Its original position is vertical.

    """

    _vertical_transform = {
        0: (1, -1),
        1: (0, 0),
        2: (-1, 1),
        3: (-2, 2)
    }

    _horizontal_transform = {
        0: (-1, 1),
        1: (0, 0),
        2: (1, -1),
        3: (2, -2)
    }

    def __init__(self, x, y):
        """Create a new bar shape at the given coordinates."""
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

    """A zig-zag shape consisting of 4 blocks.

    Its original position is vertical.

    """

    _vertical_transform = {
        0: (0, 1),
        1: (-1, 2),
        2: (0, -1),
        3: (-1, 0)
    }

    _horizontal_transform = {
        0: (0, -1),
        1: (1, -2),
        2: (0, 1),
        3: (1, 0)
    }

    def __init__(self, x, y):
        """Create a new zig-zag shape at the given coordinates."""
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

    """A cane-shaped shaped consisting of four blocks.

    Has four positions: top, right, bottom, left.
    The shape rotates by one step in the same order.

    Its original position is top.

    """

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
        """Create a cane shape at the given coordinates."""
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