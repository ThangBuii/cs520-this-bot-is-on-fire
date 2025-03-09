from utils import Utils
from fire import Fire
from bot import Bot1,Bot2,Bot3,Bot4
from visualization import Visualizer
from model import CellType
import time
import pygame
import copy

class Game:
    def __init__(self, q, ship,fire,bots,bot_pos,button_pos,fire_pos,visualizer=None):
        self.D = len(ship)
        self.original_ship = ship
        self.q = q
        self.fire = fire
        self.bots = bots
        self.bot_pos = bot_pos
        self.button_pos = button_pos
        self.fire_pos = fire_pos
        self.visualizer = visualizer
        
    #Visualize the simulation
    def display_state(self, ship, t):
        self.visualizer.visualize_grid(ship, t, self.current_bot_name)
        time.sleep(4)

    #Simulate with visual
    def simulate_single_bot(self,bot):
        t = 0
        ship = copy.deepcopy(self.original_ship)
        ship[self.bot_pos] = CellType.BOT.value
        ship[self.button_pos] = CellType.BUTTON.value
        ship[self.fire_pos] = CellType.FIRE.value
        current_bot_pos = self.bot_pos

        while True:
            try:
                # Plan and get time t position
                current_bot_pos = bot.get_move_at_time_t(t, current_bot_pos, ship)
            except ValueError as e:
                if str(e) == "No path to button":
                    return t, "no_path_to_button"
                raise  # Re-raise other unexpected errors

            # Move bot on the map
            ship = bot.move(t, ship)

            # Check if bot moved to fire cell
            if ship is None:
                self.display_state(ship, t)
                return t, "bot_moved_to_fire"
            
            # Check if the bot has reached the button
            if current_bot_pos == self.button_pos:
                self.display_state(ship, t)
                return t, "success"

            # Spread fire
            fire_spread_pos = self.fire.get_fire_spread_at_t_time(t)
            ship = Utils.set_cells_value(ship, fire_spread_pos, CellType.FIRE.value)

            # Check if bot caught fire
            if ship[current_bot_pos] == CellType.FIRE.value:
                self.display_state(ship, t)
                return t, "fire_spread_to_bot"
            
            # Check if button caught fire
            if ship[self.button_pos] == CellType.FIRE.value:
                self.display_state(ship, t)
                return t, "fire_spread_to_button"

            # Update visualization with path
            self.display_state(ship, t)

            # Increase time step
            t += 1

    #Simulate with no visual
    def simulate_single_bot_no_visual(self,bot):
        t = 0
        ship = copy.deepcopy(self.original_ship)
        ship[self.bot_pos] = CellType.BOT.value
        ship[self.button_pos] = CellType.BUTTON.value
        ship[self.fire_pos] = CellType.FIRE.value
        current_bot_pos = self.bot_pos

        while True:
            try:
                # Plan and get time t position
                current_bot_pos = bot.get_move_at_time_t(t, current_bot_pos, ship)
            except ValueError as e:
                if str(e) == "No path to button":
                    return t, "no_path_to_button"
                raise  # Re-raise other unexpected errors

            # Move bot on the map
            ship = bot.move(t, ship)

            # Check if bot moved to fire cell
            if ship is None:
                return t, "bot_moved_to_fire"
            
            # Check if the bot has reached the button
            if current_bot_pos == self.button_pos:
                return t, "success"

            # Spread fire
            fire_spread_pos = self.fire.get_fire_spread_at_t_time(t)
            ship = Utils.set_cells_value(ship, fire_spread_pos, CellType.FIRE.value)

            # Check if bot caught fire
            if ship[current_bot_pos] == CellType.FIRE.value:
                return t, "fire_spread_to_bot"
            
            # Check if button caught fire
            if ship[self.button_pos] == CellType.FIRE.value:
                return t, "fire_spread_to_button"

            # Increase time step
            t += 1

    def re_simulate(self,bot_move_history, fire_spread_history):
        ship = copy.deepcopy(self.original_ship)
        ship[self.bot_pos] = CellType.BOT.value
        ship[self.button_pos] = CellType.BUTTON.value
        ship[self.fire_pos] = CellType.FIRE.value
        next_pos = self.bot_pos
        for t,position in bot_move_history:
            previous_pos = next_pos
            next_pos = position
            
            ship = Utils.set_cells_value(ship, [previous_pos], CellType.OPEN.value)
            ship = Utils.set_cells_value(ship, [next_pos], CellType.BOT.value)
            

            fire_positions = fire_spread_history[t][1]
            ship = Utils.set_cells_value(ship, fire_positions, CellType.FIRE.value)
            self.display_state(ship, t)
    
    #Get the result than visualize the simulation
    def simulate_re_simulate(self):  
        pygame.init()          
        results = []
        # Run the simulation for each bot
        for i, bot in enumerate(self.bots):
            self.current_bot_name = f"Bot {i+1}"
            moves, reason = self.simulate_single_bot_no_visual(bot)
            results.append((i + 1, moves, reason))
            if reason != "success":
                bot_move_history = bot.get_bot_move_history()
                fire_spread_history = self.fire.get_fire_spread_history()
                self.re_simulate(bot_move_history,fire_spread_history)
        
        pygame.quit()
        return results
    
    #Simulate without visual
    def simulate(self):
        results = []
        # Run the simulation for each bot
        for i, bot in enumerate(self.bots):
            self.current_bot_name = f"Bot {i+1}"
            moves, reason = self.simulate_single_bot_no_visual(bot)
            results.append((i + 1, moves, reason))
        
        return results

    #Simulate with visual
    def simulate_visual(self):    
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
            elif reason == "no_path_to_button":
                status = "Lost (no more path to button)"
            print(f"Bot {bot_num}: {status} in {moves} moves")

        pygame.quit()
