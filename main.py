import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from ship import Ship
from game import Game
from utils import Utils
from bot import Bot1,Bot2,Bot3,Bot4
import copy
from fire import Fire
from visualization import Visualizer
from test import run_full_test


def run_simulation(ship_size=40, q=0.5, visualize=True):
    """ Runs the simulation once and returns the result. """
    # Generate the ship
    ship = Ship()
    ship_grid = ship.generate_ship(ship_size)
    visualizer = Visualizer(ship_size) if visualize else None

    bot_pos, button_pos, fire_pos = Utils.select_random_positions(ship_grid, num_positions=3)

    # Initialize fire
    fire = Fire(copy.deepcopy(ship_grid), q, fire_pos)
    
    bots = [
        Bot1(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
        Bot2(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
        Bot3(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos),
        Bot4(copy.deepcopy(ship_grid), bot_pos, button_pos, fire_pos, q)
    ]   
    game = Game(q, ship_grid, fire, bots, bot_pos, button_pos, fire_pos, visualizer)
    game.simulate_visual()
        
def main():
    while True:
        print("\nChoose an option:")
        print("1. Run simulation for each bot (visual)")
        print("2. Run 100 simulations on each q for bots")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            run_simulation()
        elif choice == "2":
            run_full_test()
        elif choice == "3":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()




