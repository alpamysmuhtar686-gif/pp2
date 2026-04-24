import pygame
from player import MusicPlayer


pygame.init()

WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

font = pygame.font.SysFont(None, 32)
small_font = pygame.font.SysFont(None, 24)

player = MusicPlayer("music")

running = True
clock = pygame.time.Clock()


def draw_text(text, x, y, font_obj):
    rendered_text = font_obj.render(text, True, (255, 255, 255))
    screen.blit(rendered_text, (x, y))


while running:
    screen.fill((30, 30, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next_track()
            elif event.key == pygame.K_b:
                player.previous_track()
            elif event.key == pygame.K_q:
                running = False

    current_track = player.get_current_track()
    position = player.get_position()

    draw_text("Music Player", 210, 30, font)
    draw_text(f"Current track: {current_track}", 50, 90, small_font)
    draw_text(f"Position: {position} sec", 50, 130, small_font)

    draw_text("Controls:", 50, 180, small_font)
    draw_text("P - Play | S - Stop | N - Next | B - Back | Q - Quit", 50, 215, small_font)

    pygame.display.update()
    clock.tick(60)

pygame.quit()