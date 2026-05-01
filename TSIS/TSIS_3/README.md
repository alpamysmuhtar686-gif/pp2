Quick guide for direction:
1. Archive files: need to be ignored, this is used when testing, so this is safe back versions in case of bugs or errors
2. assets: needed files to load: background music, coin_take etc.
3. settings.json: settings for game to run
4. leaderboard.json - leaderboard for racer game.
5. archive_files/Game_safe - a safe working version of game in case main.py will be fallen (all codes among ui.py, persistence.py, racer.py in once place)
6. persistence.py - .py file that works with JSON, implement import/export settings, and leaderboards
7. racer.py - main game mechanics
8. ui.py - transitive scenes and button styles
9. main.py - main executing file collecting and working by importing files above