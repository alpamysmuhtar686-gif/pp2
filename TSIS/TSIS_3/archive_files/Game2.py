#Imports
import pygame, sys
from pygame.locals import *
import random, time
import math

#Initialzing 
pygame.init()

#Setting up FPS 
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

# Lane positions for hazards and events
LANE_POSITIONS = [60, 140, 220, 300]

# Difficulty scaling
DIFFICULTY_LEVEL = 1
MAX_TRAFFIC_CARS = 3
MAX_OBSTACLES = 4
SPAWN_INTERVAL_BASE = 2000  # 2 seconds (120 frames at 60 FPS)

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("AnimatedStreet.png")

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    """Traffic car that moves downwards"""
    def __init__(self, y_pos=None):
        super().__init__() 
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        # Safe spawn: don't spawn on top of player
        if y_pos is not None:
            self.rect.center = (random.choice(LANE_POSITIONS), y_pos)
        else:
            self.rect.center = (random.choice(LANE_POSITIONS), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if (self.rect.bottom > 600):
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.choice(LANE_POSITIONS), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)
       
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        # Scale horizontal movement with game speed
        horizontal_speed = 5 + (SPEED - BASE_SPEED) * 0.8  # Proportional to game speed
        
        if self.rect.left > 0:
              if pressed_keys[K_LEFT]:
                  self.rect.move_ip(-horizontal_speed, 0)
        if self.rect.right < SCREEN_WIDTH:        
              if pressed_keys[K_RIGHT]:
                  self.rect.move_ip(horizontal_speed, 0)
                  
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.image = pygame.transform.scale(self.image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def move(self):
        self.rect.move_ip(0, COIN_SPEED)
        if (self.rect.bottom > 600):
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    def earn_point(self):
        if (self.rect.bottom <= 600):
            global COIN_SCORE
            RANDOM_SCORE = random.randint(1, 3)
            COIN_SCORE += RANDOM_SCORE
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Hazard(pygame.sprite.Sprite):
    """Road obstacle - oil spill, barrier, or pothole"""
    def __init__(self, hazard_type=None, y_pos=None):
        super().__init__()
        # Random hazard type if not specified
        if hazard_type is None:
            hazard_type = random.choice(["oil", "barrier", "pothole"])
        
        self.hazard_type = hazard_type
        if hazard_type == "oil":
            self.image = pygame.Surface((60, 40))
            self.image.fill((30, 30, 30))
            pygame.draw.ellipse(self.image, (50, 50, 50), (0, 0, 60, 40))
            self.speed_modifier = 0.5
        elif hazard_type == "barrier":
            self.image = pygame.Surface((50, 30))
            self.image.fill((255, 100, 0))
            pygame.draw.rect(self.image, (200, 200, 200), (5, 5, 40, 20), border_radius=5)
            self.speed_modifier = 0.3
        else:  # pothole
            self.image = pygame.Surface((40, 40))
            self.image.fill((50, 40, 30))
            pygame.draw.circle(self.image, (30, 25, 20), (20, 20), 15)
            self.speed_modifier = 0.7
        
        self.rect = self.image.get_rect()
        # Safe spawn: don't spawn on top of player
        if y_pos is not None:
            self.rect.center = (random.choice(LANE_POSITIONS), y_pos)
        else:
            self.rect.center = (random.choice(LANE_POSITIONS), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.choice(LANE_POSITIONS), 0)


class NitroBoost(pygame.sprite.Sprite):
    """Nitro boost strip that increases player speed temporarily"""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 20))
        self.image.fill((0, 255, 255))  # Cyan boost strip
        # Add lightning bolt pattern
        pygame.draw.polygon(self.image, (255, 255, 0), [(10, 0), (30, 10), (20, 10), (40, 20), (30, 10), (40, 0)])
        self.rect = self.image.get_rect()
        self.rect.center = (random.choice(LANE_POSITIONS), 0)
        self.active = True

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            self.rect.top = 0
            self.rect.center = (random.choice(LANE_POSITIONS), 0)



#Setting up Sprites        
P1 = Player()
E1 = Enemy()
COIN = Coin()

# Create initial traffic cars (dynamic)
traffic_cars = pygame.sprite.Group()
traffic_cars.add(E1)

# Create hazards (road obstacles) - reduced count
obstacles = pygame.sprite.Group()
for _ in range(1):
    hazard_type = random.choice(["oil", "barrier", "pothole"])
    h = Hazard(hazard_type)
    obstacles.add(h)

# Create nitro boost strips - reduced count
nitro_boosts = pygame.sprite.Group()
nitro = NitroBoost()
nitro_boosts.add(nitro)

#Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(COIN)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(COIN)
all_sprites.add(*obstacles)
all_sprites.add(*nitro_boosts)
all_sprites.add(*traffic_cars)

#Adding a new User event 
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Dynamic traffic and obstacle spawning
SPAWN_TRAFFIC = pygame.USEREVENT + 2
SPAWN_ITEM = pygame.USEREVENT + 3  # Unified spawner for hazard/nitro/coin
pygame.time.set_timer(SPAWN_TRAFFIC, SPAWN_INTERVAL_BASE)
pygame.time.set_timer(SPAWN_ITEM, SPAWN_INTERVAL_BASE)

# Nitro boost effect tracking
nitro_active = False
nitro_timer = 0
BASE_SPEED = 5


# coin score position, need to be adjusted manually by pressing
# coin_score_coordinate = [40, 325]
#Game Loop
while True:
      
    #Cycles through all events occuring  
    for event in pygame.event.get():
        if event.type == INC_SPEED:
              SPEED += 0.1  # Reduced rate of change (ds)
              if COIN_SCORE >= SUFFICIENT_COIN_INCREASE:
                  SPEED += 0.2  # Smaller boost on coin collection
                  SUFFICIENT_COIN_INCREASE = (SUFFICIENT_COIN_INCREASE // 5 + 1) * 5
              # Difficulty scaling: increase traffic density
              DIFFICULTY_LEVEL = min(SCORE // 5 + 1, 10)
        
        # Dynamic traffic spawning
        if event.type == SPAWN_TRAFFIC:
            if len(traffic_cars) < min(1 + DIFFICULTY_LEVEL, MAX_TRAFFIC_CARS):
                # Safe spawn: spawn above screen, not on player
                new_car = Enemy(y_pos=-50)
                # Check for overlap with existing traffic
                if not pygame.sprite.spritecollideany(new_car, traffic_cars):
                    traffic_cars.add(new_car)
                    all_sprites.add(new_car)
        
        # Unified item spawning: hazard, nitro, or coin (only one at a time)
        if event.type == SPAWN_ITEM:
            # Randomly choose what to spawn
            item_choice = random.choice(['hazard', 'nitro', 'coin'])
            
            if item_choice == 'hazard' and len(obstacles) < 2:
                new_obstacle = Hazard(y_pos=-50)
                if not pygame.sprite.spritecollideany(new_obstacle, obstacles):
                    obstacles.add(new_obstacle)
                    all_sprites.add(new_obstacle)
            elif item_choice == 'nitro' and len(nitro_boosts) < 1:
                new_nitro = NitroBoost()
                new_nitro.rect.top = -50
                if not pygame.sprite.spritecollideany(new_nitro, nitro_boosts):
                    nitro_boosts.add(new_nitro)
                    all_sprites.add(new_nitro)
            elif item_choice == 'coin' and len(coins) < 1:
                new_coin = Coin()
                new_coin.rect.top = -50
                if not pygame.sprite.spritecollideany(new_coin, coins):
                    coins.add(new_coin)
                    all_sprites.add(new_coin)
        
        if event.type == QUIT:
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
    scores = font_small.render(str(SCORE), True, BLACK)
    score_text = font_small.render("Scores", True, BLACK)
    coin_scores = font_small.render(str(COIN_SCORE), True, BLACK)
    coin_text = font_small.render("Coins", True, BLACK)
    # speed_info will be set below based on hazard/nitro status
    speed_info = font_small.render(f"Speed: {SPEED:.2f}", True, BLACK)
    # coin_to_inc_speed = font_small.render(f"Coins to increase the speed: {SUFFICIENT_COIN_INCREASE}", True, BLACK)
    # DISPLAYSURF.blit(coin_to_inc_speed, (5, 65))
    DISPLAYSURF.blit(scores, (10,25))
    DISPLAYSURF.blit(score_text, (5, 0))
    DISPLAYSURF.blit(coin_scores, (360, 25))
    DISPLAYSURF.blit(coin_text, (345, 0))
    DISPLAYSURF.blit(speed_info, (5, 45))

    # Update nitro timer
    if nitro_active:
        nitro_timer -= 1
        if nitro_timer <= 0:
            nitro_active = False
    #Moves and Re-draws all Sprites
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # If player touched a coin, a point earns        
    if pygame.sprite.spritecollideany(P1, coins):
        COIN.earn_point()
        try:
            pygame.mixer.Sound('coin_take.mp3').play()
        except FileNotFoundError:
            print("[Error]: File 'coin_take.mp3' isn't found. Didn't you delete it?")

    # Handle nitro boost collection
    if pygame.sprite.spritecollideany(P1, nitro_boosts):
        nitro_active = True
        nitro_timer = 120  # 2 seconds at 60 FPS
        try:
            pygame.mixer.Sound('coin_take.mp3').play()
        except:
            pass

    # Handle hazard collision - slow down player
    hazard_hit = pygame.sprite.spritecollideany(P1, obstacles)
    if hazard_hit:
        # Orange when hitting hazard
        speed_info = font_small.render(f"Speed: {int(SPEED)}", True, (255, 165, 0))
    elif nitro_active:
        # Blue when nitro is active
        speed_info = font_small.render(f"Speed: {int(SPEED)}", True, BLUE)
    else:
        # Black by default
        speed_info = font_small.render(f"Speed: {int(SPEED)}", True, BLACK)

    DISPLAYSURF.blit(speed_info, (5, 45))

    # To be run if collision occurs between Player and Enemy (traffic)
    # if pygame.sprite.spritecollideany(P1, traffic_cars) or pygame.sprite.spritecollideany(P1, enemies):
    #     pygame.mixer.Sound('crash.wav').play()
    #     time.sleep(0.5)
                   
    #     final_score_text = font.render(f"Scores: {SCORE}", True, BLACK)
    #     final_coin_score = font.render(f"Coins: {COIN_SCORE}", True, BLACK)
    #     DISPLAYSURF.fill(RED)
    #     DISPLAYSURF.blit(game_over, (30,200))
    #     DISPLAYSURF.blit(final_score_text, (60, 285))
    #     DISPLAYSURF.blit(final_coin_score, (60, 365))
    #     pygame.display.update()
    #     for entity in all_sprites:
    #         entity.kill() 
    #     time.sleep(2)
    #     pygame.quit()
    #     sys.exit()        
        
        
    pygame.display.update()
    FramePerSec.tick(FPS)