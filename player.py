"""
Player character class
"""
import pygame
from enum import Enum

class GameMode(Enum):
    NORMAL = 1  # Vim normal mode - movement
    INSERT = 2  # Vim insert mode - shooting

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.size = 16
        self.x = x
        self.y = y
        self.mode = GameMode.NORMAL
        self.shoot_buffer = ""  # Buffer for typed characters in insert mode
        
        # Create player sprite (simple pixel art human)
        self.image = self.create_sprite()
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
        # Movement speed
        self.speed = 8
        
    def create_sprite(self):
        """Create a simple pixel-style human character"""
        surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Head (circle)
        pygame.draw.circle(surface, (255, 200, 150), (8, 4), 3)
        
        # Body (rectangle)
        pygame.draw.rect(surface, (0, 0, 255), (6, 8, 4, 5))
        
        # Arms
        pygame.draw.line(surface, (255, 200, 150), (6, 9), (3, 11), 1)
        pygame.draw.line(surface, (255, 200, 150), (10, 9), (13, 11), 1)
        
        # Legs
        pygame.draw.line(surface, (0, 0, 0), (7, 13), (6, 16), 1)
        pygame.draw.line(surface, (0, 0, 0), (9, 13), (10, 16), 1)
        
        return surface
    
    def handle_input(self, key):
        """Handle input based on game mode"""
        if self.mode == GameMode.NORMAL:
            self.handle_normal_mode(key)
        elif self.mode == GameMode.INSERT:
            self.handle_insert_mode(key)
    
    def handle_normal_mode(self, key):
        """Handle vim normal mode controls"""
        if key == pygame.K_i:
            # Enter insert mode
            self.mode = GameMode.INSERT
            self.shoot_buffer = ""
        elif key == pygame.K_h:
            # Move left
            new_x = self.x - self.speed
            if new_x >= 0:
                self.x = new_x
        elif key == pygame.K_j:
            # Move down
            new_y = self.y + self.speed
            if new_y <= 600 - self.size:
                self.y = new_y
        elif key == pygame.K_k:
            # Move up
            new_y = self.y - self.speed
            if new_y >= 0:
                self.y = new_y
        elif key == pygame.K_l:
            # Move right
            new_x = self.x + self.speed
            if new_x <= 800 - self.size:
                self.x = new_x
    
    def handle_insert_mode(self, key):
        """Handle vim insert mode (typing/shooting)"""
        if key == pygame.K_ESCAPE:
            # Exit insert mode
            self.mode = GameMode.NORMAL
            self.shoot_buffer = ""
        elif key == pygame.K_BACKSPACE:
            # Delete last character
            self.shoot_buffer = self.shoot_buffer[:-1]
        elif key == pygame.K_RETURN:
            # Shoot the buffer - this is handled in game.py
            pass
    
    def get_typed_char(self, event):
        """Get character from unicode event"""
        if event.type == pygame.KEYDOWN and self.mode == GameMode.INSERT:
            if event.unicode and event.unicode.isprintable():
                self.shoot_buffer += event.unicode
    
    def update(self):
        """Update player position"""
        self.rect.topleft = (self.x, self.y)
    
    def get_mode_text(self):
        """Get text to display for current mode"""
        if self.mode == GameMode.NORMAL:
            return "-- NORMAL --"
        elif self.mode == GameMode.INSERT:
            return f"-- INSERT -- {self.shoot_buffer}"
