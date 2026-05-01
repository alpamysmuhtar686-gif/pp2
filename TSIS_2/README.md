Quick guide for direction:
1. Archive_files: need to be ignored, this is used when testing, so this is safe back versions in case of bugs or errors
2. images: saved canvas image from main.py is redirected to this folder as an images
3. main.py - main execution programm file
4. tools.py - tools, and a head class Painter(), which will be interacted in the main.py
5. archive_files/main_safe.py -> main.py file, which can be recovered if any error will be occured in the current main.py file (actually combined main.py + tools.py)