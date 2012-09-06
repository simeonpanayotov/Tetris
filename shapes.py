import os
import pygame
from constants import *

def load_image(name):
    fullname = os.path.abspath(os.path.join("data", name))
#    TODO: Fix the exception handling/raising code.
#    try:
    image = pygame.image.load(fullname)
#    except pygame.error as err:
#        print ('Cannot load image:', name)
#        raise SystemExit(err.args)
    image = image.convert()
    scaled_image = pygame.Surface((BOX_LENGTH, BOX_LENGTH))
    pygame.transform.scale(image, (BOX_LENGTH, BOX_LENGTH), scaled_image)

    return scaled_image, scaled_image.get_rect()

class Box(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # Call Sprite initializer.

        self.image, self.rect = load_image("brick.png")
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
        self.boxes = []
        self._center_block = None

    def move_down(self):
        for box in self.boxes:
            box.move_down()

    def move_left(self):
        for box in self.boxes:
            box.move_left()

    def move_right(self):
        for box in self.boxes:
            box.move_right()

    def move_up(self):
        for box in self.boxes:
            box.move_up()

    def clear_blocks(self):
        self.boxes = []
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

    def _get_next_transform(self):
        return {}

    def _confirm_next_position(self):
        pass

    def _is_position_valid(self, grid):
        column_count = len(grid)
        row_count = len(grid[0])

        for box in self.boxes:
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
            self.boxes[key].x += transform[key][0]
            self.boxes[key].y += transform[key][1]

class Square(Shape):
    def __init__(self, x, y):
        Shape.__init__(self)

        # upper left
        self.boxes.append(Box(x, y))
        # upper right
        self.boxes.append(Box(x + 1, y))
        # lower left
        self.boxes.append(Box(x, y + 1))
        # lower right
        self.boxes.append(Box(x + 1, y + 1))

        self._center_block = self.boxes[0]

class VerticalShape(Shape):
    def __init__(self):
        Shape.__init__(self)

    def _get_next_transform(self):
        pass

    def _confirm_next_position(self):
        self.vertical = not self.vertical

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

        self.vertical = True

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x, y + 1))
        self.boxes.append(Box(x, y + 2))
        self.boxes.append(Box(x, y + 3))

        self._center_block = self.boxes[0]

    def _confirm_next_position(self):
        VerticalShape._confirm_next_position(self)

        if self.vertical:
            self._center_block = self.boxes[0]
        else:
            self._center_block = self.boxes[1]

    def _get_next_transform(self):
        if self.vertical:
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

        self.vertical = False

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x + 1, y))
        self.boxes.append(Box(x - 1, y + 1))
        self.boxes.append(Box(x, y + 1))

        self._center_block = self.boxes[0]

    def _confirm_next_position(self):
        VerticalShape._confirm_next_position(self)

        if self.vertical:
            self._center_block = self.boxes[3]
        else:
            self._center_block = self.boxes[0]

    def _get_next_transform(self):
        if self.vertical:
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

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x + 1, y))
        self.boxes.append(Box(x, y + 1))
        self.boxes.append(Box(x, y + 2))

        self._center_block = self.boxes[0]

    def _confirm_next_position(self):
        self._position = self._get_next_position()

        if self._position == 0 or self._position == 2:
            self._center_block = self.boxes[0]
        elif self._position == 1 or self._position == 3:
            self._center_block = self.boxes[2]

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