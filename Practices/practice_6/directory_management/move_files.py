# ex 1: move with shutil
import shutil, os
file1_dst = "C://Users/User/Desktop/Semester 2/pp2_spring/Practices/Practice_6/file_handling/file2.txt"
file = os.path.basename(file1_dst)
dst = os.getcwd()
shutil.move(file1_dst, dst)
try:
    with open("file2.txt", "r") as f:
        x = f.read()
    print(f"The file exists, content: {x}")
except FileNotFoundError:
    print(f"The file doesnt exist.")