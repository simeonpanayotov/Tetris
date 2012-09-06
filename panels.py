import pygame
from constants import *
import grids

class LabelPanel:
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
    def __init__(self, width):
        self._grid = grids.NextShapeGrid(4, 4)

        self._next_label_panel = LabelPanel(width, "Next:")
        self._next_shape_panel = pygame.Surface(
            (4 * BOX_LENGTH, 4 * BOX_LENGTH))
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self.height = self._next_label_panel.height + \
                      self._next_shape_panel.get_height()
        self._panel = pygame.Surface((width, self.height))

        self.next_shape()

    def draw(self, surface, position):
        self._panel.fill(PANEL_BG_COLOR)
        self._next_label_panel.draw(self._panel, (0, 0))
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self._grid.draw(self._next_shape_panel)
        self._panel.blit(self._next_shape_panel, (0, self._next_label_panel.height))
        surface.blit(self._panel, position)

    def next_shape(self):
        """Creates a new shape and returns the previous one.
        The method is called internally on init, so that
        subsequent calls always return a shape.

        """
        shape = self._grid.active_shape
        self._grid.create_new_shape()
        self._grid.update()

        return shape

class LevelPanel:
    def __init__(self, width):
        """Creates a panel that renders the text 'Level:'
        and the the current game level. Initial level is 1.

        """
        self._level_label_panel = LabelPanel(width, "Level: ")
        self._level_value_panel = ValuePanel(width, 1)
        self.height = self._level_label_panel.height + self._level_value_panel.height
        self._panel = pygame.Surface((width, self.height))

    def increase_level(self):
        self._level_value_panel.value += 1

    def draw(self, surface, position):
        self._level_label_panel.draw(self._panel, (0, 0))
        self._level_value_panel.draw(self._panel, (0, self._level_label_panel.height))
        surface.blit(self._panel, position)


class ScorePanel:
    def __init__(self, width):
        """Creates a panel that renders the current score
        of the player.

        """
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
    def __init__(self, width, height):
        """Creates a panel with the controls for:
        next shape, level and score.

        """
        self._next_shape_panel = NextShapePanel(PANEL_WIDTH)
        self._panel_level = LevelPanel(PANEL_WIDTH)
        self._panel_score = ScorePanel(PANEL_WIDTH)
        self._panel = pygame.Surface((width, height))
        self._panel.fill(PANEL_BG_COLOR)

    def next_shape(self):
        return self._next_shape_panel.next_shape()

    def get_score(self):
        return self._panel_score.get_score()

    def add_score(self, value):
        self._panel_score.add_score(value)

    def increase_level(self):
        self._panel_level.increase_level()

    def draw(self, surface, position):
        self._next_shape_panel.draw(self._panel, (0, 0))
        panel_level_height = self._next_shape_panel.height
        self._panel_level.draw(self._panel, (0,panel_level_height))
        panel_score_height = panel_level_height + self._panel_level.height
        self._panel_score.draw(self._panel, (0,panel_score_height))
        surface.blit(self._panel, position)

