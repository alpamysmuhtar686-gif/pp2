# ex 1: basic class
class MyClass:
  x = 5

# ex 2: create an object
p1 = MyClass()
print(p1.x) # 5

# ex 3: deleting an object
del p1

# ex 4: multiple objects
p1 = MyClass()
p2 = MyClass()
p3 = MyClass()

print(p1.x)
print(p2.x)
print(p3.x)

# ex 5: pass statement
class Person:
  pass