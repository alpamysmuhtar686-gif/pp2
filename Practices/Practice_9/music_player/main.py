import pygame
from player import MusicPlayer

pygame.init()

screen = pygame.display.set_mode((600, 300))
pygame.display.set_caption("Music Player")

font = pygame.font.Font(None, 36)

player = MusicPlayer("music")

running = True

clock = pygame.time.Clock()

while running:
    screen.fill((30, 30, 30))

    # Display current track
    track_name = player.get_current_track()
    text = font.render(f"Now Playing: {track_name}", True, (255, 255, 255))
    screen.blit(text, (50, 100))

    #  Instructions
    controls = font.render("P:Play S:Stop N:Next B:Back Q:Quit", True, (200, 200, 200))
    screen.blit(controls, (50, 200))
    
    # current time position
    position_total_sec = pygame.mixer.music.get_pos() / 1000  # total seconds
    position_sec = int(position_total_sec % 60) # seconds
    position_min = int(position_total_sec // 60) # minutes
    time_text = font.render(f"Time: {int(position_min)}m {int(position_sec)}s", True, (255,255,255))
    screen.blit(time_text, (50, 150))
    pygame.display.flip()

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

    clock.tick(30)

pygame.quit()