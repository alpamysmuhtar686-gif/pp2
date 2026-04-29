import pygame
import random

# Запускаем pygame
pygame.init()

# Размер окна и размер одной клетки
w, h = 600, 400
cell = 20

# Создаем окно игры
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Snake")

# Настройки времени и шрифта
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 30)

# Цвета
black = (0, 0, 0)
green = (0, 200, 0)
red = (255, 0, 0)
white = (255, 255, 255)

# Начальное положение змейки
snake = [(100, 100), (80, 100), (60, 100)]
direction = "RIGHT"

# Очки, уровень и скорость
score = 0
level = 1
speed = 8

# Таймер еды: через 50 кадров еда исчезает и появляется новая
food_timer = 0
food_lifetime = 50


# Функция для создания еды в случайном месте
def create_food():
    while True:
        x = random.randrange(0, w, cell)
        y = random.randrange(0, h, cell)

        # Еда не должна появляться внутри змейки
        if (x, y) not in snake:
            return x, y


# Создаем первую еду
food = create_food()
run = True

# Основной игровой цикл
while run:
    screen.fill(black)

    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        # Управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            if event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            if event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            if event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # Увеличиваем таймер еды каждый кадр
    food_timer += 1

    # Берем координаты головы змейки
    head_x, head_y = snake[0]

    # Двигаем голову в выбранном направлении
    if direction == "UP":
        head_y -= cell
    elif direction == "DOWN":
        head_y += cell
    elif direction == "LEFT":
        head_x -= cell
    elif direction == "RIGHT":
        head_x += cell

    # Новая позиция головы
    new_head = (head_x, head_y)

    # Проверка столкновения со стенами
    if head_x < 0 or head_x >= w or head_y < 0 or head_y >= h:
        run = False

    # Проверка столкновения с самой собой
    if new_head in snake:
        run = False

    # Если игра закончилась, выходим из цикла
    if not run:
        break

    # Добавляем новую голову змейки
    snake.insert(0, new_head)

    # Если еда долго не съедена, она исчезает и появляется новая
    if food_timer >= food_lifetime:
        food = create_food()
        food_timer = 0

    # Если змейка съела еду
    if new_head == food:
        score += random.randint(1, 5)
        food = create_food()
        food_timer = 0

        # Повышаем уровень и скорость, если score кратен 4
        if score % 4 == 0:
            level += 1
            speed += 2
    else:
        # Если еда не съедена, убираем хвост
        snake.pop()

    # Рисуем еду
    pygame.draw.rect(screen, red, (food[0], food[1], cell, cell))

    # Рисуем змейку
    for part in snake:
        pygame.draw.rect(screen, green, (part[0], part[1], cell, cell))

    # Показываем счет и уровень
    text = font.render(f"Score: {score}  Level: {level}", True, white)
    screen.blit(text, (20, 20))

    # Обновляем экран
    pygame.display.update()

    # Контролируем скорость игры
    clock.tick(speed)

# Экран после проигрыша
screen.fill(black)

game_over_text = font.render("GAME OVER", True, red)
final_score_text = font.render(f"Score: {score}  Level: {level}", True, white)

screen.blit(game_over_text, (w // 2 - 100, h // 2 - 40))
screen.blit(final_score_text, (w // 2 - 110, h // 2 + 10))

pygame.display.update()
pygame.time.delay(2000)

# Завершаем pygame
pygame.quit()