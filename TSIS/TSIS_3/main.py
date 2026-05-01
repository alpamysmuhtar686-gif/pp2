#Imports
import pygame, sys
from pygame.locals import *
from racer import run_game
from ui import show_standalone_leaderboard, show_settings_screen, show_main_menu
#Initialzing 
pygame.init()
        # Game loop
FPS = 60
DISPLAYSURF = pygame.display.set_mode((400,600))
FramePerSec = pygame.time.Clock()
while True:
    choice = show_main_menu(DISPLAYSURF)
    if choice == "play":
        run_game(DISPLAYSURF)
    elif choice == "leaderboard":
        show_standalone_leaderboard(DISPLAYSURF)  # Pass dummy score since we're just viewing
    elif choice == "settings":
        show_settings_screen(DISPLAYSURF)
    elif choice == "quit":
        pygame.quit()
        sys.exit()
    pygame.display.update()
    FramePerSec.tick(FPS)