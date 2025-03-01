import numpy as np
import random
from utils import Utils

class Ship:
    def generate_ship(self,D):
            grid = np.zeros((D,D),dtype=int)
            start_x,start_y = random.randint(1,D-2) , random.randint(1,D-2)
            grid[start_x,start_y] = 1

            while True:
                one_neighbour_cells = [(x, y) for x in range(D) for y in range(D)
                                    if(grid[x, y] == 0 and Utils.count_open_neighbours(x,y,grid,D) == 1)]
                
                if not one_neighbour_cells:
                    break

                random_cells = random.choice(one_neighbour_cells)
                grid[random_cells] = 1

            dead_ends = [(x, y) for x in range(D) for y in range(D)
                        if(grid[x, y] == 1 and Utils.count_open_neighbours(x,y,grid,D) == 1)]
            
            for (x,y) in random.sample(dead_ends, len(dead_ends)//2):
                closed_neighbour = [(nx,ny) for nx,ny in Utils.get_neighbours(x,y,D)
                                    if grid[nx,ny] == 0]
                if closed_neighbour:
                    nx,ny = random.choice(closed_neighbour)
                    grid[nx,ny] = 1

            return grid
                
                



