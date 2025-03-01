from enum import Enum

class CellType(Enum):
    BLOCKED = 0  # Blocked (black)
    OPEN = 1     # Open (white)
    BOT = 2      # Bot (blue)
    FIRE = 3     # Fire (red)
    BUTTON = 4   # Button (green)