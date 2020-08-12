import pygame

from colors import cell_colors
from constants import CellType, SIZE


class Spot:
    def __init__(self, col, row, total_rows):
        self._row = row
        self._col = col
        self._x = col * SIZE
        self._y = row * SIZE
        self._total_rows = total_rows
        self._celltype = CellType.NULL
        self._color = cell_colors[self._celltype]
        self._neighbors = []

    @property
    def celltype(self):
        return self._celltype

    @celltype.setter
    def celltype(self, celltype):
        self._celltype = celltype
        self._color = cell_colors[self._celltype]
    
    def draw(self, surface):
        pygame.draw.rect(
            surface,
            self._color,
            (self._x, self._y, SIZE, SIZE)
        )
