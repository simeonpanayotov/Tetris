import pygame
import grids
import panels
from constants import *

class Tetris:
    def __init__(self):
    # Create the game window.
        self._screen = pygame.display.set_mode((WIDTH, grids.SCREEN_HEIGHT))
        pygame.display.set_caption(TETRIS)

        # Create the background surface.
        self._background = pygame.Surface(self._screen.get_size())
        self._background = self._background.convert()
        self._background.fill(BG_COLOR)

        self._gameGrid = grids.GameGrid()
        self._next_shape_panel = panels.NextShapePanel(PANEL_WIDTH)
        self._panel_level = panels.LevelPanel(PANEL_WIDTH)
        self._panel_score = panels.ScorePanel(PANEL_WIDTH)

        self._gameGrid.add_new_shape(self._next_shape_panel.next_shape())

    def update(self):
        self._gameGrid.update()

    def draw(self):
        self._screen.blit(self._background, (0, 0))
        self._gameGrid.draw(self._screen)
        self._next_shape_panel.draw(self._screen, (grids.SCREEN_WIDTH, 0 ))
        self._panel_level.draw(self._screen, (grids.SCREEN_WIDTH, PANEL_HEIGHT))
        self._panel_score.draw(self._screen, (grids.SCREEN_WIDTH, PANEL_HEIGHT + self._panel_level.height))

    def is_game_over(self):
        return self._gameGrid.is_game_over()

    def tick(self, key):
        self._gameGrid.tick(key)

        if not self._gameGrid.has_active_shape:
            self._gameGrid.add_new_shape(self._next_shape_panel.next_shape())

