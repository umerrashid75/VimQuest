# VimQuest - A Vim-Inspired Adventure Game

A pygame-based game featuring vim modal controls combined with a unique shooting mechanic.

## Features

- **Vim Modal Controls**: Switch between NORMAL and INSERT modes just like in Vim
  - **NORMAL mode**: Navigate with `hjkl` (h=left, j=down, k=up, l=right)
  - **INSERT mode**: Type letters to shoot them as bullets

- **Pixel Art Character**: Simple pixel-style human character that moves around the level

- **Level Design**: Multiple carefully designed levels with obstacles

- **Unique Shooting Mechanic**: 
  - Press `i` to enter INSERT mode
  - Type any letters
  - Press `Enter` to shoot the letters as alphabet bullets
  - Press `Esc` to return to NORMAL mode

## Installation

1. Install Python 3.8 or higher

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Game

**Option 1: Run with Python 3.12 (Recommended)**
```bash
py -3.12 main.py
```

**Option 2: Use the run script (Windows)**
```bash
# Batch file
run.bat

# PowerShell
.\run.ps1
```

**Option 3: Run with default Python**
```bash
python main.py
```

## Controls

### NORMAL Mode (Movement)
- `h` - Move left
- `j` - Move down  
- `k` - Move up
- `l` - Move right
- `i` - Enter INSERT mode

### INSERT Mode (Shooting)
- Type any letters to add to your shot
- `Enter` - Shoot all typed letters as bullets
- `Backspace` - Delete last character
- `Esc` - Return to NORMAL mode

## Project Structure

- `main.py` - Entry point of the game
- `game.py` - Main game class with game loop
- `player.py` - Player character and modal control system
- `bullet.py` - Bullet/alphabet projectile class
- `levels.py` - Level definitions and level manager

## Current Levels

1. **The Basics** - Introduction level with scattered obstacles
2. **The Maze** - Navigate through winding corridors
3. **Obstacle Course** - Dense obstacles to navigate through

## Development Notes

The game is built with pygame and features a modal control system inspired by Vim text editor. The collision system handles obstacles, and the shooting system creates projectiles for each typed character.

Future enhancements could include:
- Enemy AI
- More complex levels
- Sound effects
- Particle effects
- Score/progression system
- More character customization
