# ex 1: initialize 2 base and 1 child classes
class Person():
    def __init__(self, name):
        self.name = name
    def show(self):
        print(f"Person: {self.name}")

class Employee():
    def __init__(self, name, isEmployee):
        self.isEmployee = isEmployee
        self.name = name
    def is_hired(self):
        print(f"{self.name} is an employee" if self.isEmployee == True else f"{self.name} is not an employee")

class Student(Person, Employee):
    def __init__(self, name, isEmployee):
        Person.__init__(self, name)
        Employee.__init__(self, name, isEmployee)

name = "furina"
s1 = Student(name, True)
s1.show()
s1.is_hired()


# ex 2: another example to pin the knowledge

class Meta():
    def __init__(self, name, meta_coefficent):
        self.name = name
        self.meta_coefficent = meta_coefficent
    def check_necessiity(self):
        print(f"{self.name} is totally in meta." if self.meta_coefficent >= 8.5 else f"The character {self.name} is actually weaker. Would you like to choose another character?")
    
class Archont():
    def __init__(self, name, isArchont = False):
        self.name = name
        self.isArchont = isArchont
    def check_ifArchont(self, archons_list):
        if self.name.lower() in archons_list:
            self.isArchont = True
            print(f"A character {self.name} has succesfully denoted as an Archont!")
        else: 
            pass
    def show_info(self):
        print(f"A character {self.name} is an Archont" if self.isArchont == True else f"A character {self.name} is not an Archont.")
    
class Character(Meta, Archont):
    def __init__(self, name, meta_coefficent):
        Meta.__init__(self, name, meta_coefficent)
        Archont.__init__(self, name, isArchont = False)


archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "colombina"]
c1 = Character("furina", 9.5)
c1.check_necessiity()
c1.show_info()
c1.check_ifArchont(archons_list)
c1.show_info()