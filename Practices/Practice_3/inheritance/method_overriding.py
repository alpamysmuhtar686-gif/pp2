# ex 1: create a base and a child class
class Person():
    def __init__(self, name):
        self.name = name
    
class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa
    
# ex 2: redefine classes again by adding method for the base class
class Person():
    def __init__(self, name):
        self.name = name
    def show(self):
        print(f"Name: {self.name}. Belongs to the class: Person")
    
class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa


s1 = Student("furina", 3.84)
s1.show() # one shows that s1 belongs to Student class, which, obviously inherited show method from the Person - base class

# ex 3: redefine the function with the same name, but with modified version - overriding

class Person():
    def __init__(self, name):
        self.name = name
    
class Student(Person):
    def __init__(self, name, gpa):
        super().__init__(name)
        self.gpa = gpa
    def show(self):
        print(f"Name: {self.name}, GPA: {self.gpa}. Belongs to the class: Student")

s2 = Student("Furina", 3.84)
s2.show() # one shows that this function has been overrided and indicates that the method is defined inside a child class