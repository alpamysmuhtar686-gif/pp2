import pygame
import random

pygame.init()

w, h = 600, 400
cell = 20

screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

black = (0, 0, 0)
green = (0, 200, 0)
red = (255, 0, 0)
white = (255, 255, 255)

snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

score = 0
level = 1
speed = 8


def create_food():
    while True:
        x = random.randrange(0, w, cell)
        y = random.randrange(0, h, cell)

        if (x, y) not in snake:
            return x, y


food = create_food()
run = True

while run:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    head_x, head_y = snake[0]

    if direction == "UP":
        head_y -= cell
    elif direction == "DOWN":
        head_y += cell
    elif direction == "LEFT":
        head_x -= cell
    elif direction == "RIGHT":
        head_x += cell

    new_head = (head_x, head_y)

    if head_x < 0 or head_x >= w or head_y < 0 or head_y >= h:
        run = False

    if new_head in snake:
        run = False

    if not run:
        break

    snake.insert(0, new_head)

    if new_head == food:
        score += 1
        food = create_food()

        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        snake.pop()

    pygame.draw.rect(screen, red, (food[0], food[1], cell, cell))

    for part in snake:
        pygame.draw.rect(screen, green, (part[0], part[1], cell, cell))

    text = font.render(f"Score: {score}  Level: {level}", True, white)
    screen.blit(text, (20, 20))

    pygame.display.update()
    clock.tick(speed)

screen.fill(black)

game_over_text = font.render("GAME OVER", True, red)
final_score_text = font.render(f"Score: {score}  Level: {level}", True, white)

screen.blit(game_over_text, (w // 2 - 100, h // 2 - 40))
screen.blit(final_score_text, (w // 2 - 110, h // 2 + 10))
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()