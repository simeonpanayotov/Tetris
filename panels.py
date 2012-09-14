"""Define panels used in the game to display information.

LabelPanel - displays static text
ValuePanel - displays variable text
NextShapePanel - displays the next shape
LevelPanel - displays the current game level
ScorePanel - dispalys the current palyer score
ControlPanel - holds all game panels

"""
import pygame
from constants import *
import grids

class LabelPanel:

    """A panel displaying static text.

    Methods:
    draw - draw the panel on a surface

    """

    def __init__(self, width, label):
        self._font = pygame.font.Font(None, 36)

        text = self._font.render(str(label), 1, (10, 10, 10))
        textpos = text.get_rect(topleft=(10, 10))

        self.height = text.get_height() + 10
        self._panel = pygame.Surface((width, self.height))
        self._panel.fill(PANEL_BG_COLOR)
        self._panel.blit(text, textpos)

    def draw(self, surface, position):
        surface.blit(self._panel, position)

class ValuePanel:

    """A panel displaying variable text.

    Methods:
    draw - draw the panel on a surface

    """

    def __init__(self, width, value):
        self.value = value
        self._font = pygame.font.Font(None, 36)

        text = self._font.render(str(value), 1, (10, 10, 10))
        textpos = text.get_rect(topleft=(10, 10))

        self.height = text.get_height() + 10
        self._panel = pygame.Surface((width, self.height))
        self._panel.fill(PANEL_BG_COLOR)
        self._panel.blit(text, textpos)

    def draw(self, surface, position):
        text = self._font.render(str(self.value), 1, (10, 10, 10))
        textpos = text.get_rect(topleft=(10, 10))

        self._panel.fill(PANEL_BG_COLOR)
        self._panel.blit(text, textpos)

        surface.blit(self._panel, position)

class NextShapePanel:

    """A panel displaying a shape.

    Methods:
    next_shape - returns the next shape and creates a new one
    draw - draws the panel on a surface

    """

    def __init__(self, width):
        self._grid = grids.NextShapeGrid()

        self._next_label_panel = LabelPanel(width, "Next:")
        self._next_shape_panel = pygame.Surface(
            (4 * BOX_LENGTH, 4 * BOX_LENGTH))
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self.height = self._next_label_panel.height + \
                      self._next_shape_panel.get_height() + 10
        self._panel = pygame.Surface((width, self.height))

        self.next_shape()

    def next_shape(self):
        """Create and display a new shape and return the previous one.

        The method is called internally on init, so that
        subsequent calls always return a shape.

        """
        shape = self._grid._active_shape
        self._grid.create_new_shape()
        self._grid.update()

        return shape

    def draw(self, surface, position):
        self._panel.fill(PANEL_BG_COLOR)
        self._next_label_panel.draw(self._panel, (0, 0))
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self._grid.draw(self._next_shape_panel)
        self._panel.blit(self._next_shape_panel, (10, self._next_label_panel.height + 10))
        surface.blit(self._panel, position)

class LevelPanel:

    """A panel displaying the current game level.

    Methods:
    increase_level - increases the game level by one
    draw - draw the panel on a surface

    """

    def __init__(self, width):
        """Create the panel with the text 'Level: 1'"""
        self._level_label_panel = LabelPanel(width, "Level: ")
        self._level_value_panel = ValuePanel(width, 1)
        self.height = self._level_label_panel.height + self._level_value_panel.height
        self._panel = pygame.Surface((width, self.height))

    def increase_level(self):
        """Increase the current level by one."""
        self._level_value_panel.value += 1

    def draw(self, surface, position):
        self._level_label_panel.draw(self._panel, (0, 0))
        self._level_value_panel.draw(self._panel, (0, self._level_label_panel.height))
        surface.blit(self._panel, position)

class ScorePanel:

    """A panel displaying the current player score.

    Methods:
    get_score - returns the current player score
    add_score - adds to the player score
    draw - draw the panel on a surface

    """

    def __init__(self, width):
        """Create the panel with the text 'Score: 1'"""
        self._score_label_panel = LabelPanel(width, "Score: ")
        self._score_value_panel = ValuePanel(width, 0)
        self.height = self._score_label_panel.height + self._score_value_panel.height
        self._panel = pygame.Surface((width, self.height))

    def get_score(self):
        return self._score_value_panel.value

    def add_score(self, score):
        self._score_value_panel.value += score

    def draw(self, surface, position):
        self._score_label_panel.draw(self._panel, (0, 0))
        self._score_value_panel.draw(
            self._panel, (0, self._score_label_panel.height))
        surface.blit(self._panel, position)

class ControlPanel:

    """A panel showing the next shape, game level and player score.

    Methods:
    next_shape - returns the next shape and creates a new one
    increase_level - increases the game level by one
    get_score - returns the current player score
    add_score - adds to the player score
    draw - draw the panel on a surface

    """

    def __init__(self, width, height):
        self._next_shape_panel = NextShapePanel(PANEL_WIDTH)
        self._panel_level = LevelPanel(PANEL_WIDTH)
        self._panel_score = ScorePanel(PANEL_WIDTH)
        self._panel = pygame.Surface((width, height))
        self._panel.fill(PANEL_BG_COLOR)

    def next_shape(self):
        """Return the next shape."""
        return self._next_shape_panel.next_shape()

    def get_score(self):
        """Return the current player score."""
        return self._panel_score.get_score()

    def add_score(self, value):
        """Add to the player score."""
        self._panel_score.add_score(value)

    def increase_level(self):
        """Increase the game level."""
        self._panel_level.increase_level()

    def draw(self, surface, position):
        self._next_shape_panel.draw(self._panel, (0, 0))
        panel_level_height = self._next_shape_panel.height
        self._panel_level.draw(self._panel, (0,panel_level_height))
        panel_score_height = panel_level_height + self._panel_level.height
        self._panel_score.draw(self._panel, (0,panel_score_height))
        surface.blit(self._panel, position)

