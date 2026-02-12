# ex 1: simple class
class Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name) # emil
print(p1.age) # 36

# ex 2: using the class without initialization
class Person:
  pass

p1 = Person()
p1.name = "Tobias" # inefficient due to the manual writing
p1.age = 25

print(p1.name)
print(p1.age)

# ex 3: default values for a variable
class Person:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age

p1 = Person("Emil") # as the age emitting, class takes default value age = 15, so Emil is 18 years old
p2 = Person("Tobias", 25)

print(p1.name, p1.age)
print(p2.name, p2.age)

# ex 4: multiple parametres
class Person:
  def __init__(self, name, age, city, country):
    self.name = name
    self.age = age
    self.city = city
    self.country = country

p1 = Person("Linus", 30, "Oslo", "Norway")

print(p1.name)
print(p1.age)
print(p1.city)
print(p1.country)