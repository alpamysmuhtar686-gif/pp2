# ex 1: basic while
i = 1
while i <= 7:
    print(i)
    i += 1 # its important to increment/decrement the value or make a breakout in order to avoid endless loops

# ex 2: while decrement
i = 7
while i >= 0:
    print(i)
    i -= 1

# ex 3: else statement when loop stops
i = 1
while i < 6:
    print(i)
    i += 1
else:
    print("i is no longer less than 6")