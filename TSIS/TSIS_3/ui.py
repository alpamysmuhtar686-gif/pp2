import pygame, random, sys, time
from persistence import load_settings, save_settings, apply_settings, load_leaderboard, save_leaderboard
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

#Creating colors
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

#Setting up Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Default settings
default_settings = {
    "sound_enabled": True,
    "car_color": "red",
    "difficulty": "normal"
}

# Game settings (loaded from file)
game_settings = default_settings.copy()

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



# ==================== GAME SCENES ====================

def show_main_menu(DISPLAYSURF: pygame.Surface):
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

def show_settings_screen(DISPLAYSURF: pygame.Surface):
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
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

def show_game_over_screen(DISPLAYSURF: pygame.Surface, final_score, final_distance, final_coins):
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

def show_standalone_leaderboard(DISPLAYSURF: pygame.Surface):
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    return "menu"
    
    return "menu"
def show_leaderboard(DISPLAYSURF: pygame.Surface, final_score, player_name, distance_traveled):
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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if is_over_button((mx, my), back_x, back_y, button_width, button_height):
                    showing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    showing = False
    
    return False
# Color for leaderboard
YELLOW = (255, 255, 0)
#Create a white screen 
DISPLAYSURF = pygame.display.set_mode((400,600))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")