import pygame
import sys
import random
from db import execute_query
import json
import os
import datetime

# Initialize pygame
pygame.init()

# Create window
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Snake")
sound_eat = pygame.mixer.Sound("assets/snake_eat.mp3")


# =========================
# logistics (db, config, settings, leaderboards)
SETTINGS_FILE = "settings.json"

# Default settings
default_settings = {
    "snake_color": (0, 255, 255),
    "grid_overlay_status": True,
    "sound_enabled": True
}

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
    pass

def get_snake_color():
    """Get the current snake color from settings"""
    color_setting = game_settings.get("snake_color", (0, 255, 255))
    # If it's a string key, convert to RGB tuple
    if isinstance(color_setting, str):
        return SNAKE_COLORS.get(color_setting, (0, 255, 255))
    return color_setting

# Basic colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Color for leaderboard
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)

SNAKE_COLORS = {
    "red": (255, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 255, 0),
    "yellow": (255, 255, 0),
    "purple": (128, 0, 128)
}



# =========================
# Snake class
# =========================
class Snake:
    def __init__(self):
        self.size = 20
        self.body = [(300, 200)]  # list of segments
        self.dx = self.size
        self.dy = 0
        self.grow = False  # growth flag

    def move(self):
        head_x, head_y = self.body[0]

        # Create new head based on direction
        new_head = (head_x + self.dx, head_y + self.dy)
        self.body.insert(0, new_head)

        # Remove tail unless growing
        if not self.grow:
            self.body.pop()
        else:
            self.grow = False

    def draw(self, screen):
        # Get snake color from settings
        color_setting = game_settings.get("snake_color", (0, 255, 255))
        if isinstance(color_setting, str):
            snake_color = SNAKE_COLORS.get(color_setting, (0, 255, 255))
        else:
            snake_color = color_setting
            
        for segment in self.body:
            pygame.draw.rect(
                screen,
                snake_color,
                (segment[0], segment[1], self.size, self.size)
            )

    def change_direction(self, dx, dy):
        # Prevent reversing
        if self.dx == -dx and self.dy == -dy:
            return
        self.dx = dx
        self.dy = dy

    def change_speed(self, new_speed):
        # Speed change logic can be implemented here if needed
        pass


# =========================
# FUNCTIONS
# =========================
def generate_food(snake, WIDTH, HEIGHT, size, forbidden):
    while True:
        x = random.randint(0, (WIDTH // size) - 1) * size
        y = random.randint(0, (HEIGHT // size) - 1) * size

        if (x, y) not in snake.body and (x, y) not in forbidden:
            return (x, y)

# reset snake position to safe place
def reset_snake_safe(snake):
    center_x = (WIDTH // snake.size // 2) * snake.size
    center_y = (HEIGHT // snake.size // 2) * snake.size

    snake.body = [
        (center_x, center_y),
        (center_x - snake.size, center_y),
        (center_x - 2 * snake.size, center_y)
    ]

    snake.dx = snake.size
    snake.dy = 0

def generate_obstacles(snake, count, forbidden):
    new_obstacles = []

    attempts = 0
    while len(new_obstacles) < count and attempts < 200:
        attempts += 1

        x = random.randint(0, (WIDTH // snake.size) - 1) * snake.size
        y = random.randint(0, (HEIGHT // snake.size) - 1) * snake.size

        pos = (x, y)

        if (
            pos not in snake.body and
            pos not in forbidden and
            pos not in new_obstacles
        ):
            new_obstacles.append(pos)
        if abs(x - snake.body[0][0]) < 60 and abs(y - snake.body[0][1]) < 60:
            continue
    return new_obstacles

# draw grid overlay pixels
def draw_grid(screen, width, height, cell_size):
    for x in range(0, width, cell_size):
        pygame.draw.line(screen, (220, 220, 220), (x, 0), (x, height))
    for y in range(0, height, cell_size):
        pygame.draw.line(screen, (220, 220, 220), (0, y), (width, y))

def load_leaderboard():
    """Load top 10 leaderboard from PostgreSQL database"""
    sql = """
    SELECT p.username, gs.score, gs.level_reached, gs.played_at
    FROM game_sessions gs
    JOIN players p ON gs.player_id = p.id
    ORDER BY gs.score DESC
    LIMIT 10
    """
    try:
        result = execute_query(sql)
        if result:
            # Convert tuple results to list of dicts
            leaderboard = []
            for row in result:
                leaderboard.append({
                    "username": row[0],
                    "score": row[1],
                    "level_reached": row[2],
                    "played_at": row[3]
                })
            return leaderboard
        return []
    except Exception as e:
        print(f"Error loading leaderboard: {e}")
        return []

def get_personal_best(username):
    """Fetch the player's best score"""
    sql = """
    SELECT MAX(gs.score)
    FROM game_sessions gs
    JOIN players p ON gs.player_id = p.id
    WHERE p.username = %s
    """
    try:
        result = execute_query(sql, (username,))
        if result and result[0][0] is not None:
            return result[0][0]
        return 0
    except Exception as e:
        print(f"Error getting personal best: {e}")
        return 0

def save_game_result(username, score, level_reached):
    """Save player result to database"""
    # First, ensure player exists (insert if not)
    sql_player = """
    INSERT INTO players (username)
    VALUES (%s)
    ON CONFLICT (username) DO NOTHING
    """
    execute_query(sql_player, (username,))
    
    # Get player_id
    sql_get_id = """
    SELECT id FROM players WHERE username = %s
    """
    # Insert game session
    sql_insert = """
    INSERT INTO game_sessions (player_id, score, level_reached, played_at)
    VALUES (
        (SELECT id FROM players WHERE username = %s),
        %s, %s, NOW() AT TIME ZONE 'Asia/Almaty'
    )
    """
    execute_query(sql_insert, (username, score, level_reached))

def get_username():
    """Display username entry screen"""
    input_text = ""
    entering = True
    
    while entering:
        screen.fill(WHITE)
        
        # Title
        title = font_small.render("Enter Your Name", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        # Show input box
        input_box = pygame.Rect(150, 180, 300, 40)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        
        name_surface = font_small.render(input_text if input_text else "Type here...", True, BLACK)
        name_rect = name_surface.get_rect(center=input_box.center)
        screen.blit(name_surface, name_rect)
        
        instruction = font_small.render("Press ENTER to start", True, BLUE)
        instr_rect = instruction.get_rect(center=(WIDTH//2, 260))
        screen.blit(instruction, instr_rect)
        
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
                        return input_text.strip()
                elif event.unicode.isalnum() or event.unicode in ['_', '-']:
                    if len(input_text) < 15:
                        input_text += event.unicode

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
    
    # Button definitions - adjusted for 400px height window
    buttons = [
        {"text": "Play", "y": 140},
        {"text": "Leaderboard", "y": 200},
        {"text": "Settings", "y": 260},
        {"text": "Quit", "y": 320}
    ]
    button_width = 200
    button_height = 45
    button_x = (WIDTH - button_width) // 2
    
    while menu_running:
        screen.fill(WHITE)
        
        # Title
        title = font_small.render("Mini Snake", True, BLUE)
        title_rect = title.get_rect(center=(WIDTH//2, 60))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_small.render("Press a button to start", True, BLACK)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 90))
        screen.blit(subtitle, subtitle_rect)
        
        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons
        for btn in buttons:
            y = btn["y"]
            is_hovered = is_over_button(mouse_pos, button_x, y, button_width, button_height)
            draw_button(screen, btn["text"], button_x, y, button_width, button_height, GREEN, YELLOW, is_hovered)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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
    """Display settings screen with sound toggle, snake color, grid overlay"""
    settings_running = True
    
    # Load current settings
    current_settings = load_settings()
    
    # UI elements - adjusted for 400px height
    sound_y = 100
    grid_y = 150
    color_y = 200
    back_y = 300
    button_width = 150
    button_height = 40
    small_btn_width = 100
    small_btn_height = 35
    
    while settings_running:
        screen.fill(WHITE)
        
        # Title
        title = font_small.render("Settings", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 40))
        screen.blit(title, title_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Sound toggle
        sound_label = font_small.render("Sound:", True, BLACK)
        screen.blit(sound_label, (50, sound_y))
        
        sound_state = "ON" if current_settings["sound_enabled"] else "OFF"
        is_sound_hover = is_over_button(mouse_pos, 200, sound_y - 10, small_btn_width, small_btn_height)
        draw_button(screen, sound_state, 200, sound_y - 10, small_btn_width, small_btn_height, 
                   GREEN if current_settings["sound_enabled"] else RED, YELLOW, is_sound_hover)
        
        # Grid overlay toggle
        grid_label = font_small.render("Grid:", True, BLACK)
        screen.blit(grid_label, (50, grid_y))
        
        grid_state = "ON" if current_settings.get("grid_overlay_status", True) else "OFF"
        is_grid_hover = is_over_button(mouse_pos, 200, grid_y - 10, small_btn_width, small_btn_height)
        draw_button(screen, grid_state, 200, grid_y - 10, small_btn_width, small_btn_height, 
                   GREEN if current_settings.get("grid_overlay_status", True) else RED, YELLOW, is_grid_hover)
        
        # Snake color selection
        color_label = font_small.render("Snake:", True, BLACK)
        screen.blit(color_label, (50, color_y))
        
        # Draw color options in a single row
        color_x = 120
        for color_name, color_rgb in SNAKE_COLORS.items():
            is_color_hover = is_over_button(mouse_pos, color_x, color_y - 5, 25, 25)
            pygame.draw.rect(screen, color_rgb, (color_x, color_y - 5, 25, 25))
            pygame.draw.rect(screen, BLACK, (color_x, color_y - 5, 25, 25), 2)
            # Check if this color is selected (handle both string and RGB tuple)
            selected_color = current_settings.get("snake_color", (0, 255, 255))
            if selected_color == color_name or selected_color == color_rgb:
                pygame.draw.rect(screen, WHITE, (color_x - 2, color_y - 7, 29, 29), 3)
            color_x += 35
        
        # Back button
        is_back_hover = is_over_button(mouse_pos, (WIDTH - button_width)//2, back_y, button_width, button_height)
        draw_button(screen, "Save & Back", (WIDTH - button_width)//2, back_y, button_width, button_height, 
                   BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                # Sound toggle
                if is_over_button((mx, my), 200, sound_y - 10, small_btn_width, small_btn_height):
                    current_settings["sound_enabled"] = not current_settings["sound_enabled"]
                
                # Grid overlay toggle
                if is_over_button((mx, my), 200, grid_y - 10, small_btn_width, small_btn_height):
                    current_settings["grid_overlay_status"] = not current_settings.get("grid_overlay_status", True)
                
                # Snake color
                color_x = 120
                for color_name in SNAKE_COLORS.keys():
                    if is_over_button((mx, my), color_x, color_y - 5, 25, 25):
                        current_settings["snake_color"] = color_name
                    color_x += 35
                
                
                # Back button
                if is_over_button((mx, my), (WIDTH - button_width)//2, back_y, button_width, button_height):
                    # Save and apply settings before returning
                    game_settings.update(current_settings)
                    save_settings()
                    apply_settings()
                    return "menu"
    
    return "menu"

def show_game_over_screen(final_score, final_level, personal_best=0):
    """Display game over screen with score, level, personal best, and buttons: Retry, Main Menu"""
    # check whether the music of background still playing, if yes, untoggle
    if game_settings.get("sound_enabled", True) and pygame.mixer.get_busy():
        pygame.mixer.stop()
    
    game_over_running = True
    
    # Adjusted for 400px height window
    button_width = 140
    button_height = 40
    retry_x = 80
    menu_x = 250
    button_y = 320
    
    while game_over_running:
        screen.fill(RED)
        
        # Title
        title = font_small.render("Game Over", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 40))
        screen.blit(title, title_rect)
        
        # Stats
        score_label = font_small.render(f"Score: {final_score}", True, WHITE)
        score_rect = score_label.get_rect(center=(WIDTH//2, 100))
        screen.blit(score_label, score_rect)
        
        level_label = font_small.render(f"Level: {final_level}", True, WHITE)
        level_rect = level_label.get_rect(center=(WIDTH//2, 140))
        screen.blit(level_label, level_rect)
        
        personal_best_label = font_small.render(f"Best: {personal_best}", True, WHITE)
        pb_rect = personal_best_label.get_rect(center=(WIDTH//2, 180))
        screen.blit(personal_best_label, pb_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Buttons
        is_retry_hover = is_over_button(mouse_pos, retry_x, button_y, button_width, button_height)
        is_menu_hover = is_over_button(mouse_pos, menu_x, button_y, button_width, button_height)
        
        draw_button(screen, "Retry", retry_x, button_y, button_width, button_height, GREEN, YELLOW, is_retry_hover)
        draw_button(screen, "Menu", menu_x, button_y, button_width, button_height, BLUE, YELLOW, is_menu_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                
                if is_over_button((mx, my), retry_x, button_y, button_width, button_height):
                    return "retry"
                if is_over_button((mx, my), menu_x, button_y, button_width, button_height):
                    return "menu"
    
    return "menu"

def show_standalone_leaderboard():
    """Display leaderboard screen with back button (called from menu)"""
    leaderboard = load_leaderboard()
    
    # Adjusted for 400px height window
    button_width = 100
    button_height = 35
    back_x = (WIDTH - button_width) // 2
    back_y = 350
    
    while True:
        screen.fill(BLACK)
        
        # Title
        title = font_small.render("LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 20))
        screen.blit(title, title_rect)
        
        # Draw header - added Date column
        headers = ["Rank", "Name", "Score", "Date"]
        x_positions = [20, 70, 140, 210]
        
        for i, header in enumerate(headers):
            header_surf = font_small.render(header, True, GREEN)
            screen.blit(header_surf, (x_positions[i], 45))
        
        pygame.draw.line(screen, WHITE, (20, 60), (380, 60), 1)
        
        # Draw entries or empty message (limited to 7 to fit with date)
        if not leaderboard:
            empty_msg = font_small.render("No scores yet!", True, WHITE)
            empty_rect = empty_msg.get_rect(center=(WIDTH//2, 180))
            screen.blit(empty_msg, empty_rect)
        else:
            for idx, entry in enumerate(leaderboard[:10]):
                y_pos = 75 + idx * 25
                
                # Format date as %d.%m.%Y-%H:%M:%S
                played_at = entry.get("played_at")
                if played_at:
                    try:
                        date_obj = played_at if isinstance(played_at, datetime.datetime) else datetime.datetime.fromisoformat(str(played_at))
                        date_str = date_obj.strftime("%d.%m.%y %H:%M")
                    except:
                        date_str = "-"
                else:
                    date_str = "-"
                
                rank_surf = font_small.render(f"{idx + 1}.", True, WHITE)
                name_surf = font_small.render(entry.get("username", "?")[:8], True, WHITE)
                score_surf = font_small.render(str(entry.get("score", 0)), True, WHITE)
                date_surf = font_small.render(date_str, True, WHITE)
                
                screen.blit(rank_surf, (x_positions[0], y_pos))
                screen.blit(name_surf, (x_positions[1], y_pos))
                screen.blit(score_surf, (x_positions[2], y_pos))
                screen.blit(date_surf, (x_positions[3], y_pos))
        
        # Back button
        mouse_pos = pygame.mouse.get_pos()
        is_back_hover = is_over_button(mouse_pos, back_x, back_y, button_width, button_height)
        draw_button(screen, "Back", back_x, back_y, button_width, button_height, BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    return "menu"
    
    return "menu"

def show_leaderboard(final_score):
    """Display leaderboard screen with top 10 scores (after game over)"""
    leaderboard = load_leaderboard()
    
    # Add current score
    new_entry = {
        "username": player_name,
        "score": final_score,
        "level_reached": LEVEL,
        "played_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    leaderboard.append(new_entry)
    
    # Sort by score descending and keep top 10
    leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
    leaderboard = leaderboard[:10]
    
    # Save to database
    save_game_result(player_name, final_score, LEVEL)
    
    # Display leaderboard with back button - adjusted for 400px height
    button_width = 150
    button_height = 35
    back_x = (WIDTH - button_width) // 2
    back_y = 350
    
    showing = True
    while showing:
        screen.fill(BLACK)
        
        # Title
        title = font_small.render("LEADERBOARD", True, WHITE)
        title_rect = title.get_rect(center=(WIDTH//2, 20))
        screen.blit(title, title_rect)
        
        # Draw header - added Date column
        headers = ["Rank", "Name", "Score", "Date"]
        x_positions = [20, 70, 140, 210]
        
        for i, header in enumerate(headers):
            header_surf = font_small.render(header, True, GREEN)
            screen.blit(header_surf, (x_positions[i], 45))
        
        pygame.draw.line(screen, WHITE, (20, 60), (380, 60), 1)
        
        # Draw entries or empty message (limited to 7 to fit with date)
        if not leaderboard:
            empty_msg = font_small.render("No scores yet!", True, WHITE)
            empty_rect = empty_msg.get_rect(center=(WIDTH//2, 180))
            screen.blit(empty_msg, empty_rect)
        else:
            for idx, entry in enumerate(leaderboard[:10]):
                y_pos = 75 + idx * 25
                
                # Format date as %d.%m.%Y-%H:%M:%S
                played_at = entry.get("played_at")
                if played_at:
                    try:
                        date_obj = played_at if isinstance(played_at, datetime.datetime) else datetime.datetime.fromisoformat(str(played_at))
                        date_str = date_obj.strftime("%d.%m.%y %H:%M")
                    except:
                        date_str = "-"
                else:
                    date_str = "-"
                
                rank_surf = font_small.render(f"{idx + 1}.", True, WHITE)
                name_surf = font_small.render(entry.get("username", "?")[:8], True, WHITE)
                score_surf = font_small.render(str(entry.get("score", 0)), True, WHITE)
                date_surf = font_small.render(date_str, True, WHITE)
                
                screen.blit(rank_surf, (x_positions[0], y_pos))
                screen.blit(name_surf, (x_positions[1], y_pos))
                screen.blit(score_surf, (x_positions[2], y_pos))
                screen.blit(date_surf, (x_positions[3], y_pos))
        
        # Back button
        mouse_pos = pygame.mouse.get_pos()
        is_back_hover = is_over_button(mouse_pos, back_x, back_y, button_width, button_height)
        draw_button(screen, "Back", back_x, back_y, button_width, button_height, BLUE, YELLOW, is_back_hover)
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    return "menu"
                    showing = False
    
    return False



# =========================
# Config
# =========================
clock = pygame.time.Clock()

LEVEL_FPS = {
    1: 20,
    2: 25,
    3: 30
}

LEVEL_COLORS = {
    1: (255, 255, 255),   # white
    2: (255, 215, 0),     # gold
    3: (0, 183, 235),      # light blue
}

FOOD_LIFETIME = 5000  # 5 seconds

# =========================
# Init game objects
# =========================
snake = Snake()
food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [])
food_spawn_time = pygame.time.get_ticks()
poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
poison_spawn_time = pygame.time.get_ticks()
POISON_LIFETIME = 7000  # optional (you can remove if you want permanent poison)

# Power-up config
POWERUP_LIFETIME = 8000
POWERUP_CHANCE = 0.05  # 5%

powerup_pos = None
powerup_type = None
powerup_spawn_time = 0

# Active effects
active_power = None
power_start_time = 0

shield_active = False

POWER_SPEED_UP = "speed_up"
POWER_SLOW = "slow"
POWER_SHIELD = "shield"

respawn_freeze = False
respawn_start_time = 0
RESPAWN_DURATION = 3000  # 3 seconds

# Obstacles
obstacles = []

obstacles_disabled = False
obstacles_disabled_start = 0
OBSTACLE_DISABLE_DURATION = 5000  # 5 sec AFTER recovery
print_userevent = pygame.USEREVENT + 1
pygame.time.set_timer(print_userevent, 1000)  # every 1 second


SCORE = 0
LEVEL = 1

# Fonts
font_small = pygame.font.SysFont("Georgia", 16)
font_big = pygame.font.SysFont(None, 50)

game_over_text = font_big.render("Game Over!", True, (255, 255, 255))

prev_level = LEVEL

# =========================
# SCENES
# =========================
# def running_scene():
#     # ---------------------
#     # Game logic
#     # ---------------------
#     # global variables
#     global food_pos, food_spawn_time, poison_pos, poison_spawn_time, powerup_pos, powerup_type, powerup_spawn_time, active_power, power_start_time, shield_active, respawn_freeze, respawn_start_time, obstacles_disabled, obstacles_disabled_start, obstacles, LEVEL, prev_level, SCORE, game_over, WIDTH, HEIGHT, screen, snake
#     if not game_over:
#         current_time = pygame.time.get_ticks()
#         if not respawn_freeze:
#             snake.move()

#         head = snake.body[0]
#         head_x, head_y = head

#         # Wall collision
#         collision = (
#             head_x < 0 or head_x >= WIDTH or
#             head_y < 0 or head_y >= HEIGHT or
#             head in snake.body[1:] or
#             head in obstacles
#         )

#         if collision:
#             if shield_active:
#                 shield_active = False

#                 reset_snake_safe(snake)

#                 respawn_freeze = True
#                 respawn_start_time = pygame.time.get_ticks()

#                 powerup_type = None
#                 active_power = None

#                 # disable obstacles AFTER recovery
#                 obstacles_disabled = True
#                 obstacles_disabled_start = pygame.time.get_ticks()

#             else:
#                 game_over = True

#         if respawn_freeze:
#             if current_time - respawn_start_time < RESPAWN_DURATION:
#                 # Skip movement
#                 pass
#             else:
#                 respawn_freeze = False

#         if obstacles_disabled:
#             if current_time - obstacles_disabled_start > (RESPAWN_DURATION + OBSTACLE_DISABLE_DURATION):
#                 obstacles_disabled = False

#                 if LEVEL >= 3:
#                     obstacles = generate_obstacles(
#                         snake,
#                         LEVEL - 2,
#                         [food_pos, poison_pos]
#                     )
#                     obstacles_disabled = False

#         # Food eaten
#         if head == food_pos:

#             snake.grow = True
#             food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [poison_pos])
#             food_spawn_time = pygame.time.get_ticks()

#             SCORE += random.randint(1, 3)
#             sound_eat.play()  # Play eat sound
#         # Poison eaten
#         if head == poison_pos:
#             sound_eat.play()
#             # shrink snake by 2
#             for _ in range(2):
#                 if len(snake.body) > 1:
#                     snake.body.pop()

#             # Check death condition
#             if len(snake.body) <= 1:
#                 game_over = True

#             # Respawn poison
#             poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
#             poison_spawn_time = pygame.time.get_ticks()

#         # Food expiration
#         current_time = pygame.time.get_ticks()
#         if current_time - food_spawn_time > FOOD_LIFETIME:
#             food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [poison_pos])
#             food_spawn_time = current_time
#         if current_time - poison_spawn_time > POISON_LIFETIME:
#             poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
#             poison_spawn_time = current_time

#           # Spawn power-up (only if none exists)
#         if powerup_pos is None:
#             if random.random() < POWERUP_CHANCE:
#                 powerup_type = random.choice([
#                     POWER_SPEED_UP,
#                     POWER_SLOW,
#                     POWER_SHIELD
#                 ])

#                 powerup_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos, poison_pos])
#                 powerup_spawn_time = pygame.time.get_ticks()

#         if powerup_pos and head == powerup_pos:
#             active_power = powerup_type
#             power_start_time = pygame.time.get_ticks()

#             if powerup_type == POWER_SHIELD:
#                 shield_active = True

#             powerup_pos = None
#             powerup_type = None  
        
#         if powerup_pos:
#             if current_time - powerup_spawn_time > POWERUP_LIFETIME:
#                 powerup_pos = None
#                 powerup_type = None
#         # Level update
#         LEVEL = SCORE // 5 + 1

#         if LEVEL != prev_level:
#             prev_level = LEVEL

#             if LEVEL >= 3:
#                 obstacle_count = LEVEL - 2

#                 obstacles = generate_obstacles(
#                     snake,
#                     obstacle_count,
#                     [food_pos, poison_pos]
#                 )

#     # ---------------------
#     # Rendering
#     # ---------------------
#     if not game_over:
#         screen.fill(LEVEL_COLORS.get(LEVEL, (0, 183, 235)))  # default to light blue if level exceeds defined colors

#         snake.draw(screen)
#         draw_grid(screen, WIDTH, HEIGHT, snake.size) # if SETTINGS_FILE.get("grid_overlay_status", True) else None
#         # Food color warning (last 1 sec)
#         current_time = pygame.time.get_ticks()
#         time_left = FOOD_LIFETIME - (current_time - food_spawn_time)

#         if time_left < 1000:
#             food_color = (255, 100, 100)
#         else:
#             food_color = (200, 0, 0)

#         pygame.draw.rect(
#             screen,
#             food_color,
#             (food_pos[0], food_pos[1], snake.size, snake.size)
#         )
#         pygame.draw.rect(
#             screen,
#             (120, 0, 0),  # dark red
#             (poison_pos[0], poison_pos[1], snake.size, snake.size)
#         )

#         if powerup_pos:
#             if powerup_type == POWER_SPEED_UP:
#                 color = (0, 0, 255)  # blue
#             elif powerup_type == POWER_SLOW:
#                 color = (255, 165, 0)  # orange
#             elif powerup_type == POWER_SHIELD:
#                 color = (200, 200, 200)  # gray

#             pygame.draw.rect(
#                 screen,
#                 color,
#                 (powerup_pos[0], powerup_pos[1], snake.size, snake.size)
#             )

#         if not obstacles_disabled:
#             for obs in obstacles:
#                 pygame.draw.rect(
#                     screen,
#                     (0, 0, 0),
#                     (obs[0], obs[1], snake.size, snake.size)
#                 )

#         # UI
#         score_text = font_small.render(f"Score: {SCORE}", True, (0, 0, 0))
#         level_text = font_small.render(f"Level: {LEVEL}", True, (0, 0, 0))
#         size_info = font_small.render(f"Snake size: {len(snake.body)}", True, (0, 0, 0))
#         if active_power:
#             if active_power != POWER_SHIELD:
#                 powerup_info = font_small.render(f"Power-up: {active_power} ({(5000 - (current_time - power_start_time)) // 1000}s)", True, (0, 0, 0))
#             else:
#                 powerup_info = font_small.render(f"Power-up: {active_power} (shield active)", True, (0, 0, 0))
#             screen.blit(powerup_info, (5, 65))

#         if respawn_freeze:
#             freeze_text = font_small.render(f"RECOVERING... ({(RESPAWN_DURATION - (current_time - respawn_start_time)) // 1000}s)", True, (0, 0, 0))
#             screen.blit(freeze_text, (5, 85))

#         screen.blit(score_text, (5, 5))
#         screen.blit(level_text, (5, 25))
#         screen.blit(size_info, (5, 45))
#     else:
#         game_over_scene()
#     # ---------------------
#     # Update
#     # ---------------------
#     pygame.display.flip()
#     base_speed = LEVEL_FPS.get(LEVEL, 20)
#     if active_power == POWER_SPEED_UP:
#         if current_time - power_start_time < 5000:
#             base_speed += 10
#         else:
#             active_power = None

#     elif active_power == POWER_SLOW:
#         if current_time - power_start_time < 5000:
#             base_speed -= 10
#         else:
#             active_power = None

#     clock.tick(max(5, base_speed))  # avoid freezing

def game_over_scene():
    screen.fill((200, 0, 0))
    screen.blit(game_over_text, (WIDTH//2 - 120, HEIGHT//2 - 50))
    score_display = font_big.render(f"Score: {SCORE}", True, (255, 255, 255))
    level_display = font_big.render(f"Level: {LEVEL}", True, (255, 255, 255))
    screen.blit(score_display, (180, 200))
    screen.blit(level_display, (180, 250))



# =========================
# Game loop
# =========================
running = True
game_over = False

# while running:
#     # ---------------------
#     # Events
#     # ---------------------
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP:
#                 snake.change_direction(0, -snake.size)
#             elif event.key == pygame.K_DOWN:
#                 snake.change_direction(0, snake.size)
#             elif event.key == pygame.K_LEFT:
#                 snake.change_direction(-snake.size, 0)
#             elif event.key == pygame.K_RIGHT:
#                 snake.change_direction(snake.size, 0)
#         # if event.type == print_userevent:
#         #     print("Obstacles:", obstacles)
        

while True:
    # Show main menu and get choice
    choice = show_main_menu()
    
    if choice == "play":
        # Get username before playing
        player_name = get_username()
        
        # Get personal best
        personal_best = get_personal_best(player_name)
        
        # Reapply difficulty settings
        apply_settings()
        
        # Reset game state
        snake = Snake()
        SCORE = 0
        LEVEL = 1
        game_over = False
        obstacles = []
        food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [])
        food_spawn_time = pygame.time.get_ticks()
        poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
        poison_spawn_time = pygame.time.get_ticks()
        powerup_pos = None
        powerup_type = None
        active_power = None
        shield_active = False
        
        # Game loop
        while not game_over:
            # ---------------------
            # Events
            # ---------------------
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_direction(0, -snake.size)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(0, snake.size)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(-snake.size, 0)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(snake.size, 0)
            if not game_over:
                current_time = pygame.time.get_ticks()
                if not respawn_freeze:
                    snake.move()

                head = snake.body[0]
                head_x, head_y = head

                # Wall collision
                collision = (
                    head_x < 0 or head_x >= WIDTH or
                    head_y < 0 or head_y >= HEIGHT or
                    head in snake.body[1:] or
                    head in obstacles
                )
                if collision:
                    if shield_active:
                        shield_active = False

                        reset_snake_safe(snake)

                        respawn_freeze = True
                        respawn_start_time = pygame.time.get_ticks()

                        powerup_type = None
                        active_power = None

                        # disable obstacles AFTER recovery
                        obstacles_disabled = True
                        obstacles_disabled_start = pygame.time.get_ticks()

                    else:
                        game_over = True

                if respawn_freeze:
                    if current_time - respawn_start_time < RESPAWN_DURATION:
                        # Skip movement
                        pass
                    else:
                        respawn_freeze = False

                if obstacles_disabled:
                    if current_time - obstacles_disabled_start > (RESPAWN_DURATION + OBSTACLE_DISABLE_DURATION):
                        obstacles_disabled = False

                        if LEVEL >= 3:
                            obstacles = generate_obstacles(
                                snake,
                                LEVEL - 2,
                                [food_pos, poison_pos]
                            )
                            obstacles_disabled = False

                # Food eaten
                if head == food_pos:
                    if game_settings["sound_enabled"] == True:
                        sound_eat.play()
                    snake.grow = True
                    food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [poison_pos])
                    food_spawn_time = pygame.time.get_ticks()

                    SCORE += random.randint(1, 3)
                    if game_settings.get("sound_enabled", True):
                        sound_eat.play()  # Play eat sound
                # Poison eaten
                if head == poison_pos:
                    if game_settings.get("sound_enabled", True):
                        sound_eat.play()
                    # shrink snake by 2
                    for _ in range(2):
                        if len(snake.body) > 1:
                            snake.body.pop()

                    # Check death condition
                    if len(snake.body) <= 1:
                        game_over = True

                    # Respawn poison
                    poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
                    poison_spawn_time = pygame.time.get_ticks()

                # Food expiration
                current_time = pygame.time.get_ticks()
                if current_time - food_spawn_time > FOOD_LIFETIME:
                    food_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [poison_pos])
                    food_spawn_time = current_time
                if current_time - poison_spawn_time > POISON_LIFETIME:
                    poison_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos])
                    poison_spawn_time = current_time

                # Spawn power-up (only if none exists)
                if powerup_pos is None:
                    if random.random() < POWERUP_CHANCE:
                        powerup_type = random.choice([
                            POWER_SPEED_UP,
                            POWER_SLOW,
                            POWER_SHIELD
                        ])

                        powerup_pos = generate_food(snake, WIDTH, HEIGHT, snake.size, [food_pos, poison_pos])
                        powerup_spawn_time = pygame.time.get_ticks()

                if powerup_pos and head == powerup_pos:
                    active_power = powerup_type
                    power_start_time = pygame.time.get_ticks()

                    if powerup_type == POWER_SHIELD:
                        shield_active = True

                    powerup_pos = None
                    powerup_type = None  
                
                if powerup_pos:
                    if current_time - powerup_spawn_time > POWERUP_LIFETIME:
                        powerup_pos = None
                        powerup_type = None
                # Level update
                LEVEL = SCORE // 5 + 1

                if LEVEL != prev_level:
                    prev_level = LEVEL

                    if LEVEL >= 3:
                        obstacle_count = LEVEL - 2

                        obstacles = generate_obstacles(
                            snake,
                            obstacle_count,
                            [food_pos, poison_pos]
                        )

            # ---------------------
            # Rendering
            # ---------------------
            if not game_over:
                screen.fill(LEVEL_COLORS.get(LEVEL, (0, 183, 235)))  # default to light blue if level exceeds defined colors

                snake.draw(screen)
                
                # Grid overlay - respect settings
                if game_settings.get("grid_overlay_status", True):
                    draw_grid(screen, WIDTH, HEIGHT, snake.size)
                # Food color warning (last 1 sec)
                current_time = pygame.time.get_ticks()
                time_left = FOOD_LIFETIME - (current_time - food_spawn_time)

                if time_left < 1000:
                    food_color = (255, 100, 100)
                else:
                    food_color = (200, 0, 0)

                pygame.draw.rect(
                    screen,
                    food_color,
                    (food_pos[0], food_pos[1], snake.size, snake.size)
                )
                pygame.draw.rect(
                    screen,
                    (120, 0, 0),  # dark red
                    (poison_pos[0], poison_pos[1], snake.size, snake.size)
                )

                if powerup_pos:
                    if powerup_type == POWER_SPEED_UP:
                        color = (0, 0, 255)  # blue
                    elif powerup_type == POWER_SLOW:
                        color = (255, 165, 0)  # orange
                    elif powerup_type == POWER_SHIELD:
                        color = (200, 200, 200)  # gray

                    pygame.draw.rect(
                        screen,
                        color,
                        (powerup_pos[0], powerup_pos[1], snake.size, snake.size)
                    )

                if not obstacles_disabled:
                    for obs in obstacles:
                        pygame.draw.rect(
                            screen,
                            (0, 0, 0),
                            (obs[0], obs[1], snake.size, snake.size)
                        )

                # UI
                score_text = font_small.render(f"Score: {SCORE}", True, (0, 0, 0))
                level_text = font_small.render(f"Level: {LEVEL}", True, (0, 0, 0))
                size_info = font_small.render(f"Snake size: {len(snake.body)}", True, (0, 0, 0))
                if active_power:
                    if active_power != POWER_SHIELD:
                        powerup_info = font_small.render(f"Power-up: {active_power} ({(5000 - (current_time - power_start_time)) // 1000}s)", True, (0, 0, 0))
                    else:
                        powerup_info = font_small.render(f"Power-up: {active_power} (shield active)", True, (0, 0, 0))
                    screen.blit(powerup_info, (5, 65))

                if respawn_freeze:
                    freeze_text = font_small.render(f"RECOVERING... ({(RESPAWN_DURATION - (current_time - respawn_start_time)) // 1000}s)", True, (0, 0, 0))
                    screen.blit(freeze_text, (5, 85))

                screen.blit(score_text, (5, 5))
                screen.blit(level_text, (5, 25))
                screen.blit(size_info, (5, 45))
            else:
                # Game over - show screen and then leaderboard
                result = show_game_over_screen(SCORE, LEVEL, personal_best)
                if result == "retry":
                    continue  # Restart the game loop
                elif result == "menu":
                    show_leaderboard(SCORE)
                    break  # Return to main menu
            # ---------------------
            # Update
            # ---------------------
            pygame.display.flip()
            base_speed = LEVEL_FPS.get(LEVEL, 20)
            if active_power == POWER_SPEED_UP:
                if current_time - power_start_time < 5000:
                    base_speed += 10
                else:
                    active_power = None

            elif active_power == POWER_SLOW:
                if current_time - power_start_time < 5000:
                    base_speed -= 10
                else:
                    active_power = None

            clock.tick(max(5, base_speed))  # avoid freezing
    elif choice == "leaderboard":
        show_standalone_leaderboard()  # Pass dummy score since we're just viewing
    elif choice == "settings":
        show_settings_screen()
    elif choice == "quit":
        pygame.quit()
        sys.exit()