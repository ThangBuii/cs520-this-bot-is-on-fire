from collections import deque
import random
from model import CellType
import numpy as np
class Utils:
    # Get neighbours of a cell
    @staticmethod
    def get_neighbours(x, y,size):
        neighbors = []
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < size and 0 <= ny < size:
                neighbors.append((nx, ny))
        return neighbors
    
    # Get open neighbours
    @staticmethod
    def get_open_neighbours(x,y,ship):
        neighbors = []
        size = len(ship)
        for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            if 0 <= nx < size and 0 <= ny < size and ship[nx,ny] == CellType.OPEN.value:
                neighbors.append((nx, ny))
        return neighbors
    
    # Count open neighbours
    @staticmethod
    def count_open_neighbours(x, y, grid, D):
        return sum(1 for nx, ny in Utils.get_neighbours(x, y,D)
                   if grid[nx, ny] == CellType.OPEN.value)
    
    # Get open cells in the ship
    @staticmethod
    def get_open_cells(grid):
        size = len(grid)
        return [(x,y) for x in range(size) for y in range(size)
                if grid[x,y] == CellType.OPEN.value]
    
    # Set the value of a list of cells
    @staticmethod
    def set_cells_value(grid,positions,value):
        size = len(positions)
        for position in positions:
            grid[position] = value
        return grid
    
    # Select random position in the ship
    @staticmethod
    def select_random_positions(grid, num_positions):
        open_cells = Utils.get_open_cells(grid)

        if len(open_cells) < num_positions:
            raise ValueError("Not enough open cells to select the required positions.")

        return random.sample(open_cells, num_positions)
    
    # Calculate distance between two point (Manhattan distance)
    @staticmethod
    def calculate_distance(x,y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])
    
    # Check if there is any open cell left
    @staticmethod
    def is_no_more_open_cell(grid):
        return not np.any(grid == CellType.OPEN.value)
    
    # Reconstruct the path for A*
    @staticmethod
    def reconstruct_path(came_from,current,start):
        path = []
        while current in came_from:
            path.append(current)
            current = came_from[current]
        path.append(start)
        return path[::-1]

    # Calculate K of each cell
    @staticmethod
    def compute_burning_neighbors(ship):
        K_map = {}
        size = len(ship)
        for x in range(size):
            for y in range(size):
                if ship[x, y] != CellType.BLOCKED.value and ship[x, y] != CellType.FIRE.value:
                    neighbors = Utils.get_neighbours(x,y,size)
                    K = sum(1 for nx, ny in neighbors if ship[nx, ny] == CellType.FIRE.value)
                    K_map[(x, y)] = K
        return K_map
    
    # Find all fire cells
    @staticmethod
    def find_fire_cells(ship):
        size = len(ship)
        result = []
        for x in range(size):
            for y in range(size):
                if ship[x,y] == CellType.FIRE.value:
                    result.append((x,y))
        
        return result
    
    # Check if simulation is winnable
    @staticmethod
    def is_winnable(mazes,button_pos,bot_pos):
        size = len(mazes[0])
        T = len(mazes) - 1
        start = (bot_pos[0],bot_pos[1],0)
        explored = set()
        queue = deque([start])

        while queue:
            x, y, t = queue.popleft()
            if (x, y) == (button_pos[0], button_pos[1]) and mazes[t][x, y] == CellType.OPEN.value:
                return True
            if (x, y, t) in explored:
                continue
            explored.add((x, y, t))
            
            next_t = min(t + 1, T)
            moves = Utils.get_neighbours(x, y, size)
            for nx, ny in moves:
                if (mazes[next_t][nx, ny] != CellType.FIRE.value and 
                    mazes[next_t][nx, ny] != CellType.BLOCKED.value):
                    queue.append((nx, ny, next_t))

        return False