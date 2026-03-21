# ex 1: os.makedir
import os, shutil
try:
    os.mkdir("folder1")
except FileExistsError:
    shutil.rmtree("folder1")
    os.mkdir("folder1")
    print("Folder1 has been re-initialized.")

# ex 2: make nested directories
os.makedirs("folder1/folder2/folder3", exist_ok = True)

# ex 3: os.chdir -> oper. system, change directory
path = ".."
os.chdir(path)
path = os.getcwd()
print(path)


# attempting to create a python file inside a .py to proceed the next task. It's completed once, because of flag "x" in opening otherwise raise FileExistsError

# os.mkdir("builtin_functions")
# os.chdir("builtin_functions")
# with open("map_filter_reduce.py", "x") as f:
#     f.writelines("n = int(input()) # is written from the external file directory_management/remained_functions, line 23")