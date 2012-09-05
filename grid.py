import shapes
import random

BOX_LENGTH = shapes.BOX_LENGTH
COLUMN_COUNT = 10
ROW_COUNT = COLUMN_COUNT * 2
SCREEN_WIDTH = COLUMN_COUNT * BOX_LENGTH
SCREEN_HEIGHT = SCREEN_WIDTH * 2

# The grid has a buffer where new shapes are initialized.
# The buffer area does not render initially.
# The tallest shape is the bar, which is 4 boxes high, so the maximum buffer height is 4 boxes.
NEW_SHAPE_BUFFER_LENGTH = 4
GRID_ROW_COUNT = ROW_COUNT + NEW_SHAPE_BUFFER_LENGTH
START_X = COLUMN_COUNT // 2 - 1
START_Y = ROW_COUNT - 1
START_POS_SCREEN = (START_X * BOX_LENGTH, ROW_COUNT - START_Y)
START_POS_GRID = shapes.Coords(START_X, START_Y)

# TODO: Rename to Tetris and try renaming the module as well but not to Tetris.
class Grid():
    def __init__(self):
        """
        Create the grid that represents the Tetris logical surfrace.
        """
        self.grid = []

        for x in range(COLUMN_COUNT):
            self.grid.append([None] * GRID_ROW_COUNT)

    def is_shape_placed(self, shape):
        if self.has_box_at_grid_bottom(shape):
            return 1
        elif self.has_box_below(shape):
            return 1
        return 0

    def has_box_at_grid_bottom(self, shape):
        for box in shape.boxes:
            if not box.grid_pos.y:
                return 1
        return 0

    def has_box_below(self, shape):
        for box in shape.boxes:
            if self.grid[box.grid_pos.x][box.grid_pos.y - 1]:
                return 1
        return 0

    def mark_shape_place(self, shape):
        for box in shape.boxes:
            self.grid[box.grid_pos.x][box.grid_pos.y] = box

    def can_shape_move_left(self, shape):
        for box in shape.boxes:
            if not box.grid_pos.x or\
               self.grid[box.grid_pos.x - 1][box.grid_pos.y]:
                return 0
        return 1

    def can_shape_move_right(self, shape):
        for box in shape.boxes:
            if box.grid_pos.x == (COLUMN_COUNT - 1) or\
               self.grid[box.grid_pos.x + 1][box.grid_pos.y]:
                return 0
        return 1

    def create_active_shape(self):
        shape_type = random.choice(
            [shapes.Bar, shapes.Square,
             shapes.Cane, shapes.ZigZag])

        return shape_type(START_POS_GRID)