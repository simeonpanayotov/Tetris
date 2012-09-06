import pygame
import grid

TETRIS = "Tetris"
BG_COLOR = (219, 203, 138)

class Tetris:
    def __init__(self):
    # Create the game window.
        self._screen = pygame.display.set_mode((grid.SCREEN_WIDTH, grid.SCREEN_HEIGHT))
        pygame.display.set_caption(TETRIS)

        # Create the background surface.
        self._background = pygame.Surface(self._screen.get_size())
        self._background = self._background.convert()
        self._background.fill(BG_COLOR)

        self._gameGrid = grid.Grid()

    def update(self):
        self._gameGrid.update()

    def draw(self):
        self._screen.blit(self._background, (0, 0))
        self._gameGrid.draw(self._screen)

    def is_game_over(self):
        return self._gameGrid.is_game_over()

    def tick(self, key):
        self._gameGrid.tick(key)

