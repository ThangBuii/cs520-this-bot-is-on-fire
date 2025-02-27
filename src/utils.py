import random

class Utils:
    @staticmethod
    def get_neighbours(x, y,D):
        neighbors = []
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < D and 0 <= ny < D:
                neighbors.append((nx, ny))
        return neighbors
    
    @staticmethod
    def count_open_neighbours(x, y, grid, D):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y,D)
                   if grid[nx, ny] == 1)
    
    @staticmethod
    def select_random_positions(grid, num_positions=3):
        shipSize = len(grid)
        open_cells = [(x, y) for x in range(shipSize) for y in range(shipSize) if grid[x, y] == 1]

        if len(open_cells) < num_positions:
            raise ValueError("Not enough open cells to select the required positions.")

        return random.sample(open_cells, num_positions)  # Pick unique positions