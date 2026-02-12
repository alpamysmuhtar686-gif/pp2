# ex 1: basic lambda
x = lambda a : a + 10
print(x(5)) # 15

# ex 2: basic multiplication
x = lambda a, b : a * b
print(x(5, 6)) # 30

# ex 3: sum of 3 variables
x = lambda a, b, c : a + b + c
print(x(5, 6, 2)) # 13

# ex 4: complicated lambda
def myfunc(n):
  return lambda a : a * n

mytripler = myfunc(3)

print(mytripler(11)) # 33

