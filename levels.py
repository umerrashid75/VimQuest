"""
Level design and management
"""
import pygame

class Level:
    def __init__(self, name, description, obstacles, enemies):
        self.name = name
        self.description = description
        self.obstacles = obstacles  # List of (x, y, width, height)
        self.enemies = enemies  # List of (x, y) positions
        
    def draw_obstacles(self, surface):
        """Draw all obstacles"""
        for obs in self.obstacles:
            pygame.draw.rect(surface, (100, 100, 100), obs)
    
    def get_collision_rects(self):
        """Get collision rectangles for obstacles"""
        return [pygame.Rect(obs) for obs in self.obstacles]

class LevelManager:
    def __init__(self):
        self.levels = self.create_levels()
        self.current_level_index = 0
    
    def create_levels(self):
        """Define all game levels"""
        levels = []
        
        # Level 1: The Basics - Simple level with few obstacles
        levels.append(Level(
            name="The Basics",
            description="Learn to move with hjkl and shoot with i",
            obstacles=[
                (100, 100, 60, 20),  # (x, y, width, height)
                (200, 250, 20, 100),
                (400, 150, 100, 20),
                (600, 300, 40, 80),
            ],
            enemies=[]
        ))
        
        # Level 2: The Maze - More complex layout
        levels.append(Level(
            name="The Maze",
            description="Navigate through the winding corridors",
            obstacles=[
                (50, 50, 20, 500),     # Left wall
                (750, 50, 50, 500),    # Right wall
                (50, 50, 700, 20),     # Top wall
                (50, 550, 700, 50),    # Bottom wall
                (150, 150, 200, 20),
                (200, 200, 20, 150),
                (350, 100, 250, 20),
                (400, 200, 20, 200),
                (500, 300, 150, 20),
            ],
            enemies=[]
        ))
        
        # Level 3: Obstacle Course - Dense obstacles
        levels.append(Level(
            name="Obstacle Course",
            description="Get through the dense obstacles to reach the end",
            obstacles=[
                (100, 100, 100, 30),
                (250, 200, 100, 30),
                (400, 100, 100, 30),
                (550, 200, 100, 30),
                (150, 350, 80, 30),
                (350, 300, 80, 30),
                (550, 350, 80, 30),
            ],
            enemies=[]
        ))
        
        return levels
    
    def get_current_level(self):
        """Get the current level"""
        return self.levels[self.current_level_index]
    
    def next_level(self):
        """Move to next level"""
        if self.current_level_index < len(self.levels) - 1:
            self.current_level_index += 1
            return True
        return False
    
    def reset_level(self):
        """Reset current level"""
        pass
