"""
Main game class
"""
import pygame
from player import Player, GameMode
from bullet import Bullet
from levels import LevelManager

class Game:
    def __init__(self):
        # Screen dimensions
        self.WIDTH = 800
        self.HEIGHT = 600
        self.FPS = 60
        
        # Create screen
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("VimQuest - A Vim Adventure")
        
        # Clock for FPS
        self.clock = pygame.time.Clock()
        
        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # Initialize player
        self.player = Player(400, 300)
        self.all_sprites.add(self.player)
        
        # Initialize level manager
        self.level_manager = LevelManager()
        
        # Font for UI
        self.font_large = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.running = True
        
    def handle_events(self):
        """Handle all game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                # Handle normal mode keys
                self.player.handle_input(event.key)
            
            # Handle unicode input for insert mode (text input)
            elif event.type == pygame.TEXTINPUT:
                if self.player.mode == GameMode.INSERT:
                    self.player.shoot_buffer += event.text
            
            # Handle key up for special keys in insert mode
            if event.type == pygame.KEYDOWN and self.player.mode == GameMode.INSERT:
                if event.key == pygame.K_RETURN:
                    # Shoot all characters in buffer
                    self.shoot_bullets()
                    self.player.shoot_buffer = ""
    
    def shoot_bullets(self):
        """Create bullets from the shoot buffer"""
        if not self.player.shoot_buffer:
            return
        
        # Create bullet for each character
        for i, char in enumerate(self.player.shoot_buffer):
            # Spread bullets slightly
            offset_y = (i - len(self.player.shoot_buffer) / 2) * 8
            bullet = Bullet(
                self.player.x + self.player.size,
                self.player.y + offset_y,
                char,
                direction=(1, 0)
            )
            self.all_sprites.add(bullet)
            self.bullets.add(bullet)
    
    def check_collisions(self):
        """Check collisions between player and obstacles"""
        level = self.level_manager.get_current_level()
        collision_rects = level.get_collision_rects()
        
        player_rect = self.player.rect
        
        for obs_rect in collision_rects:
            if player_rect.colliderect(obs_rect):
                # Simple collision response - push player back
                # This is a basic implementation
                if self.player.x < obs_rect.x:
                    self.player.x = obs_rect.x - self.player.size
                elif self.player.x > obs_rect.right:
                    self.player.x = obs_rect.right
                if self.player.y < obs_rect.y:
                    self.player.y = obs_rect.y - self.player.size
                elif self.player.y > obs_rect.bottom:
                    self.player.y = obs_rect.bottom
                
                self.player.update()
    
    def update(self):
        """Update game state"""
        self.all_sprites.update()
        self.check_collisions()
    
    def draw(self):
        """Draw everything"""
        # Clear screen
        self.screen.fill((200, 200, 200))
        
        # Draw level
        level = self.level_manager.get_current_level()
        level.draw_obstacles(self.screen)
        
        # Draw sprites
        self.all_sprites.draw(self.screen)
        
        # Draw UI
        self.draw_ui()
        
        # Update display
        pygame.display.flip()
    
    def draw_ui(self):
        """Draw user interface elements"""
        # Level name
        level = self.level_manager.get_current_level()
        level_text = self.font_small.render(f"Level: {level.name}", True, (0, 0, 0))
        self.screen.blit(level_text, (10, 10))
        
        # Mode indicator
        mode_text = self.font_small.render(self.player.get_mode_text(), True, (0, 0, 0))
        self.screen.blit(mode_text, (10, 30))
        
        # Instructions
        if self.player.mode == GameMode.NORMAL:
            inst_text = self.font_small.render("hjkl: move | i: insert mode", True, (100, 100, 100))
            self.screen.blit(inst_text, (10, 550))
        else:
            inst_text = self.font_small.render("Type letters and press Enter to shoot | Esc: normal mode", True, (100, 100, 100))
            self.screen.blit(inst_text, (10, 550))
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.FPS)
