#Imports
import pygame, sys
from pygame.locals import *
import random, time
import math
import json
import os

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
MAX_OBSTACLES = 3
MAX_EVENTS = 2

# Distance and race variables
TOTAL_DISTANCE = 1000  # Total distance to finish
distance_traveled = 0
player_name = ""

# Leaderboard file
LEADERBOARD_FILE = "leaderboard.json"
SETTINGS_FILE = "settings.json"

# Default settings
default_settings = {
    "sound_enabled": True,
    "car_color": "red",
    "difficulty": "normal"
}

# Game settings (loaded from file)
game_settings = default_settings.copy()

def load_settings():
    """Load settings from JSON file"""
    global game_settings
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to ensure all keys exist
                game_settings = {**default_settings, **loaded}
        except:
            game_settings = default_settings.copy()
    else:
        game_settings = default_settings.copy()
    return game_settings

def save_settings():
    """Save settings to JSON file"""
    with open(SETTINGS_FILE, 'w') as f:
        json.dump(game_settings, f, indent=2)

def apply_settings():
    """Apply saved preferences to the game"""
    global SPEED, COIN_SPEED, MAX_OBSTACLES, MAX_EVENTS
    
    # Apply difficulty settings
    difficulty = game_settings.get("difficulty", "normal")
    if difficulty == "easy":
        SPEED = 4
        COIN_SPEED = 4
        MAX_OBSTACLES = 2
        MAX_EVENTS = 1
    elif difficulty == "hard":
        SPEED = 7
        COIN_SPEED = 7
        MAX_OBSTACLES = 4
        MAX_EVENTS = 3
    else:  # normal
        SPEED = 5
        COIN_SPEED = 5
        MAX_OBSTACLES = 3
        MAX_EVENTS = 2


# Color for leaderboard
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

# Car color options
CAR_COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128)
}

# Car colors with their appropriate images
CAR_IMAGES = {
    "red": "player_red.png",
    "blue": "player_blue.png",
    "green": "player_green.png",
    "yellow": "player_yellow.png",
    "purple": "player_purple.png"
}

# ==================== SCREEN FUNCTIONS ====================

def draw_button(surface, text, x, y, w, h, color, hover_color, is_hovered):
    """Draw a button with hover effect"""
    btn_color = hover_color if is_hovered else color
    pygame.draw.rect(surface, btn_color, (x, y, w, h))
    pygame.draw.rect(surface, BLACK, (x, y, w, h), 2)
    
    text_surf = font_small.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(x + w//2, y + h//2))
    surface.blit(text_surf, text_rect)

def is_over_button(mouse_pos, x, y, w, h):
    """Check if mouse is over button"""
    mx, my = mouse_pos
    return x <= mx <= x + w and y <= my <= y + h

def show_main_menu():
    """Display main menu screen with Play, Leaderboard, Settings, Quit buttons"""
    menu_running = True
    
    # Button definitions
    buttons = [
        {"text": "Play", "y": 180},
        {"text": "Leaderboard", "y": 260},
        {"text": "Settings", "y": 340},
        {"text": "Quit", "y": 420}
    ]
    button_width = 200
    button_height = 50
    button_x = (SCREEN_WIDTH - button_width) // 2
    
    while menu_running:
        DISPLAYSURF.fill(WHITE)
        
        # Title
        title = font.render("Racing Game", True, BLUE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 80))
        DISPLAYSURF.blit(title, title_rect)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons
        for btn in buttons:
            y = btn["y"]
            is_hovered = is_over_button(mouse_pos, button_x, y, button_width, button_height)
            draw_button(DISPLAYSURF, btn["text"], button_x, y, button_width, button_height, GREEN, YELLOW, is_hovered)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                for btn in buttons:
                    y = btn["y"]
                    if is_over_button((mx, my), button_x, y, button_width, button_height):
                        if btn["text"] == "Play":
                            return "play"
                        elif btn["text"] == "Leaderboard":
                            return "leaderboard"
                        elif btn["text"] == "Settings":
                            return "settings"
                        elif btn["text"] == "Quit":
                            pygame.quit()
                            sys.exit()
    
    return "quit"

def show_settings_screen():
    """Display settings screen with sound toggle, car color, difficulty"""
    settings_running = True
    
    # Load current settings
    current_settings = load_settings()
    
    # UI elements
    sound_y = 150
    color_y = 250
    difficulty_y = 350
    back_y = 480
    button_width = 150
    button_height = 40
    small_btn_width = 100
    small_btn_height = 35
    
    while settings_running:
        DISPLAYSURF.fill(WHITE)
        
        # Title
        title = font.render("Settings", True, BLACK)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        DISPLAYSURF.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Sound toggle
        sound_label = font_small.render("Sound:", True, BLACK)
        DISPLAYSURF.blit(sound_label, (50, sound_y))
        
        sound_state = "ON" if current_settings["sound_enabled"] else "OFF"
        is_sound_hover = is_over_button(mouse_pos, 200, sound_y - 10, small_btn_width, small_btn_height)
        draw_button(DISPLAYSURF, sound_state, 200, sound_y - 10, small_btn_width, small_btn_height, 
                   GREEN if current_settings["sound_enabled"] else RED, YELLOW, is_sound_hover)
        
        # Car color selection
        color_label = font_small.render("Car Color:", True, BLACK)
        DISPLAYSURF.blit(color_label, (50, color_y))
        
        color_x = 200
        for color_name, color_rgb in CAR_COLORS.items():
            is_color_hover = is_over_button(mouse_pos, color_x, color_y - 10, 30, 30)
            pygame.draw.rect(DISPLAYSURF, color_rgb, (color_x, color_y - 10, 30, 30))
            pygame.draw.rect(DISPLAYSURF, BLACK, (color_x, color_y - 10, 30, 30), 2)
            if current_settings["car_color"] == color_name:
                pygame.draw.rect(DISPLAYSURF, WHITE, (color_x - 2, color_y - 12, 34, 34), 3)
            color_x += 40
        
        # Difficulty selection
        diff_label = font_small.render("Difficulty:", True, BLACK)
        DISPLAYSURF.blit(diff_label, (50, difficulty_y))
        
        difficulties = ["easy", "normal", "hard"]
        diff_x = 140
        for diff in difficulties:
            is_diff_hover = is_over_button(mouse_pos, diff_x, difficulty_y - 10, small_btn_width, small_btn_height)
            btn_color = GREEN if current_settings["difficulty"] == diff else (200, 200, 200)
            draw_button(DISPLAYSURF, diff.capitalize(), diff_x, difficulty_y - 10, small_btn_width, small_btn_height, 
                       btn_color, YELLOW, is_diff_hover)
            diff_x += 75
        
        # Back button
        is_back_hover = is_over_button(mouse_pos, (SCREEN_WIDTH - button_width)//2, back_y, button_width, button_height)
        draw_button(DISPLAYSURF, "Back", (SCREEN_WIDTH - button_width)//2, back_y, button_width, button_height, 
                   BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                # Sound toggle
                if is_over_button((mx, my), 200, sound_y - 10, small_btn_width, small_btn_height):
                    current_settings["sound_enabled"] = not current_settings["sound_enabled"]
                
                # Car color
                color_x = 200
                for color_name in CAR_COLORS.keys():
                    if is_over_button((mx, my), color_x, color_y - 10, 30, 30):
                        current_settings["car_color"] = color_name
                    color_x += 40
                
                # Difficulty
                diff_x = 140
                for diff in difficulties:
                    if is_over_button((mx, my), diff_x, difficulty_y - 10, small_btn_width, small_btn_height):
                        current_settings["difficulty"] = diff
                    diff_x += 75
                
                # Back button
                if is_over_button((mx, my), (SCREEN_WIDTH - button_width)//2, back_y, button_width, button_height):
                    # Save and apply settings before returning
                    game_settings.update(current_settings)
                    save_settings()
                    apply_settings()
                    return "menu"
    
    return "menu"

def show_game_over_screen(final_score, final_distance, final_coins):
    # check whether the music of background still playing, if yes, untoggle
    if game_settings.get("sound_enabled", True) and pygame.mixer.get_busy():
        pygame.mixer.stop()
    """Display game over screen with score, distance, coins, and buttons: Retry, Main Menu"""
    game_over_running = True
    
    button_width = 150
    button_height = 50
    retry_x = 50
    menu_x = 220
    button_y = 420
    
    while game_over_running:
        DISPLAYSURF.fill(RED)
        
        # Title
        title = font.render("Game Over", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 50))
        DISPLAYSURF.blit(title, title_rect)
        
        # Stats
        score_label = font.render(f"Score: {final_score}", True, WHITE)
        score_rect = score_label.get_rect(center=(SCREEN_WIDTH//2, 150))
        DISPLAYSURF.blit(score_label, score_rect)
        
        distance_label = font_small.render(f"Distance: {final_distance}", True, WHITE)
        dist_rect = distance_label.get_rect(center=(SCREEN_WIDTH//2, 220))
        DISPLAYSURF.blit(distance_label, dist_rect)
        
        coins_label = font_small.render(f"Coins: {final_coins}", True, WHITE)
        coins_rect = coins_label.get_rect(center=(SCREEN_WIDTH//2, 260))
        DISPLAYSURF.blit(coins_label, coins_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Buttons
        is_retry_hover = is_over_button(mouse_pos, retry_x, button_y, button_width, button_height)
        is_menu_hover = is_over_button(mouse_pos, menu_x, button_y, button_width, button_height)
        
        draw_button(DISPLAYSURF, "Retry", retry_x, button_y, button_width, button_height, GREEN, YELLOW, is_retry_hover)
        draw_button(DISPLAYSURF, "Main Menu", menu_x, button_y, button_width, button_height, BLUE, YELLOW, is_menu_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                if is_over_button((mx, my), retry_x, button_y, button_width, button_height):
                    return "retry"
                if is_over_button((mx, my), menu_x, button_y, button_width, button_height):
                    return "menu"
    
    return "menu"

def show_standalone_leaderboard():
    """Display leaderboard screen with back button (called from menu)"""
    leaderboard = load_leaderboard()
    
    button_width = 100
    button_height = 40
    back_x = (SCREEN_WIDTH - button_width) // 2
    back_y = 520
    
    while True:
        DISPLAYSURF.fill(BLACK)
        
        title = font.render("LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 30))
        DISPLAYSURF.blit(title, title_rect)
        
        # Draw header
        headers = ["Rank", "Name", "Score", "Distance"]
        x_positions = [30, 100, 210, 300]
        
        for i, header in enumerate(headers):
            header_surf = font_small.render(header, True, GREEN)
            DISPLAYSURF.blit(header_surf, (x_positions[i], 70))
        
        pygame.draw.line(DISPLAYSURF, WHITE, (20, 100), (380, 100), 2)
        
        # Draw entries or empty message
        if not leaderboard:
            empty_msg = font_small.render("No scores yet!", True, WHITE)
            empty_rect = empty_msg.get_rect(center=(SCREEN_WIDTH//2, 250))
            DISPLAYSURF.blit(empty_msg, empty_rect)
        else:
            for idx, entry in enumerate(leaderboard):
                y_pos = 120 + idx * 35
                
                rank_surf = font_small.render(f"{idx + 1}.", True, WHITE)
                name_surf = font_small.render(entry["name"][:10], True, WHITE)
                score_surf = font_small.render(str(entry["score"]), True, WHITE)
                dist_surf = font_small.render(str(entry["distance"]), True, WHITE)
                
                DISPLAYSURF.blit(rank_surf, (x_positions[0], y_pos))
                DISPLAYSURF.blit(name_surf, (x_positions[1], y_pos))
                DISPLAYSURF.blit(score_surf, (x_positions[2], y_pos))
                DISPLAYSURF.blit(dist_surf, (x_positions[3], y_pos))
        
        # Back button
        mouse_pos = pygame.mouse.get_pos()
        is_back_hover = is_over_button(mouse_pos, back_x, back_y, button_width, button_height)
        draw_button(DISPLAYSURF, "Back", back_x, back_y, button_width, button_height, BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    return "menu"
    
    return "menu"


# Create EMPTY groups
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
events = pygame.sprite.Group()
powerups = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

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

def load_leaderboard():
    """Load leaderboard from JSON file"""
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, 'r') as f:
                return json.load(f)
        except:
            return []
    return []

def save_leaderboard(leaderboard):
    """Save leaderboard to JSON file"""
    with open(LEADERBOARD_FILE, 'w') as f:
        json.dump(leaderboard, f, indent=2)

def calculate_final_score():
    """Calculate final score: distance + coins * 10 + SCORE * 5 + power-up bonuses"""
    base_score = distance_traveled + (COIN_SCORE * 10) + (SCORE * 5)
    # Bonus for finishing
    if distance_traveled >= TOTAL_DISTANCE:
        base_score += 500
    return base_score

def get_username():
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
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    input_text = input_text[:-1]
                elif event.key == K_RETURN:
                    if input_text.strip():
                        entering = False
                        return input_text.strip()
                elif event.unicode.isalnum() or event.unicode in ['_', '-']:
                    if len(input_text) < 15:
                        input_text += event.unicode

def show_leaderboard(final_score):
    """Display leaderboard screen with top 10 scores (after game over)"""
    leaderboard = load_leaderboard()
    
    # Add current score
    new_entry = {
        "name": player_name,
        "score": final_score,
        "distance": distance_traveled
    }
    leaderboard.append(new_entry)
    
    # Sort by score descending and keep top 10
    leaderboard.sort(key=lambda x: x["score"], reverse=True)
    leaderboard = leaderboard[:10]
    
    # Save updated leaderboard
    save_leaderboard(leaderboard)
    
    # Display leaderboard with back button
    button_width = 150
    button_height = 40
    back_x = (SCREEN_WIDTH - button_width) // 2
    back_y = 520
    
    showing = True
    while showing:
        DISPLAYSURF.fill(BLACK)
        
        title = font.render("TOP 10 LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, 30))
        DISPLAYSURF.blit(title, title_rect)
        
        # Draw header
        headers = ["Rank", "Name", "Score", "Distance"]
        x_positions = [20, 100, 220, 320]
        
        for i, header in enumerate(headers):
            header_surf = font_small.render(header, True, GREEN)
            DISPLAYSURF.blit(header_surf, (x_positions[i], 60))
        
        # Draw separator line
        pygame.draw.line(DISPLAYSURF, WHITE, (20, 85), (380, 85), 2)
        
        # Draw leaderboard entries
        for idx, entry in enumerate(leaderboard):
            y_pos = 100 + idx * 35
            
            rank_surf = font_small.render(f"{idx + 1}.", True, WHITE)
            name_surf = font_small.render(entry["name"][:10], True, WHITE)
            score_surf = font_small.render(str(entry["score"]), True, WHITE)
            dist_surf = font_small.render(str(entry["distance"]), True, WHITE)
            
            DISPLAYSURF.blit(rank_surf, (x_positions[0], y_pos))
            DISPLAYSURF.blit(name_surf, (x_positions[1], y_pos))
            DISPLAYSURF.blit(score_surf, (x_positions[2], y_pos))
            DISPLAYSURF.blit(dist_surf, (x_positions[3], y_pos))
        
        # Back button with mouse hover
        mouse_pos = pygame.mouse.get_pos()
        is_back_hover = is_over_button(mouse_pos, back_x, back_y, button_width, button_height)
        draw_button(DISPLAYSURF, "Back to Menu", back_x, back_y, button_width, button_height, BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    showing = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    showing = False
    
    return False

# Color for leaderboard
YELLOW = (255, 255, 0)

#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

background = pygame.image.load("assets/AnimatedStreet.png")
background_music = pygame.mixer.Sound('assets/background.wav')

        
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
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-self.current_speed, 0)

        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
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
while True:
    # Show main menu and get choice
    choice = show_main_menu()
    
    if choice == "play":
        # Get username before playing
        player_name = get_username()
        
        # Reset game variables for new game
        SCORE = 0
        COIN_SCORE = 0
        distance_traveled = 0
        SPEED = 5
        COIN_SPEED = 5
        SUFFICIENT_COIN_INCREASE = 5
        
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
        
        # Game loop
        while True:
            # check sound playing
            if game_settings.get("sound_enabled", True) and not pygame.mixer.get_busy():
                background_music.play(-1)  # Loop indefinitely
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
                    else: continue
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
                    result = show_game_over_screen(final_score, distance_traveled, COIN_SCORE)
                    
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
                        show_leaderboard(final_score)
                        # Return to main menu
                        break  # Break out of inner game loop        
            pygame.display.update()
            FramePerSec.tick(FPS)
    elif choice == "leaderboard":
        show_leaderboard(final_score=0)  # Pass dummy score since we're just viewing
    elif choice == "settings":
        show_settings_screen()
# Exit game cleanly from main menu
pygame.quit()
sys.exit()