from utils import Utils
from fire import Fire
from bot import Bot1
from visualization import Visualizer
from model import CellType
import time
import pygame

class Game:
    def __init__(self, q, ship):
        self.D = len(ship)
        self.ship = ship
        self.q = q

        bot_pos, self.button_pos, fire_pos = Utils.select_random_positions(self.ship, num_positions=3)

        # Initialize bot 1
        self.bot = Bot1(self.ship, bot_pos, self.button_pos, fire_pos)
        self.bot1_path = self.bot.bot1_algo()
        self.ship[bot_pos] = CellType.BOT.value

        # Initialize fire
        self.fire = Fire(self.ship, q)
        self.fire.initiate_first_position(fire_pos)

        # Initialize button
        self.ship[self.button_pos] = CellType.BUTTON.value

        # Initialize visualizer
        self.visualizer = Visualizer(self.D)

    def display_state(self, t):
        self.visualizer.visualize_grid(self.ship, t)
        time.sleep(2)

    def simulate(self):
        t = 0
        pygame.init()

        while True:
            # Get current bot position 
            current_bot1_pos = self.bot1_path[t]

            # Move bot
            self.ship = self.bot.move(t, self.ship)
            if self.ship is None:
                print("Bot is on fire!")
                self.display_state(t)
                break

            # Check if the bot has reached the button
            if current_bot1_pos == self.button_pos:
                print(f"Bot 1 has won the game in {t} moves!")
                self.display_state(t)
                break

            # Spread fire
            fire_spread_pos = self.fire.spread_fire()
            self.ship = Utils.set_cells_value(self.ship, fire_spread_pos, CellType.FIRE.value)

            # Check if bot caught fire
            if self.ship[current_bot1_pos] == CellType.FIRE.value:
                print("Bot is on fire!")
                self.display_state(t)
                break

            # Update visualization
            self.display_state(t)

            # Increase time step
            t += 1

            time.sleep(1)

        pygame.quit()