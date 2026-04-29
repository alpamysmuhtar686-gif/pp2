import pygame
import math

pygame.init()

# Размер окна
w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 180, 0)
blue = (0, 100, 255)

# Заливаем экран белым цветом
screen.fill(white)

font = pygame.font.SysFont("Arial", 20)

# Текущий цвет и инструмент
current_color = black
tool = "brush"

drawing = False
start_pos = None

run = True

while run:
    for event in pygame.event.get():

        # Закрытие окна
        if event.type == pygame.QUIT:
            run = False

        # Нажатия клавиш
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"

            elif event.key == pygame.K_r:
                tool = "rectangle"

            elif event.key == pygame.K_c:
                tool = "circle"

            elif event.key == pygame.K_e:
                tool = "eraser"

            # Новые инструменты
            elif event.key == pygame.K_s:
                tool = "square"

            elif event.key == pygame.K_t:
                tool = "right_triangle"

            elif event.key == pygame.K_q:
                tool = "equilateral_triangle"

            elif event.key == pygame.K_d:
                tool = "rhombus"

            # Выбор цвета
            elif event.key == pygame.K_1:
                current_color = black

            elif event.key == pygame.K_2:
                current_color = red

            elif event.key == pygame.K_3:
                current_color = green

            elif event.key == pygame.K_4:
                current_color = blue

            # Очистка экрана
            elif event.key == pygame.K_SPACE:
                screen.fill(white)

        # Начало рисования
        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        # Конец рисования
        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Прямоугольник
            if tool == "rectangle":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])

                pygame.draw.rect(screen, current_color, (x, y, width, height), 3)

            # Круг
            elif tool == "circle":
                radius = int(
                    ((end_pos[0] - start_pos[0]) ** 2 +
                     (end_pos[1] - start_pos[1]) ** 2) ** 0.5
                )

                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

            # Квадрат
            elif tool == "square":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])

                # Сторона квадрата берется по меньшему расстоянию
                side = min(
                    abs(start_pos[0] - end_pos[0]),
                    abs(start_pos[1] - end_pos[1])
                )

                pygame.draw.rect(screen, current_color, (x, y, side, side), 3)

            # Прямоугольный треугольник
            elif tool == "right_triangle":
                # Три точки: старт, конец по X, конец по Y
                points = [
                    start_pos,
                    (start_pos[0], end_pos[1]),
                    end_pos
                ]

                pygame.draw.polygon(screen, current_color, points, 3)

            # Равносторонний треугольник
            elif tool == "equilateral_triangle":
                side = abs(end_pos[0] - start_pos[0])

                # Высота равностороннего треугольника
                height_triangle = int(side * math.sqrt(3) / 2)

                points = [
                    start_pos,
                    (start_pos[0] + side, start_pos[1]),
                    (start_pos[0] + side // 2, start_pos[1] - height_triangle)
                ]

                pygame.draw.polygon(screen, current_color, points, 3)

            # Ромб
            elif tool == "rhombus":
                center_x = (start_pos[0] + end_pos[0]) // 2
                center_y = (start_pos[1] + end_pos[1]) // 2

                width = abs(end_pos[0] - start_pos[0])
                height_rhombus = abs(end_pos[1] - start_pos[1])

                points = [
                    (center_x, center_y - height_rhombus // 2),
                    (center_x + width // 2, center_y),
                    (center_x, center_y + height_rhombus // 2),
                    (center_x - width // 2, center_y)
                ]

                pygame.draw.polygon(screen, current_color, points, 3)

    # Рисование кистью и ластиком во время движения мыши
    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if tool == "brush":
            pygame.draw.line(screen, current_color, start_pos, mouse_pos, 5)
            start_pos = mouse_pos

        elif tool == "eraser":
            pygame.draw.line(screen, white, start_pos, mouse_pos, 20)
            start_pos = mouse_pos

    # Верхняя панель с подсказками
    pygame.draw.rect(screen, white, (0, 0, w, 75))

    info = font.render(
        "B Brush | R Rect | C Circle | E Eraser | S Square | T Right Triangle | Q Equal Triangle | D Rhombus",
        True,
        black
    )

    info2 = font.render(
        "1 Black | 2 Red | 3 Green | 4 Blue | Space Clear",
        True,
        black
    )

    screen.blit(info, (15, 10))
    screen.blit(info2, (15, 40))

    pygame.display.update()
    clock.tick(60)

pygame.quit()