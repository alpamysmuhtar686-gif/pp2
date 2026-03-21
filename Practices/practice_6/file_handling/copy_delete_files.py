# ex 1: copy with stdIO (basic input/output)
with open("file1.txt", "r") as read_file:
    x = read_file.read()
with open("file2.txt", "w") as write_file:
    y = write_file.write(x)

z = open("file2.txt", "r").read()
print(f"file 1: {x}\nfile 2: {z}")

# ex 2: copy with shutil:
import shutil
shutil.copy("file1.txt", "file3.txt")
print(open("file3.txt", "r").read())

# ex 3: delete files with os
import os
os.remove("file3.txt")
print("File successfully deleted!")

# ex 4: preventing any error
try:
    os.remove("file3.txt")
except FileNotFoundError:
    print(f"FileNotFoundError: The file doesn't exist. Check for validity")