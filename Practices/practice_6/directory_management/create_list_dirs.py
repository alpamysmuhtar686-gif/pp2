# ex 1: creating a list of all directories inside this directory
import os
path = "." # current path is denoted as '.' sign
dirs = [d for d in os.listdir(path) if os.path.isdir(d)]
if len(dirs) == 0: print("The current directory is empty")
else: print(*dirs)

# ex 2: the specified directory
print()
path = "C:/Users/User/Desktop/Semester 2/pp2_spring"
dirs = [d for d in os.listdir(path) if os.path.isdir(os.path.join(path, d))]
if len(dirs) == 0: print("The current directory is empty")
else: print(*dirs)