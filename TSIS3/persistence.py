import json
import os

def load_scores():
    if os.path.exists("leaderboard.json"):
        with open("leaderboard.json", "r") as file:
            return json.load(file)
    return []

def save_score(name, score, coins):
    data = load_scores()

    data.append({
        "name": name,
        "score": score,
        "coins": coins
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open("leaderboard.json", "w") as file:
        json.dump(data, file)

def load_settings():
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as file:
            return json.load(file)

    return {
        "sound": True,
        "car_color": "Blue",
        "difficulty": "Normal"
    }

def save_settings(settings):
    with open("settings.json", "w") as file:
        json.dump(settings, file)