import pygame
from constants import *

class NextShapePanel():
    def __init__(self, width, height, x, y):
        self._panel = pygame.Surface((width, height))
        self._panel.fill(PANEL_BG_COLOR)
        self._position = (x, y)

        self._draw_text()

    def _draw_text(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Next:", 1, (10, 10, 10))
        textpos = text.get_rect(topleft=(10, 10))
        self._panel.blit(text, textpos)

    def draw(self, screen):
        screen.blit(self._panel, self._position)
