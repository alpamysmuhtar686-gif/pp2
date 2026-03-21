# ex 1: basic open
f = open("read.txt", "r")
print(f.read())

# ex 2: open with specified directory
print()
f2 = open("C:/Users/n_malik/Desktop/semester 2/pp2_spring/Practices/Practice_6/file_handling/read.txt", "r")
print(f2.read())

# ex 3: opening with with
print()
with open("read.txt", "r") as f3: # it automatically closes the file, meaning there is no worry about whether its closed or not
    x = f3.read()
print(x)

# ex 4: manual closing the file
print()
f4 = open("read.txt", "r")
print(f4.read())
f4.close()
print("File f4 is closed!")

# ex 5: read only parts
print()
with open("read.txt", "r") as f5:
    y = f5.read(5) # reads 5 characters, but there is a space, that is need to be considered not to confuse with n-1 elements, so its "This ", not "This"
print(y)