import pygame

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("Paint")

clock = pygame.time.Clock()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 180, 0)
blue = (0, 100, 255)

screen.fill(white)

font = pygame.font.SysFont("Arial", 20)

current_color = black
tool = "brush"
drawing = False
start_pos = None

run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_r:
                tool = "rectangle"
            elif event.key == pygame.K_c:
                tool = "circle"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_1:
                current_color = black
            elif event.key == pygame.K_2:
                current_color = red
            elif event.key == pygame.K_3:
                current_color = green
            elif event.key == pygame.K_4:
                current_color = blue
            elif event.key == pygame.K_SPACE:
                screen.fill(white)

        if event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            start_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            if tool == "rectangle":
                x = min(start_pos[0], end_pos[0])
                y = min(start_pos[1], end_pos[1])
                width = abs(start_pos[0] - end_pos[0])
                height = abs(start_pos[1] - end_pos[1])
                pygame.draw.rect(screen, current_color, (x, y, width, height), 3)

            elif tool == "circle":
                radius = int(
                    ((end_pos[0] - start_pos[0]) ** 2 +
                     (end_pos[1] - start_pos[1]) ** 2) ** 0.5
                )
                pygame.draw.circle(screen, current_color, start_pos, radius, 3)

    if drawing:
        mouse_pos = pygame.mouse.get_pos()

        if tool == "brush":
            pygame.draw.line(screen, current_color, start_pos, mouse_pos, 5)
            start_pos = mouse_pos

        elif tool == "eraser":
            pygame.draw.line(screen, white, start_pos, mouse_pos, 20)
            start_pos = mouse_pos

    pygame.draw.rect(screen, white, (0, 0, w, 50))
    info = font.render(
        "B: Brush | R: Rectangle | C: Circle | E: Eraser | 1: Black 2: Red 3: Green 4: Blue | Space: Clear",
        True,
        black
    )
    screen.blit(info, (15, 15))

    pygame.display.update()
    clock.tick(60)

pygame.quit()