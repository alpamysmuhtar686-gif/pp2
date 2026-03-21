# ex 1: readline, and readlines
with open("multiline.txt", "r") as mlf:
    while True:
        x = mlf.readline() # reads only 1 line: is similar to yield behaviour
        print(x)
        if not x: # EOF or newline
            break

# ex 2: readlines
print("="*50, "\n")
with open("multiline.txt", "r") as mlf2:
    y = mlf2.readlines() # returns a list of elements
print(*y, sep = "\n")