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
        self.mazes = {}

        self.grid[self.first_position] = CellType.FIRE.value
        self.mazes[0] = grid
        self.fire_spread_history.append((0,[self.first_position]))
    
    def get_fire_spread_history(self):
        return self.fire_spread_history

    # Count the number of burning neigbours of a open cell
    def count_burning_neighbour(self, x, y):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y, self.D)
                   if self.grid[nx, ny] == CellType.FIRE.value)

    # Spread the fire at time t
    def spread_fire(self,t):
        # Copy the ship layout
        new_grid = np.array(self.grid)
        newly_burning_cells = []

        #Create flammable cells if it haven't been created
        if not hasattr(self, "flammable_cells"):
            self.flammable_cells = [(x, y) for x in range(self.D) for y in range(self.D) if self.grid[x, y] != CellType.BLOCKED.value]

        for x, y in self.flammable_cells[:]:
            K = self.count_burning_neighbour(x, y)
            probability = 1 - (1 - self.q) ** K
            if random.random() < probability:
                new_grid[x, y] = CellType.FIRE.value
                newly_burning_cells.append((x, y))
                self.flammable_cells.remove((x, y))

        self.grid = new_grid
        self.mazes[t] = np.array(self.grid)
        self.fire_spread_history.append((t,newly_burning_cells))

        return newly_burning_cells
    
    # Return the cells caught on fire at time t
    def get_fire_spread_at_t_time(self,t):
        if t < len(self.fire_spread_history):
            return self.fire_spread_history[t][1]
        else:
            newly_burning_cells = self.spread_fire(t)
            return newly_burning_cells

    #Return mazes(ship layout) until the button caught on fire 
    def get_mazes_until_button_on_fire(self,button_position):
        t = 1
        while self.grid[button_position] != CellType.FIRE.value:
            self.spread_fire(t)
            t += 1
        
        return self.mazes


