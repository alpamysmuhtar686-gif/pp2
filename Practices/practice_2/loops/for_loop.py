# ex 1: print values in a list by looping
archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "mualani"]
for archon in archons_list:
    print(archon)

# ex 2: looping through a string
archon = "Furina"
for letter in archon:
    print(letter) # class <'char'>

# ex 3: looping with a range
for x in range(6):
    print(x)

# ex 4: nested loops
a = [1, 2, 3]
b = [4, 5, 6]
for i in a:
    for j in b:
        print(f"({i, j})")

# ex 5: pass
archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "mualani"]
for archon in archons_list:
    pass

