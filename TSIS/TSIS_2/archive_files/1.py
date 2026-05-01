import pygame
import sys

# Initialize Pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((200, 200))
pygame.display.set_caption("set_at Example")

# Fill background with white
screen.fill((255, 255, 255))

# Set a single pixel at (50, 50) to red
screen.set_at((50, 50), (255, 0, 0))

# Update the display
pygame.display.flip()

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()