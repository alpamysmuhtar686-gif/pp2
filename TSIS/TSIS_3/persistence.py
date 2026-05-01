# Leaderboard file
import json, os, pygame, sys
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