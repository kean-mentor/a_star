import math

import pygame

from colors import cell_colors
from constants import CellType, SIZE


class Spot:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        self._x = col * SIZE
        self._y = row * SIZE
        self._celltype = CellType.NULL
        self._neighbors = []

    # TODO: Why!!!??? Is it because we use spot objects as dict keys?
    def __lt__(self, other):
        return False

    @property
    def celltype(self):
        return self._celltype

    @celltype.setter
    def celltype(self, celltype):
        self._celltype = celltype

    @property
    def neighbors(self):
        return self._neighbors

    def find_neighbors(self, grid):
        max_row = len(grid) - 1
        max_col = len(grid[0]) - 1
        
        # UP
        if self._row > 0 and grid[self._row - 1][self._col]._celltype != CellType.BARRIER:
            self._neighbors.append(grid[self._row - 1][self._col])

        # RIGHT
        if self._col < max_col and grid[self._row][self._col + 1]._celltype != CellType.BARRIER:
            self._neighbors.append(grid[self._row][self._col + 1])
        
        # DOWN
        if self._row < max_row and grid[self._row + 1][self._col]._celltype != CellType.BARRIER:
            self._neighbors.append(grid[self._row + 1][self._col])

        # LEFT:
        if self._col > 0 and grid[self._row][self._col - 1]._celltype != CellType.BARRIER:
            self._neighbors.append(grid[self._row][self._col - 1])

    def distance(self, other):
        """Calculating distance from 'other' using Manhattan distance."""
        return abs(other._col - self._col) + abs(other._row - self._row)

    def distance_euc(self, other):
        """Calculating distance from 'other' using Euclidean distance."""
        return math.sqrt(pow(other._col - self._col, 2) + pow(other._row - self._row, 2))
    
    def draw(self, surface):
        pygame.draw.rect(
            surface,
            cell_colors[self._celltype],
            (self._x, self._y, SIZE, SIZE)
        )
