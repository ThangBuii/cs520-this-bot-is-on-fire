from utils import Utils
from fire import Fire

class Game:
    def __init__(self, q,ship):
        self.D = len(ship)
        self.ship = ship
        self.q = q
        
        bot_pos, button_pos, fire_pos = Utils.select_random_positions(self.ship, num_positions=3)

        
        
        # Initialize fire
        self.fire = Fire(self.ship, q)
        self.fire.initiate_first_position(fire_pos)

    def simulate():
        return 0