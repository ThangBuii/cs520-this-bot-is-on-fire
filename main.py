import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from ship import Ship
from visualization import visualize_grid

shipSize = random.randint(10,40)
ship = Ship(shipSize)
visualize_grid(ship.grid)