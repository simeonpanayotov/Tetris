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
        self._control_panel = panels.ControlPanel(PANEL_WIDTH, SCREEN_HEIGHT)

        self._gameGrid.add_new_shape(self._control_panel.next_shape())
        self._collapsed_row_count = 0
        self.level = 4

    def _get_score(self):
        score = 200

        if self._collapsed_row_count == 2:
            score += 10
        elif self._collapsed_row_count == 3:
            score += 30
        elif self._collapsed_row_count == 4:
            score += 60

        return score

    def _has_leveled_up(self, new_score, old_score):
        new_score //= 1000
        old_score //= 1000

        return new_score > old_score

    def update(self):
        self._gameGrid.update()

        if self._collapsed_row_count:
            score = self._get_score()
            old_score = self._control_panel.get_score()
            self._control_panel.add_score(score)
            new_score = self._control_panel.get_score()

            if self._has_leveled_up(new_score, old_score):
                self._control_panel.increase_level()
                self.level += 1

    def draw(self):
        self._screen.blit(self._background, (0, 0))
        self._gameGrid.draw(self._screen)
        self._control_panel.draw(self._screen, (grids.SCREEN_WIDTH, 0))

    def is_game_over(self):
        return self._gameGrid.is_game_over()

    def tick(self, key):
        self._collapsed_row_count = self._gameGrid.tick(key)

        if not self._gameGrid.has_active_shape:
            self._gameGrid.add_new_shape(self._control_panel.next_shape())

