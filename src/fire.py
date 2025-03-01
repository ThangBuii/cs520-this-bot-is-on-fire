import random
import numpy as np
from utils import Utils
from model import CellType

class Fire:
    def __init__(self, grid, q):
        self.grid = grid
        self.D = len(grid)
        self.q = q

    def initiate_first_position(self, first_position):
        self.grid[first_position] = CellType.FIRE.value

    def count_burning_neighbour(self, x, y):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y, self.D)
                   if self.grid[nx, ny] == CellType.FIRE.value)

    def spread_fire(self):
        new_grid = np.array(self.grid)
        newly_burning_cells = []

        for x in range(self.D):
            for y in range(self.D):
                if self.grid[x, y] == CellType.OPEN.value:
                    K = self.count_burning_neighbour(x, y)
                    probability = 1 - (1 - self.q) ** K
                    if random.random() < probability:
                        new_grid[x, y] = CellType.FIRE.value
                        newly_burning_cells.append((x, y))

        self.grid = new_grid
        return newly_burning_cells