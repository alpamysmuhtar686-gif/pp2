# ex 1: a function with 1 argument (actually a parameter)
def my_function(fname):
  print(fname + " Refsnes")

my_function("Emil")
my_function("Tobias")
my_function("Linus")

# ex 2: Parameter vs Arguments
def praise_KBTU(name): # < -- this is a parameter
    print(f"KBTU is Great! by {name}") # final exam number 2

praise_KBTU("ItsukiLiquid") # < -- this is an argument

# ex 3: function must contain the same amount of arguments as its parameter - 2 parameters, then 2 arguments is mandatory
def my_function(fname, lname):
  print(fname + " " + lname)

my_function("Emil", "Refsnes") # my_function("Emil") causes an error

# ex 4: default value
def my_function(name = "friend"):
  print("Hello", name)

my_function("Emil")
my_function("Tobias")
my_function() # even though there is no argument, function takes "friend" as a default value
my_function("Linus")

# ex 5: keyword args
def my_function(animal, name):
  print("I have a", animal)
  print("My", animal + "'s name is", name)

my_function(animal = "dog", name = "Buddy")