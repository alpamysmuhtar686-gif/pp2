Quick guide for direction:
1. Archive files: need to be ignored, this is used when testing, so this is safe back versions in case of bugs or errors
2. assets: needed files to load: background music, coin_take etc.
3. settings.json: settings for game to run
4. db.py - python file to execute queries to PostgreSQL
5. database.ini - database configuration
6. db_connection.log - logging connections and executions to sql server (need to be ignored)
7. game.py - game mechanics
8. config.py - use configurations to connect with DB
9. main.py - main executable program to play the game
10. archive_files/main_safe.py -> safe version if any error occurs (just a file with all codes combined from main.py + game.py)