# ex 1: appending text to the file
with open("write.txt", "a") as f1:
    f1.write("Now it has appended from the code")
x = open("write.txt", "r")
print(x.read())
x.close()


# ex 2: overwriting the whole text by using "w" flag
print()
with open("write.txt", "w") as f2:
    f2.write("Oops! Nothing is left except this expression")
x = open("write.txt", "r")
print(x.read())
x.close()

# ex 3: creating custom files
print()
y = open("new_file.txt", "x") # once the file created, further attempts will raise FileExistError.
x = open("new_file.txt", "a")
x.write("some sentence")
x.close()
z = open("new_file.txt", "r")
print(z.read())
y.close(); z.close()