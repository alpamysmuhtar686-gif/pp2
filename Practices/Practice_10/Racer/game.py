import pygame
import random
import os

# Initialize pygame
pygame.init()

# Create clock to control FPS
clock = pygame.time.Clock()

# Window size
w = 600
h = 800

# Create game window
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Racer")

# Get path to images folder
BASE_PATH = os.path.dirname(__file__)
IMG_DIR = os.path.join(BASE_PATH, "images")

# Score for passed enemy cars
score1 = 0

# Load and resize background image
background = pygame.image.load(os.path.join(IMG_DIR, "Street.png"))
background = pygame.transform.scale(background, (w, h))

# Load and resize player car
player = pygame.image.load(os.path.join(IMG_DIR, "Player.png"))
player = pygame.transform.scale(player, (75, 150))

# Create rectangle for player position and collision
player_rect = player.get_rect()
player_rect.center = (w // 2, h - 150)

# Load and resize enemy car
enemy = pygame.image.load(os.path.join(IMG_DIR, "Enemy.png"))
enemy = pygame.transform.scale(enemy, (75, 125))

# Create rectangle for enemy position and collision
enemy_rect = enemy.get_rect()
enemy_rect.x = random.randint(60, w - 130)
enemy_rect.y = -150

# Load and resize coin
coin = pygame.image.load(os.path.join(IMG_DIR, "Coin.png"))
coin = pygame.transform.scale(coin, (75, 125))

# Create rectangle for coin position and collision
coin_rect = coin.get_rect()
coin_rect.x = random.randint(60, w - 130)
coin_rect.y = -150

# Font for Game Over text
font = pygame.font.SysFont("Arial", 60)

# Main game variables
run = True
score = 0  # Score for collected coins

# Main game loop
while run:
    # Check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Check collision with enemy car
    if player_rect.colliderect(enemy_rect):
        text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(text, (w // 2 - 170, h // 2 - 30))
        pygame.display.update()
        pygame.time.delay(2000)
        run = False

    # Check collision with coin
    if player_rect.colliderect(coin_rect):
        score += 1
        coin_rect.y = -130
        coin_rect.x = random.randint(60, w - 130)
        pygame.display.update()

    # Get pressed keys
    keys = pygame.key.get_pressed()

    # Move player left
    if keys[pygame.K_LEFT] and player_rect.left > 0:
        player_rect.x -= 5

    # Move player right
    if keys[pygame.K_RIGHT] and player_rect.right < w:
        player_rect.x += 5

    # Move enemy car down
    enemy_rect.y += 5

    # If enemy car goes out of screen, return it to the top
    if enemy_rect.top > h:
        enemy_rect.y = -130
        enemy_rect.x = random.randint(60, w - 130)
        score1 += 1

    # Move coin down
    coin_rect.y += 3

    # If coin goes out of screen, return it to the top
    if coin_rect.top > h:
        coin_rect.y = -130
        coin_rect.x = random.randint(60, w - 130)

    # Draw background
    screen.blit(background, (0, 0))

    # Draw player, enemy and coin
    screen.blit(player, player_rect)
    screen.blit(enemy, enemy_rect)
    screen.blit(coin, coin_rect)

    # Show collected coins
    score_text = pygame.font.SysFont("Arial", 30).render(
        f"Coins: {score}", True, (255, 255, 255)
    )
    screen.blit(score_text, (400, 20))

    # Show passed enemy cars
    score1_text = pygame.font.SysFont("Arial", 30).render(
        f"Score: {score1}", True, (255, 255, 255)
    )
    screen.blit(score1_text, (400, 55))

    # Control FPS
    clock.tick(60)

    # Update screen
    pygame.display.update()

# Close pygame
pygame.quit()