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
        if t >= len(self.bot_move_history) or t == 0:
            return grid
        
        current_pos, next_pos = self.bot_move_history[t-1][1], self.bot_move_history[t][1]
        
        if grid[current_pos] == CellType.FIRE.value or grid[next_pos] == CellType.FIRE.value:
            return None

        grid[current_pos] = CellType.OPEN.value
        grid[next_pos] = CellType.BOT.value

        return grid
    
    #Return the bot move history
    def get_bot_move_history(self):
        return self.bot_move_history

#Plan the move with a* algorithm and move accordingly
class Bot1(Bot):
    def __init__(self, ship, start_pos, button_pos, fire_pos):
        super().__init__(ship, start_pos, button_pos, fire_pos)
        self.path = self.plan_path()

    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if(t < len(self.path)):
            self.bot_move_history.append((t,self.path[t]))
            return self.path[t]
        raise ValueError("No path to button")
    
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
        #h_score = distance from goal to point (using manhattan distance)
        #f_score = g_score + h_score
        g_score[start] = 0
        f_score[start] = 0 + Utils.calculate_distance(start, goal)

        while open:
            #using heapq to get the smallest f_score when pop
            _, current = heapq.heappop(open)

            #if it reached the goal, traverse to the start to find path
            if current == goal:
                return Utils.reconstruct_path(came_from,current,start)

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
    # At every t, replan the next move using upgraded a* algorithm
    # (same as bot 1 but it check for current fire cells not only first fire cell)
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if t == 0:
            return current_pos
        
        path = self.advanced_a_star_algo(current_pos, self.button_pos, ship)
        
        if len(path) < 2:
            self.bot_move_history.append((t, current_pos))
            raise ValueError("No path to button")
        
        next_pos = path[1]
        self.bot_move_history.append((t,next_pos))
        return next_pos

    def advanced_a_star_algo(self, start, goal, ship):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = 0 + Utils.calculate_distance(start, goal)

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                return Utils.reconstruct_path(came_from,current,start)

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
    # At every t, find a new plan
    # Plan 1: still using a* but check for fire cells and adjacent neigbour of fire cells
    # Plan 2: will be used when plan 1 cannot find a path, same strategy with bot 2
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if t == 0:
            return current_pos
        
        path = self.plan_1(current_pos, self.button_pos, ship)
        if len(path) < 2:
            path = self.plan_2(current_pos, self.button_pos, ship)

        if len(path) < 2:
            self.bot_move_history.append((t, current_pos))
            raise ValueError("No path to button")
        
        next_pos = path[1]
        self.bot_move_history.append((t,next_pos))
        return next_pos

    def plan_2(self, start, goal, ship):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = 0 + Utils.calculate_distance(start, goal)

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                return Utils.reconstruct_path(came_from,current,start)

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
        f_score[start] = 0 + Utils.calculate_distance(start, goal)

        fire_cells_and_ajdacent_cells = self.find_fire_cells_and_adjacent_cells(ship)

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                return Utils.reconstruct_path(came_from,current,start)

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

class Bot4(Bot):
    def __init__(self, ship, start_pos, button_pos, fire_pos,q):
        super().__init__(ship, start_pos, button_pos, fire_pos)
        self.q = q

    #At every t, find a new plan
    #Using a* but the bot would prefer cells that further away from fire
    def get_move_at_time_t(self, t, current_pos = None, ship=None):
        if t == 0:
            return current_pos
        path = self.fire_distance_risk_based_a_star_algo(current_pos, self.button_pos, ship)
        
        if len(path) < 2:
            self.bot_move_history.append((t, current_pos))
            raise ValueError("No path to button")
        
        next_pos = path[1]
        self.bot_move_history.append((t,next_pos))
        return next_pos
    
    # Compute the distance of a cell to its nearest fire cell
    def precompute_fire_distance_map(self, ship):
        size = len(ship)
        result = {}
        fire_cells = Utils.find_fire_cells(ship)
        
        for x in range(size):
            for y in range(size):
                if ship[x, y] == CellType.BLOCKED.value or ship[x, y] == CellType.FIRE.value:
                    result[(x, y)] = 0
                else:
                    result[(x, y)] = min(Utils.calculate_distance((x, y), f) for f in fire_cells) if fire_cells else size
        return result
    
    def fire_distance_risk_based_a_star_algo(self, start, goal, ship):
        open = []
        heapq.heappush(open, (0, start))
        came_from = {}
        g_score = {}
        f_score = {}

        g_score[start] = 0
        f_score[start] = 0 + Utils.calculate_distance(start, goal)
        K_set = Utils.compute_burning_neighbors(ship)
        min_dist_to_fire_map = self.precompute_fire_distance_map(ship)
        #The higher the weight, the scarier the fire to the bot
        fire_risk_weight = 10
        #The higher the weight, the bot prioritizes path to goal more
        heuristic_weight = 1.5 if self.q <= 0.5 else 1.8

        while open:
            _, current = heapq.heappop(open)

            if current == goal:
                return Utils.reconstruct_path(came_from,current,start)

            neighbours = Utils.get_neighbours(current[0], current[1], len(ship))
            for neighbour in neighbours:
                if ship[neighbour] != CellType.BLOCKED.value and ship[neighbour] != CellType.FIRE.value:
                    #Get k value of neighbour
                    K = K_set.get(neighbour,0)
                    #Get distance from nearest fire of cell
                    min_dist_from_fire = min_dist_to_fire_map[neighbour]
                    #K = 0, the risk will base on the distance to the fire
                    #K > 0, the risk will base on the fire spread formula
                    if K == 0:
                        fire_spread_risk = 1 / max(1, min_dist_from_fire)
                    else:
                        fire_spread_risk = 1 - (1 - self.q) ** K
                    temp_g_score = g_score[current] + 1 + fire_risk_weight * fire_spread_risk

                    if neighbour not in g_score or temp_g_score < g_score[neighbour]:
                        g_score[neighbour] = temp_g_score
                        came_from[neighbour] = current
                        f_score[neighbour] = temp_g_score + heuristic_weight * Utils.calculate_distance(neighbour,goal)
                        heapq.heappush(open, (f_score[neighbour], neighbour))

        return []