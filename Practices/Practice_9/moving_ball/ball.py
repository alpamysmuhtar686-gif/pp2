import pygame

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Ball")

width = 600
height = 600

x = 300
y = 300
radius = 25
step = 20

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and y - step - radius >= 0:
                y -= step
            if event.key == pygame.K_DOWN and y + step + radius <= height:
                y += step
            if event.key == pygame.K_LEFT and x - step - radius >= 0:
                x -= step
            if event.key == pygame.K_RIGHT and x + step + radius <= width:
                x += step

    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pygame.display.update()
    clock.tick(999)

pygame.quit()