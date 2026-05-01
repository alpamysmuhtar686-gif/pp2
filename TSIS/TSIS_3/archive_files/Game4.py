import pygame, sys, random, time, json, os
from pygame.locals import *

pygame.init()

# ================= BASIC =================
FPS = 60
FramePerSec = pygame.time.Clock()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

# ================= COLORS =================
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)

# ================= FONTS =================
font = pygame.font.SysFont("Verdana", 50)
font_small = pygame.font.SysFont("Verdana", 20)

# ================= FILES =================
SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

# ================= SETTINGS =================
default_settings = {
    "sound_enabled": True,
    "car_color": "red",
    "difficulty": "normal"
}
game_settings = default_settings.copy()

CAR_COLORS = {
    "red": (255,0,0),
    "blue": (0,0,255),
    "green": (0,255,0),
    "yellow": (255,255,0)
}

def load_settings():
    global game_settings
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r') as f:
            game_settings = {**default_settings, **json.load(f)}

def save_settings():
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(game_settings, f)

# ================= LEADERBOARD =================
def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        return json.load(open(LEADERBOARD_FILE))
    return []

def save_leaderboard(lb):
    json.dump(lb, open(LEADERBOARD_FILE,"w"), indent=2)

# ================= UI =================
def button(text, x,y,w,h, mouse):
    hover = x<mouse[0]<x+w and y<mouse[1]<y+h
    pygame.draw.rect(DISPLAYSURF, YELLOW if hover else GREEN, (x,y,w,h))
    pygame.draw.rect(DISPLAYSURF, BLACK, (x,y,w,h),2)
    txt = font_small.render(text, True, BLACK)
    DISPLAYSURF.blit(txt, txt.get_rect(center=(x+w//2,y+h//2)))
    return hover

# ================= PLAYER =================
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        color = CAR_COLORS[game_settings["car_color"]]
        self.image.fill(color, special_flags=pygame.BLEND_MULT)
        self.rect = self.image.get_rect(center=(200,500))

        self.speed = 5
        self.repair = False

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left>0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right<SCREEN_WIDTH:
            self.rect.x += self.speed

# ================= ENEMY =================
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect(center=(random.randint(40,360),0))

    def move(self):
        self.rect.y += SPEED
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.x = random.randint(40,360)

# ================= COIN =================
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("coin.png")
        self.rect = self.image.get_rect(center=(random.randint(40,360),0))

    def move(self):
        self.rect.y += SPEED
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.x = random.randint(40,360)

# ================= GAME =================
def run_game(player_name):
    global SPEED

    SPEED = 5
    score = 0
    coins_collected = 0

    P1 = Player()
    E1 = Enemy()
    C1 = Coin()

    enemies = pygame.sprite.Group(E1)
    coins = pygame.sprite.Group(C1)
    all_sprites = pygame.sprite.Group(P1,E1,C1)

    background = pygame.image.load("AnimatedStreet.png")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return "quit"

        DISPLAYSURF.blit(background,(0,0))

        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # coin collision
        if pygame.sprite.spritecollideany(P1, coins):
            coins_collected += 1
            C1.rect.top = 0

        # enemy collision
        if pygame.sprite.spritecollideany(P1, enemies):
            if P1.repair:
                P1.repair = False
                for e in enemies:
                    e.kill()
            else:
                final_score = score + coins_collected*10
                return show_game_over(player_name, final_score)

        score += 1

        txt = font_small.render(f"Score: {score}",True,BLACK)
        DISPLAYSURF.blit(txt,(5,5))

        pygame.display.update()
        FramePerSec.tick(FPS)

# ================= GAME OVER =================
def show_game_over(name, score):
    lb = load_leaderboard()
    lb.append({"name":name,"score":score})
    lb.sort(key=lambda x:x["score"], reverse=True)
    lb = lb[:10]
    save_leaderboard(lb)

    while True:
        DISPLAYSURF.fill(RED)
        txt = font.render("Game Over",True,WHITE)
        DISPLAYSURF.blit(txt,(60,100))

        s = font_small.render(f"Score: {score}",True,WHITE)
        DISPLAYSURF.blit(s,(120,200))

        mouse = pygame.mouse.get_pos()

        if button("Retry",50,400,120,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "play"

        if button("Menu",220,400,120,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "menu"

        pygame.display.update()

# ================= SETTINGS =================
def settings_screen():
    while True:
        DISPLAYSURF.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        if button("Sound",100,150,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                game_settings["sound_enabled"] = not game_settings["sound_enabled"]

        if button("Color",100,250,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                game_settings["car_color"] = random.choice(list(CAR_COLORS.keys()))

        if button("Back",100,400,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                save_settings()
                return "menu"

        pygame.display.update()

# ================= LEADERBOARD =================
def leaderboard_screen():
    lb = load_leaderboard()

    while True:
        DISPLAYSURF.fill(BLACK)
        y = 100
        for i,e in enumerate(lb):
            txt = font_small.render(f"{i+1}. {e['name']} {e['score']}",True,WHITE)
            DISPLAYSURF.blit(txt,(50,y))
            y+=30

        mouse = pygame.mouse.get_pos()
        if button("Back",100,500,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "menu"

        pygame.display.update()

# ================= MENU =================
def menu():
    while True:
        DISPLAYSURF.fill(WHITE)
        mouse = pygame.mouse.get_pos()

        if button("Play",100,150,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "play"

        if button("Leaderboard",100,230,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "leaderboard"

        if button("Settings",100,310,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "settings"

        if button("Quit",100,390,200,50,mouse):
            if pygame.mouse.get_pressed()[0]:
                return "quit"

        pygame.display.update()

# ================= MAIN =================
load_settings()

state = "menu"
player_name = "Player"

while True:
    if state == "menu":
        state = menu()

    elif state == "play":
        state = run_game(player_name)

    elif state == "settings":
        state = settings_screen()

    elif state == "leaderboard":
        state = leaderboard_screen()

    elif state == "quit":
        pygame.quit()
        sys.exit()