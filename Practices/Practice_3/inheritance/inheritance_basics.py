# ex 1: creating a base class
class Person:
  def __init__(self, fname, lname):
    self.firstname = fname
    self.lastname = lname

  def printname(self):
    print(self.firstname, self.lastname)

#Use the Person class to create an object, and then execute the printname method:

x = Person("John", "Doe")
x.printname()

# ex 2: create a child class
class Student(Person):
    def __init__(self, fname, lname):
       super().__init__(fname, lname)


# ex 3: create an object with parent class
x = Student("Mike", "Olsen")
x.printname()