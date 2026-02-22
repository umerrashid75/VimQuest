"""
VimQuest - A Vim-inspired Adventure Game in Pygame
"""
import pygame
import sys
from game import Game

def main():
    # Initialize Pygame
    pygame.init()
    
    # Create game instance
    game = Game()
    
    # Run the game
    game.run()
    
    # Quit
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
