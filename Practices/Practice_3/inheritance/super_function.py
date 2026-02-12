# ex 1: inheriting parameters from parent class
class Person():
    def __init__(self, name):
        self.name = name

class Student(Person):
    def __init__(self, name):
        super().__init__(name) # inherits from parent class

# ex 2: add property

class Person_2():
    def __init__(self, name, sname):
        self.name = name
        self.sname = sname

class Student_2(Person_2):
    def __init__(self, name, sname):
        super().__init__(name, sname)
    graduation_date = 2019 # class variable

s1 = Student_2("Furina", "Focalors")
print(s1.name, s1.sname, s1.graduation_date, sep = " ")

# ex 3: redefine instance variable

class Person():
    def __init__(self, name, sname):
        self.name = name
        self.sname = sname

class Student(Person):
    def __init__(self, name, sname, graduation_year):
        super().__init__(name, sname)
        self.graduation_year = graduation_year
s1 = Student("a", "b", 2021)
print(s1.name, s1.sname, s1.graduation_year)