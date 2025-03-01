import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from ship import Ship
from game import Game

#Initialize ship size and flammability q
shipSize = random.randrange(10,40)
q = 0.3
#Generate the ship
ship = Ship()
ship_grid = ship.generate_ship(shipSize)

#Initialize the game
game = Game(q,ship_grid)
game.simulate()




