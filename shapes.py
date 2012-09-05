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

class Coords():
    def __init__(self, *args):
        """
        Creates an object representing the coordinates of a point in
        a two-dimensional coordinate system. Used for both the screen
        and grid points.
        """
        if len(args) == 1:
            self.x = args[0].x
            self.y = args[0].y
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]

    def addX(self, value):
        """
        Adds a value to the x coordinate.
        """
        self.x = self.x + value

    def addY(self, value):
        """
        Adds a value to the y coordinate.
        """
        self.y = self.y + value

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
        self.grid_pos.addY(-1)

    def move_left(self):
        self.move_pos = (self.move_pos[0] - BOX_LENGTH, self.move_pos[1])
        self.grid_pos.addX(-1)

    def move_right(self):
        self.move_pos = (self.move_pos[0] + BOX_LENGTH, self.move_pos[1])
        self.grid_pos.addX(1)

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

class Square(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        # upper left
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH, -BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 1)))
        # upper right
        self.boxes.append(Box(
            ((grid_pos.x + 1) * BOX_LENGTH, -BOX_LENGTH),
            Coords(grid_pos.x + 1, grid_pos.y + 1)))
        # lower left
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH, 0),
            Coords(grid_pos)))
        # lower right
        self.boxes.append(Box(
            ((grid_pos.x + 1) * BOX_LENGTH, 0),
            Coords(grid_pos.x + 1, grid_pos.y)))

class Bar(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  -3 * BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 3)))
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  -2 * BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 2)))
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  -1 * BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 1)))
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  0),
            Coords(grid_pos)))

class Cane(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  -2 * BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 2)))
        self.boxes.append(Box(
            ((grid_pos.x + 1) * BOX_LENGTH,  -2 * BOX_LENGTH),
            Coords(grid_pos.x + 1, grid_pos.y + 2)))
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  -BOX_LENGTH),
            Coords(grid_pos.x, grid_pos.y + 1)))
        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  0),
            Coords(grid_pos)))

class ZigZag(Shape):
    def __init__(self, grid_pos):
        Shape.__init__(self)

        self.boxes.append(Box(
            (grid_pos.x * BOX_LENGTH,  0),
            Coords(grid_pos)))
        self.boxes.append(Box(
            ((grid_pos.x + 1) * BOX_LENGTH,  -BOX_LENGTH),
            Coords(grid_pos.x + 1, grid_pos.y + 1)))
        self.boxes.append(Box(
            ((grid_pos.x + 1) * BOX_LENGTH,  0),
            Coords(grid_pos.x + 1, grid_pos.y)))
        self.boxes.append(Box(
            ((grid_pos.x + 2) * BOX_LENGTH,  -BOX_LENGTH),
            Coords(grid_pos.x + 2, grid_pos.y + 1)))