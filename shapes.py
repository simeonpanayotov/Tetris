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
        self.reinit()

    def reinit(self):
        self.screen_delta_x = 0
        self.screen_delta_y = 0

    def move_down(self):
        self.screen_delta_y = self.screen_delta_y + BOX_LENGTH
        self.y += 1

    def move_left(self):
        self.screen_delta_x = self.screen_delta_x - BOX_LENGTH
        self.x -= 1

    def move_right(self):
        self.screen_delta_x = self.screen_delta_x + BOX_LENGTH
        self.x += 1

    def update(self):
        moved_rect = self.rect.move((self.screen_delta_x, self.screen_delta_y))
        self.rect = moved_rect

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
    def __init__(self, x, y):
        Shape.__init__(self)

        self.boxes.append(Box(x, y))
        self.boxes.append(Box(x, y + 1))
        self.boxes.append(Box(x, y + 2))
        self.boxes.append(Box(x, y + 3))

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