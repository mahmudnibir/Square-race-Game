# README: Freely Moving Squares Game with Collision Mechanics

## Description
This Python program is a 2D simulation game built with **Pygame**. The game involves colorful squares moving freely within a confined space, interacting with walls, other squares, and obstacles defined by a grid loaded from a CSV file. The game features collision detection, interactive movements, and a "Game Over" condition triggered by collisions with specific cells.

---

## Features
- **Dynamic Movement**: Squares move independently with varying speeds and directions.
- **Collision Detection**:
  - Squares collide and bounce off each other and walls.
  - Interaction with different grid cells triggers unique behaviors.
- **Level Grid**: Levels are defined in a CSV file, allowing flexible customizations.
- **Game Over Condition**: Colliding with specific grid cells ends the game.
- **Sound Effects**: Play on collisions to enhance the interactive experience.
- **Rotating Levels**: Levels are dynamically rotated to add variety.

---

## Requirements
- **Python 3.x**
- **Pygame 2.x**
- A CSV file (e.g., `level_data5.csv`) defining the level layout.
- Sound file (`hit.mp3`) for collision effects.

---

## Installation
1. Install Pygame:
   ```bash
   pip install pygame
   ```
2. Ensure the following files are in the same directory:
   - `level_data5.csv` (level layout)
   - `hit.mp3` (sound effect)

---

## How to Play
1. **Launch the Game**:
   Run the Python file:
   ```bash
   python level1.py 
   ```
   use 1,2,3,4,5 for running different levels
2. **Objective**:
   - Avoid "game over" squares (marked `r` in the CSV file).
   - Interact with the environment dynamically.
3. **Controls**:
   No player control is implemented; observe the simulation.

---

## Level Design
Levels are defined in CSV files. Each cell represents:
- `w`: White block (interactive obstacle).
- `r`: Red block (triggers game over).
- `g`: Green block (special square interaction).

Example CSV:
```
w,w,w,w,w,w
w,g,g,g,g,w
w,r,r,r,r,w
w,w,w,w,w,w
```

---

## Code Overview
### Key Components
- **Square Movement**:
  Squares are initialized with random speeds and move freely.
- **Collision Handling**:
  - Wall collisions reverse direction.
  - Square-to-square collisions calculate overlap and adjust speeds and positions.
- **Level Mechanics**:
  - CSV files load level grids.
  - Rotations add variety to gameplay.

---

## Customization
### Adjust Movement Speed
Modify the `square_speed` variable:
```python
square_speed = 2  # Adjust for faster or slower squares
```

## Known Issues
- Ensure the CSV file and sound file are correctly placed in the directory.
- Adjust `trail_length` or `square_size` for better visual effects if needed.

---

## License
This project is open-source and free to use for educational purposes. Modify and expand it as you wish!

Enjoy the simulation! 🚀