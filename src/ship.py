import numpy as np
import random
from utils import Utils
from model import CellType

class Ship:
    def generate_ship(self,D):
            grid = np.zeros((D,D),dtype=int)
            start_x,start_y = random.randint(1,D-2) , random.randint(1,D-2)
            grid[start_x,start_y] = CellType.OPEN.value

            while True:
                # Find all cells with exactly one neighbour
                one_neighbour_cells = [(x, y) for x in range(D) for y in range(D)
                                    if(grid[x, y] == CellType.BLOCKED.value and Utils.count_open_neighbours(x,y,grid,D) == 1)]
                
                if not one_neighbour_cells:
                    break
                
                #Choose a random cell and open it
                random_cell = random.choice(one_neighbour_cells)
                grid[random_cell] = CellType.OPEN.value

            # Find the dead ends cell
            dead_ends = [(x, y) for x in range(D) for y in range(D)
                        if(grid[x, y] == CellType.OPEN.value and Utils.count_open_neighbours(x,y,grid,D) == 1)]
            
            # Choose randomly half of the dead cells and one of their closed neighbour at random
            for (x,y) in random.sample(dead_ends, len(dead_ends)//2):
                closed_neighbour = [(nx,ny) for nx,ny in Utils.get_neighbours(x,y,D)
                                    if grid[nx,ny] == 0]
                if closed_neighbour:
                    nx,ny = random.choice(closed_neighbour)
                    grid[nx,ny] = CellType.OPEN.value

            return grid
                
                



