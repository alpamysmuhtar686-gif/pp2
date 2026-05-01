import pygame
import random

from ui import main_menu, name_screen, leaderboard_screen, settings_screen, game_over_screen
from persistence import save_score, load_settings, save_settings

def run_game():
    pygame.init()
    pygame.mixer.init()

    height = 800
    width = 600
    lanes = [70, 210, 410]

    ecran = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Racer")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Verdana", 80)
    font_small = pygame.font.SysFont("Verdana", 20)

    settings = load_settings()
    sound = settings["sound"]
    car_color = settings["car_color"]
    difficulty = settings["difficulty"]

    pygame.mixer.music.load("assets/sounds/music.wav")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    if not sound:
        pygame.mixer.music.pause()

    def load_img(path, size):
        img = pygame.image.load(path)
        return pygame.transform.scale(img, size)

    fon = load_img("assets/images/AnimatedStreet.png", (width, height))
    player_blue = load_img("assets/images/Player.png", (50, 100))
    player_red = load_img("assets/images/red.png", (50, 100))
    player_green = load_img("assets/images/green.png", (50, 100))
    enemy = load_img("assets/images/Enemy.png", (50, 100))
    enemy2 = load_img("assets/images/Enemy.png", (50, 100))
    enemy3 = load_img("assets/images/Enemy.png", (50, 100))
    coin = load_img("assets/images/Coin.png", (60, 60))
    obstacles = load_img("assets/images/obstacles.png", (80, 80))
    oil = load_img("assets/images/oil.png", (100, 100))
    zone = load_img("assets/images/zone.png", (170, 50))
    zone2 = load_img("assets/images/zone2.png", (170, 50))
    shield = load_img("assets/images/shield.png", (60, 60))
    repair = load_img("assets/images/repair.png", (60, 60))

    screen = "menu"
    player_name = ""
    a = True
    saved_score = False

    def reset_game():
        nonlocal player_x, player_y, player_speed
        nonlocal enemy_x, enemy_y, enemy2_x, enemy2_y, enemy3_x, enemy3_y
        nonlocal coin_x, coin_y, obstacles_x, obstacles_y, oil_x, oil_y
        nonlocal zone_x, zone_y, zone2_x, zone2_y
        nonlocal shield_x, shield_y, repair_x, repair_y
        nonlocal score, point, move, point_coin
        nonlocal slow, slow_timer, fast, fast_timer
        nonlocal slip, slip_timer, shield_active, repair_count
        nonlocal saved_score

        player_x = 200
        player_y = 650
        player_speed = 3

        enemy_x = random.choice(lanes)
        enemy_y = -100
        enemy2_x = random.choice(lanes)
        enemy2_y = -400
        enemy3_x = random.choice(lanes)
        enemy3_y = -700

        coin_x = random.choice(lanes)
        coin_y = -60

        obstacles_x = random.choice(lanes)
        obstacles_y = -250

        oil_x = random.choice(lanes)
        oil_y = -500

        zone_x = random.choice(lanes)
        zone_y = random.randint(-500, -100)

        zone2_x = random.choice(lanes)
        zone2_y = random.randint(-600, -100)

        shield_x = random.choice(lanes)
        shield_y = random.randint(-700, -200)

        repair_x = random.choice(lanes)
        repair_y = random.randint(-900, -300)

        score = 0
        point = 0
        move = 1
        point_coin = 15

        slow = False
        slow_timer = 0

        fast = False
        fast_timer = 0

        slip = False
        slip_timer = 0

        shield_active = False
        repair_count = 0

        saved_score = False

    player_x = 200
    player_y = 650
    player_speed = 3

    enemy_x = enemy_y = enemy2_x = enemy2_y = enemy3_x = enemy3_y = 0
    coin_x = coin_y = 0
    obstacles_x = obstacles_y = 0
    oil_x = oil_y = 0
    zone_x = zone_y = 0
    zone2_x = zone2_y = 0
    shield_x = shield_y = 0
    repair_x = repair_y = 0

    score = 0
    point = 0
    move = 1
    point_coin = 15

    slow = False
    slow_timer = 0
    fast = False
    fast_timer = 0
    slip = False
    slip_timer = 0

    shield_active = False
    repair_count = 0

    reset_game()

    while a:
        if screen == "menu":
            main_menu(ecran, font, font_small)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if 200 <= mx <= 400 and 250 <= my <= 310:
                        reset_game()
                        player_name = ""
                        screen = "name"

                    elif 200 <= mx <= 400 and 330 <= my <= 390:
                        screen = "leaderboard"

                    elif 200 <= mx <= 400 and 410 <= my <= 470:
                        screen = "settings"

                    elif 200 <= mx <= 400 and 490 <= my <= 550:
                        a = False

            pygame.display.update()
            clock.tick(60)
            continue

        if screen == "name":
            name_screen(ecran, font_small, player_name)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if player_name == "":
                            player_name = "Player"
                        screen = "game"
                    else:
                        if len(player_name) < 12:
                            player_name += event.unicode

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if 200 <= mx <= 400 and 380 <= my <= 440:
                        if player_name == "":
                            player_name = "Player"
                        screen = "game"

            pygame.display.update()
            clock.tick(60)
            continue

        if screen == "leaderboard":
            leaderboard_screen(ecran, font_small)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if 200 <= mx <= 400 and 650 <= my <= 710:
                        screen = "menu"

            pygame.display.update()
            clock.tick(60)
            continue

        if screen == "settings":
            settings_screen(ecran, font_small, sound, car_color, difficulty)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if 180 <= mx <= 420 and 210 <= my <= 260:
                        sound = not sound

                        if sound:
                            pygame.mixer.music.unpause()
                        else:
                             pygame.mixer.music.pause()

                        if sound:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()

                    elif 180 <= mx <= 420 and 300 <= my <= 350:
                        if car_color == "Blue":
                            car_color = "Red"
                        elif car_color == "Red":
                            car_color = "Green"
                        else:
                            car_color = "Blue"

                    elif 180 <= mx <= 420 and 390 <= my <= 440:
                        if difficulty == "Easy":
                            difficulty = "Normal"
                        elif difficulty == "Normal":
                            difficulty = "Hard"
                        else:
                            difficulty = "Easy"

                    elif 200 <= mx <= 400 and 650 <= my <= 710:
                        settings = {
                            "sound": sound,
                            "car_color": car_color,
                            "difficulty": difficulty
                        }
                        save_settings(settings)
                        screen = "menu"

            pygame.display.update()
            clock.tick(60)
            continue

        if screen == "game_over":
            game_over_screen(ecran, font, font_small, score, point)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    a = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = event.pos

                    if 200 <= mx <= 400 and 420 <= my <= 480:
                        reset_game()
                        screen = "game"

                    elif 200 <= mx <= 400 and 510 <= my <= 570:
                        screen = "menu"

            pygame.display.update()
            clock.tick(60)
            continue

        enemy_speed = 2 + move

        if difficulty == "Easy":
            enemy_speed = 2 + move
        elif difficulty == "Normal":
            enemy_speed = 3 + move
        elif difficulty == "Hard":
            enemy_speed = 4 + move

        enemy_y += enemy_speed
        enemy2_y += enemy_speed
        enemy3_y += enemy_speed
        coin_y += 2
        obstacles_y += 2
        oil_y += 2
        zone_y += 2
        zone2_y += 2
        shield_y += 2
        repair_y += 2

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                a = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] and player_x < width - 50:
            player_x += player_speed

        if slip:
            player_x += random.randint(-10, 10)
            slip_timer -= 1

            if slip_timer <= 0:
                slip = False

        if slow:
            player_speed = 1
            slow_timer -= 1

            if slow_timer <= 0:
                slow = False
                player_speed = 3

        if fast:
            player_speed = 8
            fast_timer -= 1

            if fast_timer <= 0:
                fast = False
                player_speed = 3

        if player_x < 0:
            player_x = 0

        if player_x > width - 50:
            player_x = width - 50

        if enemy_y > height:
            score += 1
            enemy_y = -100
            enemy_x = random.choice(lanes)

        if enemy2_y > height:
            score += 1
            enemy2_y = -400
            enemy2_x = random.choice(lanes)

        if enemy3_y > height:
            score += 1
            enemy3_y = -700
            enemy3_x = random.choice(lanes)

        if coin_y > height:
            coin_y = -60
            coin_x = random.choice(lanes)

        if obstacles_y > height:
            obstacles_y = -250
            obstacles_x = random.choice(lanes)

        if oil_y > height:
            oil_y = -500
            oil_x = random.choice(lanes)

        if zone_y > height:
            zone_y = random.randint(-500, -100)
            zone_x = random.choice(lanes)

        if zone2_y > height:
            zone2_y = random.randint(-600, -100)
            zone2_x = random.choice(lanes)

        if shield_y > height:
            shield_y = random.randint(-700, -200)
            shield_x = random.choice(lanes)

        if repair_y > height:
            repair_y = random.randint(-900, -300)
            repair_x = random.choice(lanes)

        if car_color == "Red":
            player = player_red
        elif car_color == "Green":
         player = player_green
        else:
            player = player_blue
        player_rect = player.get_rect(topleft=(player_x, player_y))
        enemy_rect = enemy.get_rect(topleft=(enemy_x, enemy_y))
        enemy2_rect = enemy2.get_rect(topleft=(enemy2_x, enemy2_y))
        enemy3_rect = enemy3.get_rect(topleft=(enemy3_x, enemy3_y))
        coin_rect = coin.get_rect(topleft=(coin_x, coin_y))
        obstacles_rect = obstacles.get_rect(topleft=(obstacles_x, obstacles_y))
        oil_rect = oil.get_rect(topleft=(oil_x, oil_y))
        zone_rect = zone.get_rect(topleft=(zone_x, zone_y))
        zone2_rect = zone2.get_rect(topleft=(zone2_x, zone2_y))
        shield_rect = shield.get_rect(topleft=(shield_x, shield_y))
        repair_rect = repair.get_rect(topleft=(repair_x, repair_y))

        def game_over():
            nonlocal screen, saved_score

            if not saved_score:
                save_score(player_name, score, point)
                saved_score = True

            screen = "game_over"

        def check_enemy_collision(enemy_y_value, enemy_x_value, reset_y):
            nonlocal shield_active, repair_count

            if shield_active:
                shield_active = False
                return random.choice(lanes), reset_y

            if repair_count > 0:
                repair_count -= 1
                return random.choice(lanes), reset_y

            game_over()
            return enemy_x_value, enemy_y_value

        if player_rect.colliderect(enemy_rect):
            enemy_x, enemy_y = check_enemy_collision(enemy_y, enemy_x, -100)

        if player_rect.colliderect(enemy2_rect):
            enemy2_x, enemy2_y = check_enemy_collision(enemy2_y, enemy2_x, -400)

        if player_rect.colliderect(enemy3_rect):
            enemy3_x, enemy3_y = check_enemy_collision(enemy3_y, enemy3_x, -700)

        if player_rect.colliderect(obstacles_rect):
            if shield_active:
                shield_active = False
                obstacles_y = -250
                obstacles_x = random.choice(lanes)
            elif repair_count > 0:
                repair_count -= 1
                obstacles_y = -250
                obstacles_x = random.choice(lanes)
            else:
                game_over()

        if player_rect.colliderect(oil_rect):
            if repair_count > 0:
                repair_count -= 1
            else:
                slip = True
                slip_timer = 120

            oil_y = -500
            oil_x = random.choice(lanes)

        if player_rect.colliderect(zone_rect):
            slow = True
            slow_timer = 200
            zone_y = random.randint(-500, -100)
            zone_x = random.choice(lanes)

        if player_rect.colliderect(zone2_rect):
            fast = True
            fast_timer = 200
            zone2_y = random.randint(-600, -100)
            zone2_x = random.choice(lanes)

        if player_rect.colliderect(shield_rect):
            shield_active = True
            shield_y = random.randint(-700, -200)
            shield_x = random.choice(lanes)

        if player_rect.colliderect(repair_rect):
            repair_count += 1
            repair_y = random.randint(-900, -300)
            repair_x = random.choice(lanes)

        if player_rect.colliderect(coin_rect):
            point += random.randint(1, 6)
            coin_y = -60
            coin_x = random.choice(lanes)

        if point >= point_coin:
            move += 1
            point_coin += 15

        ecran.blit(fon, (0, 0))

        pygame.draw.line(ecran, (255, 255, 255), (200, 0), (200, height), 5)
        pygame.draw.line(ecran, (255, 255, 255), (400, 0), (400, height), 5)

        ecran.blit(zone, (zone_x, zone_y))
        ecran.blit(zone2, (zone2_x, zone2_y))
        ecran.blit(player, (player_x, player_y))
        ecran.blit(enemy, (enemy_x, enemy_y))
        ecran.blit(enemy2, (enemy2_x, enemy2_y))
        ecran.blit(enemy3, (enemy3_x, enemy3_y))
        ecran.blit(coin, (coin_x, coin_y))
        ecran.blit(obstacles, (obstacles_x, obstacles_y))
        ecran.blit(oil, (oil_x, oil_y))
        ecran.blit(shield, (shield_x, shield_y))
        ecran.blit(repair, (repair_x, repair_y))

        text = font_small.render(f"SCORE: {score}", True, (0, 0, 0))
        text2 = font_small.render(f"COINS: {point}", True, (0, 0, 0))
        text3 = font_small.render(f"SHIELD: {shield_active}", True, (0, 0, 0))
        text4 = font_small.render(f"REPAIR: {repair_count}", True, (0, 0, 0))
        name_text = font_small.render(f"PLAYER: {player_name}", True, (0, 0, 0))

        if fast:
            power_text = font_small.render(f"NITRO TIME: {fast_timer}", True, (0, 0, 0))
        elif slow:
            power_text = font_small.render(f"SLOW TIME: {slow_timer}", True, (0, 0, 0))
        elif slip:
            power_text = font_small.render(f"OIL EFFECT: {slip_timer}", True, (0, 0, 0))
        else:
            power_text = font_small.render("POWER: NONE", True, (0, 0, 0))

        ecran.blit(text, (7, 5))
        ecran.blit(text2, (450, 5))
        ecran.blit(text3, (7, 30))
        ecran.blit(text4, (450, 30))
        ecran.blit(name_text, (7, 55))
        ecran.blit(power_text, (7, 80))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()