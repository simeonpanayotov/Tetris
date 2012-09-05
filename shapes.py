import os
import pygame

BOX_LENGTH = 30

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

    def update(self):
        self.rect.topleft = (self.x * BOX_LENGTH, self.y * BOX_LENGTH)

class Shape():
    def __init__(self):
        self.boxes = []

    def move_down(self):
        for box in self.boxes:
            box.move_down()

    def move_left(self):
        for box in self.boxes:
            box.move_left()

    def move_right(self):
        for box in self.boxes:
            box.move_right()

    def rotate(self, grid):
        transform = self._get_next_transform()
        self._rotate(transform)

        if self._is_position_valid(grid):
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

class Bar(Shape):
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
        Shape.__init__(self)

        self.vertical = True

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x, y + 1))
        self.boxes.append(Box(x, y + 2))
        self.boxes.append(Box(x, y + 3))

    def _get_next_transform(self):
        if self.vertical:
            return Bar._horizontal_transform
        else:
            return Bar._vertical_transform

    def _confirm_next_position(self):
        self.vertical = not self.vertical


class Cane(Shape):
    def __init__(self, x, y):
        Shape.__init__(self)

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x + 1, y))
        self.boxes.append(Box(x, y + 1))
        self.boxes.append(Box(x, y + 2))

class ZigZag(Shape):
    def __init__(self, x, y):
        Shape.__init__(self)

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x + 1, y))
        self.boxes.append(Box(x - 1, y + 1))
        self.boxes.append(Box(x, y + 1))