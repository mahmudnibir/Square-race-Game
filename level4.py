import pygame
import random
import sys
import csv

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 700

# Colors
BLACK = (255, 226, 164)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 205, 0)
YELLOW = (255, 255, 0)
WHITE = (23, 70, 95)

# Square settings
square_size = 20
square_speed = 2  # Reduced speed for smoother motion

# Set the starting position for squares at the middle of the bottom
start_x = 0
start_y = SCREEN_HEIGHT - square_size

# Generate initial squares with starting position and random speeds
squares = [
    {"color": BLUE, "x": start_x, "y": start_y,
     "speed_x": random.choice([-square_speed, square_speed]), "speed_y": -square_speed},
    {"color": RED, "x": start_x, "y": start_y,
     "speed_x": random.choice([-square_speed, square_speed]), "speed_y": -square_speed},
    {"color": GREEN, "x": start_x, "y": start_y,
     "speed_x": random.choice([-square_speed, square_speed]), "speed_y": -square_speed},
    {"color": YELLOW, "x": start_x, "y": start_y,
     "speed_x": random.choice([-square_speed, square_speed]), "speed_y": -square_speed}
]

# Trail settings
trail = {i: [] for i in range(len(squares))}
trail_length = 10

# Sound
hit_sound = pygame.mixer.Sound("hit.mp3")  # Ensure 'hit.mp3' is in the same directory
hit_sound.set_volume(0.2)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Freely Moving Squares with Collision")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Function to detect collision between two squares
def detect_collision(sq1, sq2):
    return (sq1["x"] < sq2["x"] + square_size and
            sq1["x"] + square_size > sq2["x"] and
            sq1["y"] < sq2["y"] + square_size and
            sq1["y"] + square_size > sq2["y"])

# Function to resolve collision by adjusting speed directions and positions
def resolve_collision(square1, square2):
    # Calculate the overlap distance in both X and Y axes
    overlap_x = (square1["x"] + square_size // 2) - (square2["x"] + square_size // 2)
    overlap_y = (square1["y"] + square_size // 2) - (square2["y"] + square_size // 2)

    # Adjust speed for each square based on the overlap
    if abs(overlap_x) > abs(overlap_y):  # Horizontal overlap is more significant
        square1["speed_x"] *= -1
        square2["speed_x"] *= -1
        # Adjust positions to avoid sticking
        adjustment = square_size - abs(overlap_x) // 2
        if overlap_x > 0:
            square1["x"] += adjustment
            square2["x"] -= adjustment
        else:
            square1["x"] -= adjustment
            square2["x"] += adjustment
    else:  # Vertical overlap is more significant
        square1["speed_y"] *= -1
        square2["speed_y"] *= -1
        # Adjust positions to avoid sticking
        adjustment = square_size - abs(overlap_y) // 2
        if overlap_y > 0:
            square1["y"] += adjustment
            square2["y"] -= adjustment
        else:
            square1["y"] -= adjustment
            square2["y"] += adjustment

    # Play hit sound
    if hit_sound:
        hit_sound.play()

# Function to handle wall collisions and prevent the square from getting stuck
def handle_wall_collisions(square):
    # Handle horizontal wall collisions
    if square["x"] <= 0:
        square["x"] = 0
        square["speed_x"] *= -1
        hit_sound.play()
    elif square["x"] >= SCREEN_WIDTH - square_size:
        square["x"] = SCREEN_WIDTH - square_size
        square["speed_x"] *= -1
        hit_sound.play()

    # Handle vertical wall collisions
    if square["y"] <= 0:
        square["y"] = 0
        square["speed_y"] *= -1
        hit_sound.play()
    elif square["y"] >= SCREEN_HEIGHT - square_size:
        square["y"] = SCREEN_HEIGHT - square_size
        square["speed_y"] *= -1
        hit_sound.play()

# Function to load level from CSV
def load_level(filename):
    level_data = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            level_data.append(row)
    return level_data

# Function to rotate the level 90 degrees clockwise
def rotate_level_90(level_data):
    rotated_level = []
    rows = len(level_data)
    cols = len(level_data[0])

    for col in range(cols):
        new_row = []
        for row in range(rows-1, -1, -1):  # Traverse rows in reverse order
            new_row.append(level_data[row][col])
        rotated_level.append(new_row)

    return rotated_level

# Set initial position and speed for the green square
green_square_speed = 1
green_square_direction = 1  # 1 for moving down, -1 for moving up
green_square_y = SCREEN_HEIGHT // 2  # Start at the center vertically

# Function to update the green square's movement
def update_green_square_position():
    global green_square_y, green_square_direction

    # Update the position
    green_square_y += green_square_speed * green_square_direction

    # Check if it reached the top or bottom and reverse direction
    if green_square_y <= 180:
        green_square_y = 180
        green_square_direction = 1  # Move down
    elif green_square_y >= (SCREEN_HEIGHT - square_size * 5)-320:  # Considering the green square's height
        green_square_y = (SCREEN_HEIGHT - square_size * 5)-320
        green_square_direction = -1  # Move up

# Update the `draw_level` function to draw the green square at the updated position
def draw_level(level_data):
    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            if cell == "w":  # Draw a white square
                pygame.draw.rect(screen, WHITE, (col_index * square_size, row_index * square_size, square_size, square_size))
            if cell == "r":  # Draw a red square (game over)
                pygame.draw.rect(screen, RED, (col_index * square_size, row_index * square_size, square_size, square_size))
            if cell == "g":  # Draw the green square
                pygame.draw.rect(screen, GREEN, (col_index * square_size, green_square_y, square_size*7, square_size*5))  # Use green_square_y for vertical position


# Function to check if a square collides with a white square
def detect_collision_with_white_square(square, level_data):
    square_rect = pygame.Rect(square["x"], square["y"], square_size, square_size)

    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            if cell == "w":
                white_square_rect = pygame.Rect(
                    col_index * square_size, row_index * square_size, square_size, square_size
                )
                
                if square_rect.colliderect(white_square_rect):
                    # Calculate penetration depth for each side
                    overlap_top = white_square_rect.bottom - square_rect.top
                    overlap_bottom = square_rect.bottom - white_square_rect.top
                    overlap_left = white_square_rect.right - square_rect.left
                    overlap_right = square_rect.right - white_square_rect.left
                    
                    # Find the minimum overlap (closest collision side)
                    overlaps = {
                        "top": overlap_top,
                        "bottom": overlap_bottom,
                        "left": overlap_left,
                        "right": overlap_right,
                    }
                    collision_side = min(overlaps, key=overlaps.get)
                    
                    # Set the collision normal based on the side
                    if collision_side == "top":
                        normal = (0, -1)
                        square["y"] = white_square_rect.bottom  # Prevent overlap
                    elif collision_side == "bottom":
                        normal = (0, 1)
                        square["y"] = white_square_rect.top - square_size
                    elif collision_side == "left":
                        normal = (-1, 0)
                        square["x"] = white_square_rect.right
                    else:  # "right"
                        normal = (1, 0)
                        square["x"] = white_square_rect.left - square_size
                    
                    # Compute reflection vector
                    velocity = (square["speed_x"], square["speed_y"])
                    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
                    reflection = (
                        velocity[0] - 2 * dot_product * normal[0],
                        velocity[1] - 2 * dot_product * normal[1]
                    )
                    
                    # Update square's velocity
                    square["speed_x"], square["speed_y"] = reflection
                    return True
    return False

# Function to check if a square collides with a "g" (green) cell
def detect_collision_with_green_square(square, level_data):
    # Create a rectangle for the moving square
    square_rect = pygame.Rect(square["x"], square["y"], square_size, square_size)
    
    # Calculate the square's potential new position based on its speed
    potential_rect = square_rect.move(square["speed_x"], square["speed_y"])

    # Loop through level data to find green squares ("g")
    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            if cell == "g":
                # Create a rectangle for the green square with its adjusted size
                green_square_rect = pygame.Rect(
                    col_index * square_size,
                    green_square_y,  # Use green square's updated vertical position
                    square_size * 7,  # Adjust width to match the green square's width
                    square_size * 5   # Adjust height to match the green square's height
                )
                
                # Check for collision with potential new position
                if potential_rect.colliderect(green_square_rect):
                    # Calculate overlap on each side
                    overlap_top = green_square_rect.bottom - square_rect.top
                    overlap_bottom = square_rect.bottom - green_square_rect.top
                    overlap_left = green_square_rect.right - square_rect.left
                    overlap_right = square_rect.right - green_square_rect.left
                    
                    # Determine the closest side of collision
                    overlaps = {
                        "top": overlap_top,
                        "bottom": overlap_bottom,
                        "left": overlap_left,
                        "right": overlap_right,
                    }
                    collision_side = min(overlaps, key=overlaps.get)
                    
                    # Set the collision normal based on the collision side
                    if collision_side == "top":
                        normal = (0, -1)
                        square["y"] = green_square_rect.bottom  # Adjust position
                    elif collision_side == "bottom":
                        normal = (0, 1)
                        square["y"] = green_square_rect.top - square_size
                    elif collision_side == "left":
                        normal = (-1, 0)
                        square["x"] = green_square_rect.right
                    else:  # "right"
                        normal = (1, 0)
                        square["x"] = green_square_rect.left - square_size
                    
                    # Compute reflection vector
                    velocity = (square["speed_x"], square["speed_y"])
                    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
                    reflection = (
                        velocity[0] - 2 * dot_product * normal[0],
                        velocity[1] - 2 * dot_product * normal[1]
                    )
                    
                    # Update the square's velocity
                    square["speed_x"], square["speed_y"] = reflection
                    return True  # Collision occurred
    return False  # No collision




# Function to check if a square collides with a "game over" square (r)
def detect_collision_with_game_over_square(square, level_data):
    square_rect = pygame.Rect(square["x"], square["y"], square_size, square_size)

    for row_index, row in enumerate(level_data):
        for col_index, cell in enumerate(row):
            if cell == "r":  # Check for game over square (r)
                game_over_rect = pygame.Rect(
                    col_index * square_size, row_index * square_size, square_size, square_size
                )
                
                if square_rect.colliderect(game_over_rect):
                    # Trigger game over action
                    return True  # Game over condition met
    return False



# Function to handle game over
def handle_game_over():
    font = pygame.font.SysFont(None, 55)
    text = font.render("GAME OVER", True, RED)
    screen.blit(text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3))
    pygame.display.flip()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting
    pygame.quit()
    sys.exit()


# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Load the level (from the CSV file)
    level_data = load_level('level_data4.csv')  # Make sure this CSV file exists in the directory

    # Rotate the level 90 degrees clockwise
    level_data = rotate_level_90(level_data)
# Inside the main game loop
    update_green_square_position()  # Update green square's movement

    # Move each square and check for collisions
    for i, square in enumerate(squares):
        # Move the square
        square["x"] += square["speed_x"]
        square["y"] += square["speed_y"]

        # Handle wall collisions
        handle_wall_collisions(square)

        # Check for collisions with other squares
        for j, other_square in enumerate(squares):
            if i != j and detect_collision(square, other_square):
                resolve_collision(square, other_square)

        # Check for collisions with white squares
        if detect_collision_with_white_square(square, level_data):
            # Play the hit sound
            hit_sound.play()

                  # Check if square collides with the game-over square ("r")
        if detect_collision_with_game_over_square(square, level_data):
            handle_game_over()  # End the game if it collides with "r"

          # Check for collisions with green squares
        if detect_collision_with_green_square(square, level_data):
          # Optional: Add additional actions specific to green square collisions
          pass


        # Update the trail for the square
        trail[i].append((square["x"] + square_size // 2, square["y"] + square_size // 2))
        if len(trail[i]) > trail_length:
            trail[i].pop(0)

    # Clear the screen
    screen.fill(BLACK)

    # Draw the level
    draw_level(level_data)

    # Draw each square and its trail
    for i, square in enumerate(squares):
        # Draw the trail
        for k, pos in enumerate(trail[i]):
            alpha = int(255 * (k / len(trail[i])))  # Gradual fade-out
            color = (*square["color"], alpha)  # Add alpha to the color
            surface = pygame.Surface((10, 10), pygame.SRCALPHA)  # Transparent surface
            pygame.draw.circle(surface, color, (5, 5), 5)
            screen.blit(surface, (pos[0] - 5, pos[1] - 5))

        # Draw the square with a thin white border
        pygame.draw.rect(screen, WHITE, (square["x"] - 1, square["y"] - 1, square_size + 2, square_size + 2))  # Border
        pygame.draw.rect(screen, square["color"], (square["x"], square["y"], square_size, square_size))  # Square

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
