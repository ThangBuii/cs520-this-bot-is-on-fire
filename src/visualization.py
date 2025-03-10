import pygame

class Visualizer:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.cell_size = 40  # Size of each cell in pixels
        self.screen = pygame.display.set_mode((self.grid_size * self.cell_size, self.grid_size * self.cell_size + 50))
        pygame.display.set_caption('This bot is on fire')

        # Define colors
        self.COLORS = {
            0: (0, 0, 0),       # Blocked (black)
            1: (255, 255, 255), # Open (white)
            2: (0, 0, 255),     # Bot (blue)
            3: (255, 0, 0),     # Fire (red)
            4: (0, 255, 0)      # Button (green)
        }

        if not pygame.font.get_init():
            pygame.font.init()
        self.font = pygame.font.Font(None, 36)  # Default font, size 36

    def visualize_grid(self, grid, time_step, bot_name):
        self.screen.fill((255, 255, 255))  # Fill background

        # Draw grid
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                color = self.COLORS.get(grid[i][j], (100, 100, 100)) 
                pygame.draw.rect(self.screen, color, (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
                pygame.draw.rect(self.screen, (128, 128, 128), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size), 1)

        # Render time step text
        text_surface = self.font.render(f"Bot: {bot_name} - Time Step: {time_step}", True, (0, 0, 0))
        self.screen.blit(text_surface, (10, self.grid_size * self.cell_size + 10))  # Display below the grid

        pygame.display.flip()  # Update screen