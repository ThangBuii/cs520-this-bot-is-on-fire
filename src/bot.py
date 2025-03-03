import heapq
from utils import Utils
from model import CellType

class Bot:
    def __init__(self, ship, start_pos, button_pos, fire_pos):
        self.ship = ship
        self.position = start_pos
        self.button_pos = button_pos
        self.fire_pos = fire_pos

        self.bot_move_history = []

        #Add the first position to history
        self.bot_move_history.append((0,self.position))

    # Return bot move at time t
    def get_move_at_time_t(self, t, current_pos = None, ship = None):
        raise NotImplementedError("Each bot must define its own pathfinding method.")
    
    # Return the ship layout after bot move at time t
    def move(self,t,grid):
        raise NotImplementedError("Each bot must define its own pathfinding method.")
    
    #Return the bot move history
    def get_bot_move_history(self):
        return self.bot_move_history

#Plan the move with a* algorithm and move accordingly
class Bot1(Bot):
    def __init__(self, ship, start_pos, button_pos, fire_pos):
        super().__init__(ship, start_pos, button_pos, fire_pos)
        self.path = self.plan_path()

    # Return bot 1 move a
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if(t < len(self.path)):
            self.bot_move_history.append((t,self.path[t]))
            return self.path[t]
        return None
    
    def move(self, t, grid):
        if t >= len(self.path) or t == 0:
            return grid
        
        current_pos, next_pos = self.path[t-1], self.path[t]
        
        if grid[current_pos] == CellType.FIRE.value or grid[next_pos] == CellType.FIRE.value:
            return None

        grid[current_pos] = CellType.OPEN.value
        grid[next_pos] = CellType.BOT.value

        return grid
    # Call a* algorithm
    def plan_path(self):
        return self.a_star_algo(self.position, self.button_pos)

    # Planning the move ignore the blocked cells and the first fire position
    def a_star_algo(self, start, goal):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        #g_score = distance from start to point
        #h_score = distance from point to goal (using manhattan distance)
        #f_score = g_score + h_score
        g_score[start] = 0
        f_score[start] = Utils.calculate_distance(start, goal)

        while open:
            #using heapq to get the smallest f_score when pop
            _, current = heapq.heappop(open)

            #if it reached the goal, traverse to the start to find path
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            #find all the neighbours of current point
            neighbours = Utils.get_neighbours(current[0], current[1], len(self.ship))

            for neighbour in neighbours:
                #check if the neighbour is not blocked or not the first fire position
                if self.ship[neighbour] != CellType.BLOCKED.value and neighbour != self.fire_pos:
                    #the g_score of the neighbor always = g_score of current + 1
                    temp_g_score = g_score[current] + 1

                    #if neighbour has not been visited or the new g_score is better
                    #then update the value for that neighbour
                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + Utils.calculate_distance(neighbour, goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []
    
class Bot2(Bot):
    def move(self, t, grid):
        if t >= len(self.bot_move_history) or t == 0:
            return grid
        
        current_pos, next_pos = self.bot_move_history[t-1][1], self.bot_move_history[t][1]
        
        if grid[current_pos] == CellType.FIRE.value or grid[next_pos] == CellType.FIRE.value:
            return None

        grid[current_pos] = CellType.OPEN.value
        grid[next_pos] = CellType.BOT.value

        return grid
    
    #at every t, replan the next move using upgraded a* algorithm
    #(same as bot 1 but check for current fire cells not only first fire cell)
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if t == 0:
            return current_pos
        
        path = self.a_star_algo(current_pos, self.button_pos, ship)
        
        next_pos = path[1] if len(path) >= 2 else current_pos
        self.bot_move_history.append((t,next_pos))
        return next_pos

    def a_star_algo(self, start, goal, ship):
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

            neighbours = Utils.get_neighbours(current[0], current[1], len(ship))
            for neighbour in neighbours:
                if ship[neighbour] != CellType.BLOCKED.value and ship[neighbour] != CellType.FIRE.value:
                    temp_g_score = g_score[current] + 1

                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + Utils.calculate_distance(neighbour, goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []
    

class Bot3(Bot):
    def move(self, t, grid):
        if t >= len(self.bot_move_history) or t == 0:
            return grid
        
        current_pos, next_pos = self.bot_move_history[t-1][1], self.bot_move_history[t][1]
        
        if grid[current_pos] == CellType.FIRE.value or grid[next_pos] == CellType.FIRE.value:
            return None

        grid[current_pos] = CellType.OPEN.value
        grid[next_pos] = CellType.BOT.value

        return grid
    
    #At every t, find a new plan
    #Plan 1: still using a* but check for fire cells and adjacent neigbour of fire cells
    #Plan 2: will be used when plan 1 cannot find a path, same strategy with bot 2
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if t == 0:
            return current_pos
        
        path = self.plan_1(current_pos, self.button_pos, ship)
        if len(path) < 2:
            path = self.plan_2(current_pos, self.button_pos, ship)

        
        next_pos = path[1] if len(path) >= 2 else current_pos
        self.bot_move_history.append((t,next_pos))
        return next_pos

    def plan_2(self, start, goal, ship):
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

            neighbours = Utils.get_neighbours(current[0], current[1], len(ship))
            for neighbour in neighbours:
                if ship[neighbour] != CellType.BLOCKED.value and ship[neighbour] != CellType.FIRE.value:
                    temp_g_score = g_score[current] + 1

                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + Utils.calculate_distance(neighbour, goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []
    
    def plan_1(self, start, goal, ship):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = Utils.calculate_distance(start, goal)

        fire_cells_and_ajdacent_cells = self.find_fire_cells_and_adjacent_cells(ship)

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]

            neighbours = Utils.get_neighbours(current[0], current[1], len(ship))
            for neighbour in neighbours:
                if ship[neighbour] != CellType.BLOCKED.value and neighbour not in fire_cells_and_ajdacent_cells:
                    temp_g_score = g_score[current] + 1

                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + Utils.calculate_distance(neighbour, goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []
    
    def find_fire_cells_and_adjacent_cells(self,ship):
        result = set()
        ship_size = len(ship)
        for x in range(ship_size):
            for y in range(ship_size):
                if ship[x,y] == CellType.FIRE.value:
                    result.add((x,y))
                    result.update(Utils.get_open_neighbours(x,y,ship))

        return list(result)
