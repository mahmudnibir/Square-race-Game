import pygame
import csv

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 700
TILE_SIZE = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Level Editor")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)  # Orange color

# Tile colors mapping
tile_colors = {'r': RED, 'g': GREEN, 'y': YELLOW, 'b': BLUE, 'w': WHITE, 'o': ORANGE}

# Reverse tile color mapping (for easy look-up)
color_names = {RED: 'r', GREEN: 'g', YELLOW: 'y', BLUE: 'b', WHITE: 'w', ORANGE: 'o'}

# Grid to store the level data
grid = [[None for _ in range(HEIGHT // TILE_SIZE)] for _ in range(WIDTH // TILE_SIZE)]

# Current selected color
selected_color = RED

# Font for text
font = pygame.font.SysFont(None, 24)

# Function to draw the grid and UI
def draw():
    SCREEN.fill(BLACK)  # Background color set to black

    # Draw the grid (for 20x20 tiles)
    for x in range(0, WIDTH, TILE_SIZE):
        for y in range(0, HEIGHT, TILE_SIZE):
            tile = grid[x // TILE_SIZE][y // TILE_SIZE]
            if tile:
                pygame.draw.rect(SCREEN, tile, (x, y, TILE_SIZE, TILE_SIZE))
    
    # Draw the color selection squares (for tile colors)
    colors = [RED, GREEN, YELLOW, BLUE, WHITE, ORANGE]  # Add orange here
    for i, color in enumerate(colors):
        pygame.draw.rect(SCREEN, color, (WIDTH - 100, 50 + i * 30, 20, 20))
    
    # Highlight the selected color
    selected_rect = pygame.Rect(WIDTH - 100, 50 + colors.index(selected_color) * 30, 20, 20)
    pygame.draw.rect(SCREEN, selected_color, selected_rect, 3)  # Outline the selected color

    # Draw buttons text
    save_text = font.render("S: Save | L: Load", True, (255, 255, 255))
    SCREEN.blit(save_text, (10, 10))
    
    pygame.display.update()

# Function to save the grid data in CSV format
def save_data():
    with open('level_data6.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        for row in grid:
            # Convert each tile to its corresponding color code (e.g., 'r', 'g', 'w')
            row_data = [color_names.get(tile, '0') for tile in row]  # Write '0' for empty cells
            writer.writerow(row_data)

# Function to load the grid data from CSV format
def load_data():
    global grid
    try:
        with open('level_data6.csv', 'r') as f:
            reader = csv.reader(f)
            loaded_grid = list(reader)  # Read the CSV into a list of rows
            # Initialize the grid to the correct dimensions
            grid = [[None for _ in range(HEIGHT // TILE_SIZE)] for _ in range(WIDTH // TILE_SIZE)]
            # Fill the grid with loaded data
            for y, row in enumerate(loaded_grid):
                for x, color_code in enumerate(row):
                    if color_code != '0':  # Skip empty cells
                        grid[y][x] = tile_colors.get(color_code, None)  # Map color code to actual color
    except FileNotFoundError:
        print("No saved data found.")

# Function to handle mouse events for drawing/removing
def handle_mouse(pos, action='draw'):
    x, y = pos
    grid_x, grid_y = x // TILE_SIZE, y // TILE_SIZE
    
    if 0 <= grid_x < WIDTH // TILE_SIZE and 0 <= grid_y < HEIGHT // TILE_SIZE:
        if action == 'draw':
            grid[grid_x][grid_y] = selected_color
        elif action == 'remove':
            grid[grid_x][grid_y] = None

# Main loop
running = True
dragging = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:  # Save the level
                save_data()
            elif event.key == pygame.K_l:  # Load the level
                load_data()
            elif event.key == pygame.K_r:  # Select Red
                selected_color = RED
            elif event.key == pygame.K_g:  # Select Green
                selected_color = GREEN
            elif event.key == pygame.K_y:  # Select Yellow
                selected_color = YELLOW
            elif event.key == pygame.K_b:  # Select Blue
                selected_color = BLUE
            elif event.key == pygame.K_w:  # Select White
                selected_color = WHITE
            elif event.key == pygame.K_o:  # Select Orange
                selected_color = ORANGE
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click to draw
                dragging = True
                handle_mouse(event.pos)
            elif event.button == 3:  # Right click to remove
                dragging = True
                handle_mouse(event.pos, action='remove')
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False
        elif event.type == pygame.MOUSEMOTION and dragging:
            if pygame.mouse.get_pressed()[0]:  # Draw
                handle_mouse(event.pos)
            elif pygame.mouse.get_pressed()[2]:  # Remove
                handle_mouse(event.pos, action='remove')

    # Draw everything
    draw()

# Quit pygame
pygame.quit()
