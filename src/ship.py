import numpy as np
import random
from utils import Utils
from model import CellType

class Ship:
    def generate_ship(self,D):
            grid = np.zeros((D,D),dtype=int)
            start_x,start_y = random.randint(1,D-2) , random.randint(1,D-2)
            grid[start_x,start_y] = CellType.OPEN.value

            #Add the neighbours of start cells into set
            one_open_neighbour_cells = set(Utils.get_neighbours(start_x, start_y, D))

            while one_open_neighbour_cells:
                #Choose randomly one of the cells
                x, y = random.choice(list(one_open_neighbour_cells))

                #Recheck if the chosen cells have only one neighbour
                open_neighbors = [(nx, ny) for nx, ny in Utils.get_neighbours(x, y, D) if grid[nx, ny] == CellType.OPEN.value]
                if len(open_neighbors) == 1:
                    grid[x, y] = CellType.OPEN.value
                    # Add its closed neighbors to the one_open_neighbour_cells
                    for nx, ny in Utils.get_neighbours(x, y, D):
                        if grid[nx, ny] == CellType.BLOCKED.value:
                            one_open_neighbour_cells.add((nx, ny))
                
                # Remove processed cell from one_open_neighbour_cells
                one_open_neighbour_cells.remove((x, y))

            # Find the dead ends cell
            dead_ends = [(x, y) for x in range(D) for y in range(D)
                        if(grid[x, y] == CellType.OPEN.value and Utils.count_open_neighbours(x,y,grid,D) == 1)]
            
            # Choose randomly half of the dead cells and one of their closed neighbour to open
            for (x,y) in random.sample(dead_ends, len(dead_ends)//2):
                closed_neighbour = [(nx,ny) for nx,ny in Utils.get_neighbours(x,y,D)
                                    if grid[nx,ny] == CellType.BLOCKED.value]
                if closed_neighbour:
                    nx,ny = random.choice(closed_neighbour)
                    grid[nx,ny] = CellType.OPEN.value

            return grid
                
                



