from utils import Utils
from fire import Fire
from bot import Bot1
from visualization import Visualizer
from model import CellType
import time
import pygame
import copy

class Game:
    def __init__(self, q, ship):
        self.D = len(ship)
        self.original_ship = ship
        self.q = q

        self.bot_pos, self.button_pos, self.fire_pos = Utils.select_random_positions(self.original_ship, num_positions=3)

        # Initialize bot 1
        self.bots = [
            Bot1(copy.deepcopy(self.original_ship), self.bot_pos, self.button_pos, self.fire_pos),
            # Bot2(copy.deepcopy(self.original_ship), self.bot_pos, self.button_pos, self.fire_pos)
            # Bot3(self.ship, bot_pos, self.button_pos, fire_pos),
            # Bot4(self.ship, bot_pos, self.button_pos, fire_pos),
        ]
        
        # Initialize fire
        self.fire = Fire(copy.deepcopy(self.original_ship), q, self.fire_pos)
    
        # Initialize visualizer
        self.visualizer = Visualizer(self.D)

    def display_state(self, ship, t):
        self.visualizer.visualize_grid(ship, t)
        time.sleep(1)

    def simulate_single_bot(self,bot,bot_index):
        t = 0
        ship = copy.deepcopy(self.original_ship)
        ship[self.bot_pos] = CellType.BOT.value
        ship[self.button_pos] = CellType.BUTTON.value

        while True:
            # Get current bot position 
            current_bot_pos = bot.get_move_at_time_t(t)

            # Move bot
            ship = bot.move(t, ship)
            if ship is None:
                self.display_state(t)
                return t,False
           
            # Check if the bot has reached the button
            if current_bot_pos == self.button_pos:
                self.display_state(ship,t)
                return t,True

            # Spread fire
            fire_spread_pos = self.fire.get_fire_spread_at_t_time(t)
            ship = Utils.set_cells_value(ship, fire_spread_pos, CellType.FIRE.value)

            # Check if bot caught fire
            if ship[current_bot_pos] == CellType.FIRE.value:
                self.display_state(ship,t)
                return t,False

            # Update visualization
            self.display_state(ship,t)

            # Increase time step
            t += 1

            time.sleep(1)
    
    def simulate(self):
        pygame.init()
        
        results = []
        for i, bot in enumerate(self.bots):
            print(f"\nSimulating Bot {i + 1}")
            moves, success = self.simulate_single_bot(bot, i)
            results.append((i + 1, moves, success))
        
        # Print summary
        print("\nSimulation Results:")
        for bot_num, moves, success in results:
            status = "Won" if success else "Lost (caught fire)"
            print(f"Bot {bot_num}: {status} in {moves} moves")
        
        pygame.quit()