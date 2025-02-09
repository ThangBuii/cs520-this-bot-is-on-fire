import pygame
import numpy as np

# Initialize pygame
pygame.init()

def visualize_grid(grid):
    size = len(grid)
    cell_size = 40  # Size of each cell in pixels
    screen = pygame.display.set_mode((size * cell_size, size * cell_size))
    pygame.display.set_caption('Grid Visualization')

    # Define colors
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    BLACK = (0, 0, 0)

    # Map grid values ('.' = white, other characters = blue)
    grid_values = np.array([[0 if cell == '.' else 1 for cell in row] for row in grid])

    # Game loop
    running = True
    while running:
        screen.fill(WHITE)  # Fill background with white
        
        for i in range(size):
            for j in range(size):
                # Color based on grid value
                color = BLUE if grid_values[i][j] == 1 else WHITE
                pygame.draw.rect(screen, color, (j * cell_size, i * cell_size, cell_size, cell_size))

                # Draw gridlines
                pygame.draw.rect(screen, BLACK, (j * cell_size, i * cell_size, cell_size, cell_size), 1)

                # Add labels (if needed)
                font = pygame.font.SysFont(None, 24)
                label = font.render(grid[i][j], True, BLACK)
                screen.blit(label, (j * cell_size + 10, i * cell_size + 10))

        pygame.display.flip()  # Update the screen

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Exit the loop on quit

    pygame.quit()
