# ex 1: output boolean value in comparison
print(5 > 1) # True
print(5 < 1) # False
print(5 == 1) # False
print(5 != 1) # True

# ex 2: compare inside the declared values
a = 10
b = 7
print(a > b) # True
print(a != b) # False

# ex 3: compare distinct value types
a = "furina"
b = 5
try:
    print(a > b)
except TypeError:
    print("str and int cant be compared through > and < operators")
print(a != b) # but we can compare if they are equal

# ex 4: check for equality by comparing (strings)
a = "furina"
b = "neuvilette"
print(a == b) # False

# ex 5: compare if the stringified version of integer equal to the integer
a = "7"
b = 7
print(a == b) # False