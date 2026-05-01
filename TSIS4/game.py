import pygame
import random
import json
from db import save_score, get_personal_best, get_leaderboard

pygame.init()

WIDTH = 600
HEIGHT = 400
CELL = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake TSIS4")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

username = ""
settings = {}
snake_color = (0, 200, 0)


def load_settings():
    global settings, snake_color
    with open("settings.json", "r") as file:
        settings = json.load(file)
    snake_color = tuple(settings["snake_color"])


def save_settings():
    with open("settings.json", "w") as file:
        json.dump(settings, file, indent=4)


def draw_text(text, x, y, color=(255, 255, 255)):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))


def draw_button(text, x, y, w, h):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    color = (80, 80, 80)
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        color = (120, 120, 120)

    pygame.draw.rect(screen, color, (x, y, w, h), border_radius=8)

    text_img = font.render(text, True, (255, 255, 255))
    text_rect = text_img.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(text_img, text_rect)

    if x < mouse[0] < x + w and y < mouse[1] < y + h and click[0]:
        pygame.time.delay(200)
        return True
    return False


def username_screen():
    global username
    typing = True

    while typing:
        screen.fill((0, 0, 0))
        draw_text("Enter username:", 190, 100)
        draw_text(username, 220, 150)
        draw_text("Press Enter to continue", 170, 220)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and username != "":
                    typing = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode


def create_food(snake, obstacles):
    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake and (x, y) not in obstacles:
            return (x, y)


def create_power_up(snake, obstacles, food, poison):
    types = ["speed", "slow", "shield"]

    while True:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)

        if (x, y) not in snake and (x, y) not in obstacles and (x, y) != food and (x, y) != poison:
            return {
                "pos": (x, y),
                "type": random.choice(types),
                "spawn_time": pygame.time.get_ticks()
            }


def create_obstacles(snake, count):
    obstacles = []

    while len(obstacles) < count:
        x = random.randrange(0, WIDTH, CELL)
        y = random.randrange(0, HEIGHT, CELL)
        block = (x, y)

        head = snake[0]

        if (
            block not in snake
            and block not in obstacles
            and abs(block[0] - head[0]) > CELL * 2
            and abs(block[1] - head[1]) > CELL * 2
        ):
            obstacles.append(block)

    return obstacles


def draw_grid():
    if settings["grid"]:
        for x in range(0, WIDTH, CELL):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))

        for y in range(0, HEIGHT, CELL):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))


def play():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = "RIGHT"

    score = 0
    level = 1
    base_speed = 8
    speed = base_speed

    obstacles = []

    food = create_food(snake, obstacles)
    poison = create_food(snake, obstacles)

    power_up = None
    active_power = None
    power_start_time = 0
    shield = False

    last_power_spawn = pygame.time.get_ticks()

    personal_best = get_personal_best(username)
    playing = True

    while playing:
        now = pygame.time.get_ticks()

        screen.fill((0, 0, 0))
        draw_grid()

        if power_up is None and now - last_power_spawn > 5000:
            power_up = create_power_up(snake, obstacles, food, poison)
            last_power_spawn = now

        if power_up is not None and now - power_up["spawn_time"] > 8000:
            power_up = None

        if active_power in ["speed", "slow"] and now - power_start_time > 5000:
            active_power = None
            speed = base_speed + (level - 1) * 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

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
            head_y -= CELL
        elif direction == "DOWN":
            head_y += CELL
        elif direction == "LEFT":
            head_x -= CELL
        elif direction == "RIGHT":
            head_x += CELL

        new_head = (head_x, head_y)

        collision = (
            head_x < 0 or head_x >= WIDTH or
            head_y < 0 or head_y >= HEIGHT or
            new_head in snake or
            new_head in obstacles
        )

        if collision:
            if shield:
                shield = False
                new_head = snake[0]
            else:
                playing = False

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            food = create_food(snake, obstacles)

            if score % 3 == 0:
                level += 1
                base_speed += 2
                speed = base_speed

                if level >= 3:
                    obstacles = create_obstacles(snake, level + 2)

        else:
            snake.pop()

        if new_head == poison:
            if len(snake) <= 2:
                playing = False
            else:
                snake.pop()
                snake.pop()

            poison = create_food(snake, obstacles)

        if power_up is not None and new_head == power_up["pos"]:
            active_power = power_up["type"]
            power_start_time = now

            if active_power == "speed":
                speed = base_speed + 5

            elif active_power == "slow":
                speed = max(4, base_speed - 4)

            elif active_power == "shield":
                shield = True

            power_up = None

        pygame.draw.rect(screen, (255, 0, 0), (*food, CELL, CELL))
        pygame.draw.rect(screen, (120, 0, 0), (*poison, CELL, CELL))

        if power_up is not None:
            if power_up["type"] == "speed":
                color = (255, 255, 0)
            elif power_up["type"] == "slow":
                color = (0, 150, 255)
            else:
                color = (180, 0, 255)

            pygame.draw.rect(screen, color, (*power_up["pos"], CELL, CELL))

        for block in obstacles:
            pygame.draw.rect(screen, (100, 100, 100), (*block, CELL, CELL))

        for block in snake:
            pygame.draw.rect(screen, snake_color, (*block, CELL, CELL))

        draw_text(f"Score: {score}", 10, 10)
        draw_text(f"Level: {level}", 10, 40)
        draw_text(f"Best: {personal_best}", 10, 70)

        if shield:
            draw_text("Shield: ON", 430, 10)

        if active_power == "speed":
            draw_text("Speed Boost", 420, 40, (255, 255, 0))
        elif active_power == "slow":
            draw_text("Slow Motion", 420, 40, (0, 150, 255))

        pygame.display.update()
        clock.tick(speed)

    save_score(username, score, level)
    game_over(score, level, personal_best)


def game_over(score, level, personal_best):
    waiting = True

    while waiting:
        screen.fill((0, 0, 0))

        draw_text("GAME OVER", 220, 70)
        draw_text(f"Score: {score}", 230, 120)
        draw_text(f"Level: {level}", 230, 150)
        draw_text(f"Best: {max(personal_best, score)}", 230, 180)

        if draw_button("Retry", 200, 230, 200, 45):
            play()

        if draw_button("Main Menu", 200, 290, 200, 45):
            waiting = False
            menu_screen()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def leaderboard_screen():
    waiting = True

    while waiting:
        data = get_leaderboard()

        screen.fill((0, 0, 0))
        draw_text("LEADERBOARD", 210, 30)

        y = 80
        rank = 1

        for row in data:
            name, score, level, date = row
            draw_text(f"{rank}. {name} | {score} | Level {level}", 80, y)
            y += 30
            rank += 1

        if draw_button("Back", 200, 330, 200, 45):
            waiting = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def settings_screen():
    global snake_color

    waiting = True

    while waiting:
        screen.fill((0, 0, 0))

        draw_text("SETTINGS", 240, 50)
        draw_text(f"Grid: {settings['grid']}", 240, 110)
        draw_text(f"Sound: {settings['sound']}", 240, 160)

        if draw_button("Toggle Grid", 190, 200, 220, 40):
            settings["grid"] = not settings["grid"]

        if draw_button("Toggle Sound", 190, 250, 220, 40):
            settings["sound"] = not settings["sound"]

        if draw_button("Change Color", 190, 300, 220, 40):
            settings["snake_color"] = [
                random.randint(50, 255),
                random.randint(50, 255),
                random.randint(50, 255)
            ]
            snake_color = tuple(settings["snake_color"])

        if draw_button("Save & Back", 190, 350, 220, 40):
            save_settings()
            waiting = False

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def menu_screen():
    menu = True

    while menu:
        screen.fill((0, 0, 0))

        draw_text("SNAKE GAME", 220, 70)

        if draw_button("Play", 200, 130, 200, 45):
            play()

        if draw_button("Leaderboard", 200, 190, 200, 45):
            leaderboard_screen()

        if draw_button("Settings", 200, 250, 200, 45):
            settings_screen()

        if draw_button("Quit", 200, 310, 200, 45):
            pygame.quit()
            exit()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()


def run():
    load_settings()
    username_screen()
    menu_screen()