# ex 1: basic else
a = 1
b = 2
if a > b:
    print("True")
elif a == b:
    print("Equal")
else:
    print("False")

# ex 2: else without elif
a = 7
b = 9
if a > b:
    print("Greater")
else:
    print("Less")

# ex 3: else is the final chain - no elif allowed after it

# this will cause a syntax error

# if a > b:
#     print("True")
# else:
#     print("False")
# elif a == b:
#     print("Equal")

# ex 4: multi-case chain
temperature = 22

if temperature > 30:
    print("It's hot outside!")
elif temperature > 20:
    print("It's warm outside")
elif temperature > 10:
    print("It's cool outside")
else:
    print("It's cold outside!")

# ex 5: else as a fallback

username = "Itsuki"
if len(username) > 0:
    print(f"Welcome, {username}!")
else:
    print("Error: Username cannot be empty")