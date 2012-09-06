import pygame
from constants import *
import grids

class NextShapePanel():
    def __init__(self, width, height, x, y):
        self._create_panel(width, height, x, y)
        self._create_text()
        self._create_next_shape_panel()
        self._grid = grids.NextShapeGrid(4, 4)

        self.next_shape()

    def _create_panel(self, width, height, x, y):
        self._panel = pygame.Surface((width, height))
        self._panel.fill(PANEL_BG_COLOR)
        self._position = (x, y)

    def _create_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Next:", 1, (10, 10, 10))
        textpos = text.get_rect(topleft=(10, 10))
        self._panel.blit(text, textpos)
        self._text = text

    def _create_next_shape_panel(self):
        self._next_shape_panel = pygame.Surface(
            (4 * BOX_LENGTH, 4 * BOX_LENGTH))
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self._next_shape_panel_position = \
            (10, self._text.get_rect().height + 10)

    def _draw_next_shape_panel(self):
        self._next_shape_panel.fill(PANEL_BG_COLOR)
        self._grid.draw(self._next_shape_panel)
        self._panel.blit(self._next_shape_panel, self._next_shape_panel_position)

    def next_shape(self):
        """Creates a new shape and returns the previous one.
        The method is called internally on init, so that
        subsequent calls always return a shape.

        """
        shape = self._grid.active_shape
        self._grid.create_new_shape()
        self._grid.update()

        return shape

    def draw(self, screen):
        self._draw_next_shape_panel()
        screen.blit(self._panel, self._position)
