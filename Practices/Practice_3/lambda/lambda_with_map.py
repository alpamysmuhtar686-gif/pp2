# ex 1: double all values
numbers = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, numbers))
print(doubled) # 2 4 6 8 10

# ex 2: triple all values
numbers = [1, 2, 3, 4, 5]
tripled = list(map(lambda x: x * 3, numbers))
print(tripled) # 3 6 9 12 15

# ex 3: absolute values of numbers

numbers = [-2, -1, 0, 1, 2]
absolute = list(map(lambda x: abs(x), numbers))
print(absolute) # 2 1 0 1 2

# ex 4: power of two

numbers = [-2, 1, 0, 1, 2]
powers = list(map(lambda x: x ** 2, numbers))
print(powers) # 4 1 0 1 4