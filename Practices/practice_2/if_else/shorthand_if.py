# ex 1: printing a value in one line
a = 5
b = 2
if a > b: print("a is greater than b")

# ex 2: print a value in one line using if / else
a = 67
b = 16
print("a > b" if a > b else "a <= b")

# ex 3: another way to print
a = 67
b = 16
print("a > b") if a > b else print("a <= b")

# ex 4: declare a value in one line
a = 67
b = 1488
bigger = a if a > b else b
print(f"Bigger is: {bigger}")

# ex 5: multiple case-scenario
a = 67
b = 67
print("a > b") if a > b else print("a == b") if a == b else print("a < b")