"""
Bullet/Alphabet class for projectiles
"""
import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, char, direction=(1, 0)):
        super().__init__()
        self.char = char
        self.speed = 8
        self.direction = direction
        self.x = x
        self.y = y
        
        # Create text surface
        font = pygame.font.Font(None, 24)
        self.image = font.render(char, True, (255, 100, 100))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        
    def update(self):
        """Update bullet position"""
        self.x += self.direction[0] * self.speed
        self.y += self.direction[1] * self.speed
        self.rect.topleft = (self.x, self.y)
        
        # Remove if off screen
        if self.x < 0 or self.x > 800 or self.y < 0 or self.y > 600:
            self.kill()
