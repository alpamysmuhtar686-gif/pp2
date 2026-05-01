import pygame
from persistence import load_scores

def draw_button(ecran, font_small, text, x, y, w, h):
    pygame.draw.rect(ecran, (200, 200, 200), (x, y, w, h))
    pygame.draw.rect(ecran, (0, 0, 0), (x, y, w, h), 3)

    button_text = font_small.render(text, True, (0, 0, 0))
    ecran.blit(button_text, (x + 30, y + 15))

def main_menu(ecran, font, font_small):
    ecran.fill((255, 255, 255))

    title = font.render("RACER", True, (0, 0, 0))
    ecran.blit(title, (150, 120))

    draw_button(ecran, font_small, "PLAY", 200, 250, 200, 60)
    draw_button(ecran, font_small, "LEADERBOARD", 200, 330, 200, 60)
    draw_button(ecran, font_small, "SETTINGS", 200, 410, 200, 60)
    draw_button(ecran, font_small, "QUIT", 200, 490, 200, 60)

def name_screen(ecran, font_small, player_name):
    ecran.fill((255, 255, 255))

    title = font_small.render("ENTER YOUR NAME:", True, (0, 0, 0))
    ecran.blit(title, (190, 200))

    pygame.draw.rect(ecran, (240, 240, 240), (150, 270, 300, 50))
    pygame.draw.rect(ecran, (0, 0, 0), (150, 270, 300, 50), 3)

    name_text = font_small.render(player_name, True, (0, 0, 0))
    ecran.blit(name_text, (165, 285))

    draw_button(ecran, font_small, "START", 200, 380, 200, 60)

def leaderboard_screen(ecran, font_small):
    ecran.fill((255, 255, 255))

    title = font_small.render("LEADERBOARD", True, (0, 0, 0))
    ecran.blit(title, (220, 80))

    scores = load_scores()

    y = 150

    if len(scores) == 0:
        text = font_small.render("No scores yet", True, (0, 0, 0))
        ecran.blit(text, (220, 200))
    else:
        for i, item in enumerate(scores):
            line = font_small.render(
                f"{i + 1}. {item['name']} | Score: {item['score']} | Coins: {item['coins']}",
                True,
                (0, 0, 0)
            )
            ecran.blit(line, (70, y))
            y += 35

    draw_button(ecran, font_small, "BACK", 200, 650, 200, 60)

def settings_screen(ecran, font_small, sound, car_color, difficulty):
    ecran.fill((255, 255, 255))

    title = font_small.render("SETTINGS", True, (0, 0, 0))
    ecran.blit(title, (240, 100))

    text1 = font_small.render(f"Sound: {sound}", True, (0, 0, 0))
    ecran.blit(text1, (220, 180))

    text2 = font_small.render(f"Car Color: {car_color}", True, (0, 0, 0))
    ecran.blit(text2, (200, 270))

    text3 = font_small.render(f"Difficulty: {difficulty}", True, (0, 0, 0))
    ecran.blit(text3, (190, 360))

    draw_button(ecran, font_small, "CHANGE SOUND", 180, 210, 240, 50)
    draw_button(ecran, font_small, "CHANGE CAR", 180, 300, 240, 50)
    draw_button(ecran, font_small, "CHANGE LEVEL", 180, 390, 240, 50)
    draw_button(ecran, font_small, "BACK", 200, 650, 200, 60)

def game_over_screen(ecran, font, font_small, score, point):
    ecran.fill((255, 0, 0))

    title = font.render("GAME OVER", True, (0, 0, 0))
    ecran.blit(title, (60, 180))

    result = font_small.render(f"Score: {score} | Coins: {point}", True, (0, 0, 0))
    ecran.blit(result, (170, 300))

    draw_button(ecran, font_small, "RETRY", 200, 420, 200, 60)
    draw_button(ecran, font_small, "MAIN MENU", 200, 510, 200, 60)