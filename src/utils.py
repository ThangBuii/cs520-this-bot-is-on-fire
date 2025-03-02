import random
from model import CellType
import numpy as np

class Utils:
    @staticmethod
    def get_neighbours(x, y,size):
        neighbors = []
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < size and 0 <= ny < size:
                neighbors.append((nx, ny))
        return neighbors
    
    @staticmethod
    def count_open_neighbours(x, y, grid, D):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y,D)
                   if grid[nx, ny] == CellType.OPEN.value)
    
    @staticmethod
    def get_open_cells(grid):
        size = len(grid)
        return [(x,y) for x in range(size) for y in range(size)
                if grid[x,y] == CellType.OPEN.value]
    
    @staticmethod
    def set_cells_value(grid,positions,value):
        size = len(positions)
        for i in range(size):
            grid[positions[i]] = value
        return grid
    
    @staticmethod
    def select_random_positions(grid, num_positions):
        open_cells = Utils.get_open_cells(grid)

        if len(open_cells) < num_positions:
            raise ValueError("Not enough open cells to select the required positions.")

        return random.sample(open_cells, num_positions)
    
    @staticmethod
    def calculate_distance(x,y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
    @staticmethod
    def is_no_more_open_cell(grid):
        return not np.any(grid == CellType.OPEN.value)