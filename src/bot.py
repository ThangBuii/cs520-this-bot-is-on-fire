import heapq
from utils import Utils
from model import CellType

class Bot1:
    def __init__(self, ship, start_pos, button_pos, fire_pos):
        self.ship = ship
        self.position = start_pos
        self.button_pos = button_pos
        self.fire_pos = fire_pos
        self.ship[button_pos] = CellType.BUTTON.value
        self.bot1_path = self.bot1_algo()

    def bot1_algo(self):
        return self.a_star_algo(self.position, self.button_pos)

    def a_star_algo(self, start, goal):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = Utils.calculate_distance(start, goal)

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            neighbours = Utils.get_neighbours(current[0], current[1], len(self.ship))
            for neighbour in neighbours:
                if self.ship[neighbour] != 0 and neighbour != self.fire_pos:
                    temp_g_score = g_score[current] + 1

                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + Utils.calculate_distance(neighbour, goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []

    def reached_goal(self):
        return self.position == self.button_pos

    def move(self, t, grid):
        current_pos, next_pos = self.bot1_path[t], self.bot1_path[t+1]

        if grid[current_pos] == CellType.FIRE.value or grid[next_pos] == CellType.FIRE.value:
            return None

        grid[current_pos] = CellType.OPEN.value
        grid[next_pos] = CellType.BOT.value

        return grid