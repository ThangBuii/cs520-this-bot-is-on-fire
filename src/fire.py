import random
import numpy as np
from utils import Utils
from model import CellType

class Fire:
    def __init__(self, grid, q, fire_pos):
        self.grid = grid
        self.D = len(grid)
        self.q = q
        self.first_position = fire_pos
        self.fire_spread_history = []

        self.grid[self.first_position] = CellType.FIRE.value
        self.fire_spread_history.append((0,[self.first_position]))
        self.fire_simulation()

    def count_burning_neighbour(self, x, y):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y, self.D)
                   if self.grid[nx, ny] == CellType.FIRE.value)

    def spread_fire(self,t):
        new_grid = np.array(self.grid)
        newly_burning_cells = []

        for x in range(self.D):
            for y in range(self.D):
                if self.grid[x, y] != CellType.BLOCKED.value:
                    K = self.count_burning_neighbour(x, y)
                    probability = 1 - (1 - self.q) ** K
                    if random.random() < probability:
                        new_grid[x, y] = CellType.FIRE.value
                        newly_burning_cells.append((x, y))

        self.grid = new_grid
        self.fire_spread_history.append((t,newly_burning_cells))

        return newly_burning_cells
    
    def get_fire_spread_at_t_time(self,t):
        if t < len(self.fire_spread_history):
            return self.fire_spread_history[t][1]
        else:
            return []
    
    def fire_simulation(self):
        t = 1
        while True:
            if Utils.is_no_more_open_cell(self.grid):
                break
            self.spread_fire(t)
            t += 1

