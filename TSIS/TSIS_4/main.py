import pygame
from game import show_main_menu, run_game, show_standalone_leaderboard, show_settings_screen
import sys

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Snake Game")
while True:
    # Show main menu and get choice
    choice = show_main_menu(screen)
    
    if choice == "play":
        run_game(screen)
    elif choice == "leaderboard":
        show_standalone_leaderboard(screen)  # Pass dummy score since we're just viewing
    elif choice == "settings":
        show_settings_screen(screen)
    elif choice == "quit":
        pygame.quit()
        sys.exit()