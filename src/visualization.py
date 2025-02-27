import pygame
import numpy as np

# Initialize pygame
pygame.init()

def visualize_grid(grid, time_step):
    """Visualize the ship layout with fire spreading, displaying the time step."""
    size = len(grid)
    cell_size = 40  # Size of each cell in pixels
    screen = pygame.display.set_mode((size * cell_size, size * cell_size + 50))  # Extra space for text
    pygame.display.set_caption('Fire Spread Simulation')

    # Define colors
    WHITE = (255, 255, 255)  # Open (1)
    BLACK = (0, 0, 0)        # Closed (0)
    RED = (255, 0, 0)        # Fire (2)

    # 🔥 Explicitly initialize font here
    if not pygame.font.get_init():
        pygame.font.init()
    font = pygame.font.Font(None, 36)  # Default font, size 36

    running = True
    while running:
        screen.fill(WHITE)  # Fill background with white
        
        # Draw grid
        for i in range(size):
            for j in range(size):
                # Set color based on grid value
                if grid[i][j] == 0:
                    color = BLACK  # Walls
                elif grid[i][j] == 1:
                    color = WHITE  # Open path
                elif grid[i][j] == 2:
                    color = RED  # Fire

                pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))
                pygame.draw.rect(screen, (128, 128, 128), (j * cell_size, i * cell_size, cell_size, cell_size), 1)  # Gridlines

        # Render and display time step text
        text_surface = font.render(f"Time Step: {time_step}", True, (0, 0, 0))
        screen.blit(text_surface, (10, size * cell_size + 10))  # Display below the grid

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop on quit

    pygame.quit()