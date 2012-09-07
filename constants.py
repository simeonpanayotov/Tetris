# Shape constants
IMAGES = "images"
CANNOT_LOAD_IMAGE = "Cannot load image:"
BRICK_PNG = "brick.png"
BOX_LENGTH = 30

# Grid constants
BOX_LENGTH = BOX_LENGTH
COLUMN_COUNT = 10
ROW_COUNT = COLUMN_COUNT * 2
SCREEN_WIDTH = COLUMN_COUNT * BOX_LENGTH
SCREEN_HEIGHT = SCREEN_WIDTH * 2

START_X = COLUMN_COUNT // 2 - 1
START_Y = 0
START_POS_SCREEN = (START_X * BOX_LENGTH, START_Y)
START_POS_GRID = [START_X, START_Y]

# Tetris game constants
TETRIS = "Tetris"
BG_COLOR = (219, 203, 138)
PANEL_WIDTH = 150
WIDTH = SCREEN_WIDTH + PANEL_WIDTH

# Panels constants
PANEL_HEIGHT_NEXT_SHAPE = 100
PANEL_BG_COLOR = (255, 127, 39)