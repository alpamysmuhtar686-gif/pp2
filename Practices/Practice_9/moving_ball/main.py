import pygame

class Ball:
    def __init__(self, width, height):
        # Start position (center of screen)
        self.x = width // 2
        self.y = height // 2

        # Ball properties
        self.radius = 25

        # Screen size (for boundary checking)
        self.width = width
        self.height = height

        # Movement speed per key press
        self.speed = 20

    def move(self, dx, dy):
        # Calculate new position
        new_x = self.x + dx
        new_y = self.y + dy

        # Prevent ball from going outside left/right boundaries
        if self.radius <= new_x <= self.width - self.radius:
            self.x = new_x

        # Prevent ball from going outside top/bottom boundaries
        if self.radius <= new_y <= self.height - self.radius:
            self.y = new_y

    def draw(self, screen):
        # Draw red circle (the ball)
        pygame.draw.circle(screen, (255, 50, 50), (self.x, self.y), self.radius)