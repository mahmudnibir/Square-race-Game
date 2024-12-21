import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions (full screen)
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1280

# Game window dimensions (your game area)
GAME_WINDOW_WIDTH = 500
GAME_WINDOW_HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Calculate the position to center the game window
game_window_x = (SCREEN_WIDTH - GAME_WINDOW_WIDTH) // 2  # Center horizontally
game_window_y = (SCREEN_HEIGHT - GAME_WINDOW_HEIGHT) // 2  # Center vertically

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Centered Game Window Demo")

# Create a surface for the game window
game_surface = pygame.Surface((GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    # Fill the main screen with dark gray
    screen.fill(GRAY)
    
    # Fill the game window with black
    game_surface.fill(BLACK)
    
    # Draw a white border around the game surface
    pygame.draw.rect(game_surface, WHITE, (0, 0, GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT), 2)
    
    # Draw some text to show the dimensions
    font = pygame.font.Font(None, 36)
    screen_text = font.render(f"Screen: {SCREEN_WIDTH}x{SCREEN_HEIGHT}", True, WHITE)
    game_text = font.render(f"Game: {GAME_WINDOW_WIDTH}x{GAME_WINDOW_HEIGHT}", True, WHITE)
    
    # Blit the text onto the main screen
    screen.blit(screen_text, (10, 10))
    screen.blit(game_text, (10, 50))
    
    # Blit the game surface onto the main screen at the centered position
    screen.blit(game_surface, (game_window_x, game_window_y))
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
