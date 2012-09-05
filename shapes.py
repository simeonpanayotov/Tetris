__author__ = 'simeon'

import os
import pygame

BOX_LENGTH = 40

def load_image(name):
    fullname = os.path.abspath(os.path.join("data", name))
#    TODO: Fix the exception handling/raising code.
#    try:
    image = pygame.image.load(fullname)
#    except pygame.error as err:
#        print ('Cannot load image:', name)
#        raise SystemExit(err.args)
    image = image.convert()

    return image, image.get_rect()

class Box(pygame.sprite.Sprite):
    def __init__(self, topleft, grid_pos):
        pygame.sprite.Sprite.__init__(self) # Call Sprite initializer.

        self.image, self.rect = load_image("brick.png")
        self.rect.topleft = topleft
        self.grid_pos = grid_pos
        self.reinit()

    def reinit(self):
        self.move_pos = (0, 0)

    def move_down(self):
        self.move_pos = (self.move_pos[0], self.move_pos[1] + BOX_LENGTH)
        self.grid_pos = (self.grid_pos[0], self.grid_pos[1] - 1)

    def move_left(self):
        self.move_pos = (self.move_pos[0] - BOX_LENGTH, self.move_pos[1])
        self.grid_pos = (self.grid_pos[0] - 1, self.grid_pos[1])

    def move_right(self):
        self.move_pos = (self.move_pos[0] + BOX_LENGTH, self.move_pos[1])
        self.grid_pos = (self.grid_pos[0] + 1, self.grid_pos[1])

    def update(self):
        new_pos = self.rect.move(self.move_pos)
        self.rect = new_pos

        self.reinit()

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

class SquareShape(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        # upper left
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH, -BOX_LENGTH), (grid_pos[0], grid_pos[1] + 1)))
        # upper right
        self.boxes.append(Box(((grid_pos[0] + 1) * BOX_LENGTH, -BOX_LENGTH), ((grid_pos[0] + 1), grid_pos[1] + 1)))
        # lower left
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH, 0), grid_pos))
        # lower right
        self.boxes.append(Box(((grid_pos[0] + 1) * BOX_LENGTH, 0), (grid_pos[0] + 1, grid_pos[1])))

class BarShape(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  -3 * BOX_LENGTH), (grid_pos[0], grid_pos[1] + 3)))
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  -2 * BOX_LENGTH), (grid_pos[0], grid_pos[1] + 2)))
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  -1 * BOX_LENGTH), (grid_pos[0], grid_pos[1] + 1)))
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  0), grid_pos))

class CaneShape(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  -2 * BOX_LENGTH), (grid_pos[0], grid_pos[1] + 2)))
        self.boxes.append(Box(((grid_pos[0] + 1) * BOX_LENGTH,  -2 * BOX_LENGTH), (grid_pos[0] + 1, grid_pos[1] + 2)))
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  -BOX_LENGTH), (grid_pos[0], grid_pos[1] + 1)))
        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  0), grid_pos))

class ZigZagShape(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box((grid_pos[0] * BOX_LENGTH,  0), grid_pos))
        self.boxes.append(Box(((grid_pos[0] + 1) * BOX_LENGTH,  -BOX_LENGTH), (grid_pos[0] + 1, grid_pos[1] + 1)))
        self.boxes.append(Box(((grid_pos[0] + 1) * BOX_LENGTH,  0), (grid_pos[0] + 1, grid_pos[1])))
        self.boxes.append(Box(((grid_pos[0] + 2) * BOX_LENGTH,  -BOX_LENGTH), (grid_pos[0] + 2, grid_pos[1] + 1)))