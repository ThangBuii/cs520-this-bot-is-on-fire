import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from ship import generate_ship
from game import Game
from visualization import visualize_grid

#Initialize ship size and flammability q
shipSize = 10  
q = 0.3
#Generate the ship
ship = generate_ship(shipSize)

#Initialize the game
game = Game(q,ship)
game.simulate()




