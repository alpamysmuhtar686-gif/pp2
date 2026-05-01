import pygame, random, sys, time
from ui import show_main_menu, show_game_over_screen, show_leaderboard, show_settings_screen
from persistence import load_settings, save_settings, apply_settings
pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
# Create EMPTY groups
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
events = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

FPS = 60
FramePerSec = pygame.time.Clock()

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Other Variables for use in the program
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
COIN_SPEED = 5
SUFFICIENT_COIN_INCREASE = 5
MAX_OBSTACLES = 3
MAX_EVENTS = 2

# Distance and race variables
TOTAL_DISTANCE = 1000  # Total distance to finish
distance_traveled = 0
player_name = ""

# Default settings
default_settings = {
    "sound_enabled": True,
    "car_color": "red",
    "difficulty": "normal"
}

# Game settings (loaded from file)
game_settings = default_settings.copy()


# background info
background = pygame.image.load("assets/AnimatedStreet.png")
background_music = pygame.mixer.Sound("assets/background.wav")

def safe_x(player_x, group=all_sprites):
    # Try up to 10 times, then return best available position
    # All entities spawn at y=0 and move down with static x
    candidates = []
    for _ in range(10):
        x = random.randint(40, SCREEN_WIDTH - 40)
        safe = True
        for sprite in group:
            # Only check sprites at spawn zone (top of screen)
            if sprite.rect.top < 50 and abs(sprite.rect.center[0] - x) < 80:
                safe = False
                break
        if safe:
            return x
        # Track closest valid position as fallback
        if candidates:
            min_dist = min(abs(c - player_x) for c in candidates)
            if abs(x - player_x) > min_dist:
                candidates.append(x)
        else:
            candidates.append(x)
    
    # Fallback: return position farthest from player
    if candidates:
        return max(candidates, key=lambda c: abs(c - player_x))
    return random.randint(40, SCREEN_WIDTH - 40)

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

def calculate_final_score():
    """Calculate final score: distance + coins * 10 + SCORE * 5 + power-up bonuses"""
    base_score = distance_traveled + (COIN_SCORE * 10) + (SCORE * 5)
    # Bonus for finishing
    if distance_traveled >= TOTAL_DISTANCE:
        base_score += 500
    return base_score

def get_username(DISPLAYSURF: pygame.Surface):
    """Display username entry screen"""
    input_text = ""
    entering = True
    
    while entering:
        DISPLAYSURF.fill(WHITE)
        
        title = font_small.render("Enter Your Name", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 150))
        DISPLAYSURF.blit(title, title_rect)
        
        # Show input box
        input_box = pygame.Rect(50, 250, 300, 50)
        pygame.draw.rect(DISPLAYSURF, BLACK, input_box, 2)
        
        name_surface = font_small.render(input_text if input_text else "Type here...", True, BLACK)
        name_rect = name_surface.get_rect(center=input_box.center)
        DISPLAYSURF.blit(name_surface, name_rect)
        
        instruction = font_small.render("Press ENTER to start", True, BLUE)
        instr_rect = instruction.get_rect(center=(SCREEN_WIDTH//2, 400))
        DISPLAYSURF.blit(instruction, instr_rect)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == pygame.K_RETURN:
                    if input_text.strip():
                        entering = False
                        return input_text.strip() or "Player"
                elif event.unicode.isalnum() or event.unicode in ['_', '-']:
                    if len(input_text) < 15:
                        input_text += event.unicode
        
class Enemy(pygame.sprite.Sprite):
      def __init__(self, player, group):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect = self.image.get_rect()

        self.player = player
        self.group = group

        self.rect.center = (safe_x(self.player.rect.center[0], self.group), 0)

      def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (safe_x(self.player.rect.center[0], self.group), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image_color = game_settings["car_color"]
        self.image = pygame.image.load(f"assets/player_{self.image_color}.png")
        if self.image_color != "blue":
            self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

        # NEW
        self.base_speed = 5
        self.current_speed = 5
        self.slow_timer = 0
        self.power = None
        self.power_timer = 0
        self.shield = False
        self.repair_used = False
        self.nitro_active = False
        self.nitro_timer = 0
        self.repair_available = False


    def move(self):
        pressed_keys = pygame.key.get_pressed()

        # recover speed over time
        if self.slow_timer > 0:
            self.slow_timer -= 1
        else:
            self.current_speed = self.base_speed

        if self.rect.left > 0:
            if pressed_keys[pygame.K_LEFT]:
                self.rect.move_ip(-self.current_speed, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[pygame.K_RIGHT]:
                self.rect.move_ip(self.current_speed, 0)

    def change_speed(self, factor=0.7, duration=60):
        self.current_speed = max(2, self.base_speed * factor)
        self.slow_timer = duration

    def update_power(self):
        # Handle nitro timer separately
        if self.nitro_active:
            self.nitro_timer -= 1
            if self.nitro_timer <= 0:
                self.nitro_active = False
        # Handle other powerups
        if self.power and self.power != "nitro":
            self.power_timer -= 1
            if self.power_timer <= 0:
                if self.power != "shield":   # shield must NOT expire
                    self.power = None
                  
class Coin(pygame.sprite.Sprite):
    def __init__(self, player, group):
        super().__init__()
        self.image = pygame.image.load("assets/coin.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.player = player
        self.group = group
        self.rect.center = (safe_x(self.player.rect.center[0], self.group), 0)
    def move(self):
        self.rect.move_ip(0, COIN_SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (safe_x(self.player.rect.center[0], self.group), 0)
    def earn_point(self):
        if (self.rect.bottom <= 600):
            global COIN_SCORE
            RANDOM_SCORE = random.randint(1, 3)
            COIN_SCORE += RANDOM_SCORE
            self.rect.top = 0
            self.rect.center = (safe_x(self.player.rect.center[0], self.group), 0)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type="oil"):
        super().__init__()
        
        self.type = type
        
        # Create surface instead of loading image
        self.image = pygame.Surface((60, 60))
        
        if type == "oil":
            self.image.fill((30, 30, 30))  # dark = oil
        elif type == "block":
            self.image.fill((139, 69, 19))  # brown = barrier
        
        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(P1.rect.center[0], obstacles), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (safe_x(P1.rect.center[0], obstacles), 0)

class RoadEvent(pygame.sprite.Sprite):
    def __init__(self, type="boost"):
        super().__init__()
        
        self.type = type
        self.image = pygame.Surface((80, 20))
        
        if type == "boost":
            self.image.fill(GREEN)
        elif type == "slow":
            self.image.fill(RED)
        
        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(P1.rect.center[0], events), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (safe_x(P1.rect.center[0], events), 0)


class PowerUp(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        self.type = type
        self.image = pygame.Surface((40, 40))

        if type == "nitro":
            self.image.fill((0, 200, 255))
        elif type == "shield":
            self.image.fill((255, 215, 0))
        elif type == "repair":
            self.image.fill((255, 100, 255))

        self.rect = self.image.get_rect()
        self.rect.center = (safe_x(P1.rect.center[0], powerups), 0)

        self.spawn_time = pygame.time.get_ticks()
    
    def move(self):
        self.rect.move_ip(0, SPEED)

        # disappear after 5 seconds if not collected
        if pygame.time.get_ticks() - self.spawn_time > 5000:
            self.kill()

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# 1. Create player FIRST
P1 = Player()



# 3. Now create objects using those groups
E1 = Enemy(P1, enemies)
COIN = Coin(P1, coins) 

# 4. Add them to groups
enemies.add(E1)
coins.add(COIN)
all_sprites.add(P1, E1, COIN)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)


SPAWN_EVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SPAWN_EVENT, 2000)  # every 2 seconds

# Repair powerup flag
repair_active = False


def clear_powerups(player):
    player.power = None
    player.shield = False
    player.nitro_active = False


# coin score position, need to be adjusted manually by pressing
# coin_score_coordinate = [40, 325]

# Load settings and apply them at startup
load_settings()
apply_settings()

# Main game loop - starts with main menu
def run_game(DISPLAYSURF: pygame.Surface):
    global SCORE, COIN_SCORE, distance_traveled, SPEED, COIN_SPEED, SUFFICIENT_COIN_INCREASE, game_settings
    game_settings = load_settings()
    apply_settings()
    player_name = get_username(DISPLAYSURF)
    # Reset game variables for new game
    SCORE = 0
    COIN_SCORE = 0
    distance_traveled = 0
    SPEED = 5
    COIN_SPEED = 5
    SUFFICIENT_COIN_INCREASE = 5
    # assign global variables for all variables that are used outside function within this function
    global repair_active, enemies, coins, obstacles, events, powerups, all_sprites, P1, background_music
    # Reapply difficulty settings
    apply_settings()
    
    # Recreate sprites
    enemies.empty()
    coins.empty()
    obstacles.empty()
    events.empty()
    powerups.empty()
    all_sprites.empty()
    
    P1 = Player()
    E1 = Enemy(P1, enemies)
    COIN = Coin(P1, coins)
    enemies.add(E1)
    coins.add(COIN)
    all_sprites.add(P1, E1, COIN)
    
    while True:
        if game_settings.get("sound_enabled", True) and not pygame.mixer.get_busy():
            background_music.play(-1)
        #Cycles through all events occuring  
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.1
                P1.base_speed += 0.1
                if COIN_SCORE >= SUFFICIENT_COIN_INCREASE: # every time as COIN is a multiple of 5 (N = 5), the speed increases
                    SPEED += 0.2
                    P1.base_speed += 0.2
                    SUFFICIENT_COIN_INCREASE = (SUFFICIENT_COIN_INCREASE // 5 + 1) * 5
            if event.type == SPAWN_EVENT:
                # Skip obstacle spawning if repair was just used
                if repair_active:
                    repair_active = False
                    pygame.time.set_timer(SPAWN_EVENT, random.randint(1500, 3000))
                    continue
                
                choice = random.choice(["obstacle", "event", "powerup"])

                if choice == "obstacle" and len(obstacles) < MAX_OBSTACLES:
                    new_obstacle = Obstacle(random.choice(["oil", "block"]))
                    obstacles.add(new_obstacle)
                    all_sprites.add(new_obstacle)

                elif choice == "event" and len(events) < MAX_EVENTS:
                    new_event = RoadEvent(random.choice(["boost", "slow"]))
                    events.add(new_event)
                    all_sprites.add(new_event)

                elif choice == "powerup":
                    pu = PowerUp(random.choice(["nitro", "shield", "repair"]))
                    powerups.add(pu)
                    all_sprites.add(pu)

                pygame.time.set_timer(SPAWN_EVENT, random.randint(1500, 3000))

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_a:
        #         coin_score_coordinate[0] -= 20               
        #     elif event.key == pygame.K_d:
        #         coin_score_coordinate[0] += 20
        #     elif event.key == pygame.K_w:
        #         coin_score_coordinate[1] -= 20
        #     elif event.key == pygame.K_s:
        #         coin_score_coordinate[1] += 20
        #     print(f"coin score coordinate: {coin_score_coordinate}")
        DISPLAYSURF.blit(background, (0,0))
        score_text = font_small.render(f"Scores: {SCORE}", True, BLACK)
        coin_scores = font_small.render(str(COIN_SCORE), True, BLACK)
        coin_text = font_small.render("Coins", True, BLACK)
        speed_info = font_small.render(f"Speed: {P1.current_speed:.2f}", True, BLACK)

        # Distance meter
        distance_text = font_small.render(f"Distance: {distance_traveled}/{TOTAL_DISTANCE}", True, BLACK)
        remaining = max(0, TOTAL_DISTANCE - distance_traveled)
        remaining_text = font_small.render(f"Remaining: {remaining}", True, BLACK)

        # coin_to_inc_speed = font_small.render(f"Coins to increase the speed: {SUFFICIENT_COIN_INCREASE}", True, BLACK)
        # DISPLAYSURF.blit(coin_to_inc_speed, (5, 65))
        DISPLAYSURF.blit(score_text, (5, 0))
        DISPLAYSURF.blit(coin_scores, (360, 25))
        DISPLAYSURF.blit(coin_text, (345, 0))
        DISPLAYSURF.blit(speed_info, (5, 45))
        DISPLAYSURF.blit(distance_text, (5, 110))
        DISPLAYSURF.blit(remaining_text, (5, 135))

        #Moves and Re-draws all Sprites
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # Update distance traveled (based on speed)
        distance_traveled += SPEED // 5
        if distance_traveled >= TOTAL_DISTANCE and not hasattr(P1, 'finished'):
            P1.finished = True
            # Bonus for finishing!

        # POWER-UP COLLISION HANDLING
        for pu in pygame.sprite.spritecollide(P1, powerups, True):
            clear_powerups(P1)
            P1.power = pu.type
            P1.power_timer = 300  # ~5 seconds

            if pu.type == "nitro":
                P1.nitro_active = True
                P1.nitro_timer = 180  # 3 seconds

            elif pu.type == "shield":
                P1.shield = True
                P1.power = "shield"
                P1.repair_available = False # fixing coexisting issue when picking a shield

            elif pu.type == "repair":
                P1.repair_available = True


        if SCORE >= 15 and len(enemies) < 2:
            E2 = Enemy(P1, enemies)
            enemies.add(E2)
            all_sprites.add(E2)
        if SCORE >= 30 and len(enemies) < 3:
            E3 = Enemy(P1, enemies)
            enemies.add(E3)
            all_sprites.add(E3)

        # Respawn killed enemies based on current difficulty
        target_enemies = 1
        if SCORE >= 15:
            target_enemies = 2
        if SCORE >= 30:
            target_enemies = 3

        # If we have fewer enemies than target (killed by shield), respawn
        while len(enemies) < target_enemies:
            new_enemy = Enemy(P1, enemies)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
        P1.update_power()

        # Update player speed based on all modifiers
        # Priority: nitro > slow > base
        if P1.nitro_active:
            P1.current_speed = P1.base_speed * 1.5
        elif P1.slow_timer > 0:
            pass  # keep current_speed set by change_speed
        else:
            P1.current_speed = P1.base_speed

        if P1.power or P1.nitro_active:
            if P1.nitro_active:
                power_name = "nitro"
                timer = P1.nitro_timer
                text = font_small.render(
                f"Power: {power_name} ({timer // 60}s)", 
                True, BLACK
                )
                DISPLAYSURF.blit(text, (5, 70))
            elif P1.power == "shield":
                power_name = "shield"
                text = font_small.render(
                f"Power: {power_name}", 
                True, BLACK
                )
                DISPLAYSURF.blit(text, (5, 70))
            if P1.repair_available:
                text = font_small.render("Repair Ready", True, BLACK)
                DISPLAYSURF.blit(text, (5, 90))
            else:
                power_name = P1.power
                timer = P1.power_timer
            
        # If player touched a coin, a point earns        
        if pygame.sprite.spritecollideany(P1, coins):
            COIN.earn_point()
            try:
                if game_settings["sound_enabled"]:
                    pygame.mixer.Sound('assets/coin_take.mp3').play()
                else: pass
            except FileNotFoundError:
                print("[Error]: File 'coin_take.mp3' isn't found. Didn't you delete it?")

        for obstacle in pygame.sprite.spritecollide(P1, obstacles, True):
            if obstacle.type == "oil":
                P1.change_speed(0.7, 60)
            elif obstacle.type == "block":
                P1.change_speed(0.5, 90)

        for event_obj in pygame.sprite.spritecollide(P1, events, True):
            if event_obj.type == "boost":
                P1.change_speed(1.3, 60)
            elif event_obj.type == "slow":
                P1.change_speed(0.7, 60)
            
        # To be run if collision occurs between Player and Enemy
        hit_enemies = pygame.sprite.spritecollide(P1, enemies, False)
        if hit_enemies:
            if P1.shield:
                for enemy in hit_enemies:
                    enemy.kill()
                P1.shield = False
                P1.power = None

            elif P1.repair_available:
                # USE REPAIR INSTEAD OF DYING
                P1.repair_available = False
                for enemy in hit_enemies:
                    enemy.kill()
                for obs in obstacles:
                    obs.kill()
                obstacles.empty()
            else:
                # stop playing sound
                # sound_isplaying = False
                # Play crash sound if sound is enabled
                if game_settings.get("sound_enabled", True):
                    try:
                        pygame.mixer.Sound('assets/crash.wav').play()
                    except:
                        pass
                time.sleep(0.5)
                
                # Calculate final score
                final_score = calculate_final_score()
                
                # Show game over screen with retry/main menu options
                result = show_game_over_screen(DISPLAYSURF, final_score, distance_traveled, COIN_SCORE)
                
                if result == "retry":
                    # Restart game - reset variables
                    SCORE = 0
                    COIN_SCORE = 0
                    distance_traveled = 0
                    apply_settings()
                    
                    # Recreate sprites
                    enemies.empty()
                    coins.empty()
                    obstacles.empty()
                    events.empty()
                    powerups.empty()
                    all_sprites.empty()
                    P1 = Player()
                    E1 = Enemy(P1, enemies)
                    COIN = Coin(P1, coins)
                    enemies.add(E1)
                    coins.add(COIN)
                    all_sprites.add(P1, E1, COIN)
                    continue  # Continue to next iteration of game loop
                else:
                    # Show leaderboard before returning to main menu
                    show_leaderboard(DISPLAYSURF, final_score, player_name, distance_traveled)
                    # Return to main menu
                    return  # Break out of inner game loop
    
        pygame.display.flip()
        pygame.time.Clock().tick(120)
    return (player_name, distance_traveled)