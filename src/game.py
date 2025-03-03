from utils import Utils
from fire import Fire
from bot import Bot1,Bot2,Bot3
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

        # Find 3 random open positions for bot, button, fire
        self.bot_pos, self.button_pos, self.fire_pos = Utils.select_random_positions(self.original_ship, num_positions=3)

        # Initialize bots
        self.bots = [
            Bot1(copy.deepcopy(self.original_ship), self.bot_pos, self.button_pos, self.fire_pos),
            Bot2(copy.deepcopy(self.original_ship), self.bot_pos, self.button_pos, self.fire_pos),
            Bot3(copy.deepcopy(self.original_ship), self.bot_pos, self.button_pos, self.fire_pos),
            # Bot4(self.ship, bot_pos, self.button_pos, fire_pos),
        ]
        
        # Initialize fire
        self.fire = Fire(copy.deepcopy(self.original_ship), q, self.fire_pos)
    
        # Initialize visualizer
        self.visualizer = Visualizer(self.D)

    def display_state(self, ship, t):
        self.visualizer.visualize_grid(ship, t, self.current_bot_name)
        time.sleep(0.5)

    def simulate_single_bot(self,bot):
        t = 0
        ship = copy.deepcopy(self.original_ship)
        ship[self.bot_pos] = CellType.BOT.value
        ship[self.button_pos] = CellType.BUTTON.value
        ship[self.fire_pos] = CellType.FIRE.value
        current_bot_pos = self.bot_pos

        while True:
            # Plan and get time t position
            current_bot_pos = bot.get_move_at_time_t(t,current_bot_pos,ship)

            # Move bot on the map
            ship = bot.move(t, ship)

            # Check if bot moved to fire cell
            if ship is None:
                return t,"bot_moved_to_fire"
           
            # Check if the bot has reached the button
            if current_bot_pos == self.button_pos:
                self.display_state(ship,t)
                return t,"success"

            # Spread fire
            fire_spread_pos = self.fire.get_fire_spread_at_t_time(t)
            ship = Utils.set_cells_value(ship, fire_spread_pos, CellType.FIRE.value)

            # Check if bot caught fire
            if ship[current_bot_pos] == CellType.FIRE.value:
                self.display_state(ship,t)
                return t,"fire_spread_to_bot"
            
            # Check if button caught fire
            if ship[self.button_pos] == CellType.FIRE.value:
                return t,"fire_spread_to_button"

            # Update visualization
            self.display_state(ship,t)

            # Increase time step
            t += 1

            time.sleep(0.5)
    
    def simulate(self):
        pygame.init()
        
        results = []
        # Run the simulation for each bot
        for i, bot in enumerate(self.bots):
            self.current_bot_name = f"Bot {i+1}"
            moves, reason = self.simulate_single_bot(bot)
            results.append((i + 1, moves, reason))
        
        # Print summary
        print("\nSimulation Results:")
        for bot_num, moves, reason in results:
            if reason == "success":
                status = "Won"
            elif reason == "bot_moved_to_fire":
                status = "Lost (bot moved to fire)"
            elif reason == "fire_spread_to_bot":
                status = "Lost (fire spread to bot)"
            elif reason == "fire_spread_to_button":
                status = "Lost (fire spread to button)"
            print(f"Bot {bot_num}: {status} in {moves} moves")
        
        pygame.quit()