# ex 1: basic general variable
class Dog:
    species = "Canis familiaris"   # ← class variable

# ex 2: class variable vs instance variable
class Dog:
    species = "Canis familiaris"   # class variable

    def __init__(self, name):
        self.name = name           # instance variable
d1 = Dog("Rex")
d2 = Dog("Buddy")
print(d1.name, d2.name, "\n", d1.species, d2.species)

# ex 3: student counter
class Student:
    count = 0   # class variable

    def __init__(self, name):
        self.name = name
        Student.count += 1
s1 = Student("Alice")
s2 = Student("Bob")

print(Student.count) # 2

# ex 4: common data
class Car:
    wheels = 4

c1 = Car()
c2 = Car()

Car.wheels = 6

print(c1.wheels, c2.wheels) # now both of them is 6

c1.wheels = 8

print(c1.wheels, c2.wheels) # now c1 - 8, c2 - still a