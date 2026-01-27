#Exercises

# ex 1
x = 5 # basic int type automatic variable declaration

# ex 2

# my-var = 7 <-- incorrect declaration
myTemporalVar = 7 # < -- Camel case
MyTemporalVar = 7 # < -- Pascal case
my_temporal_var = 7 # < -- Snake case

# ex 3: One value for multiple variables
a = b = c = 7
print(a, b, c, sep = " ")

# Declaring multiple variables in one row
a, b, c = 7, 9, 18 # <-- a corresponds to the first value 7, b to the second 9 and so on
print(a, b, c, sep = " ")


# ex 4
a = "Hello"
b = "Furina"
print(a + b) # < -- without spaces they will combine and slip. To fix we either put space to one of them, or use sep parameter

print(a, b, sep = " ")
print(a, b.replace("Furina", " Furina"))

# ex 5: Global and local variables

x = "Furina"

def praise_neuvilette():
    x = "Neuvilette" # < -- now its local
    print(x, " is great!")
praise_neuvilette()
print(x, " is great!") # expected Furina is great, because x = Neuvilette is inside a function

x = "Navia"

def praise_nahida():
    global x
    x = "Nahida" # Now Navia has been changed to Nahida because x is now global
    print(x, "is great")
praise_nahida()
print(x, "is great")




















# # ex 2, if the string can be declared both in single and double quota
# a = "John"
# b = 'John'
# print(a == b) # expected True

# # ex 3, variable names are case-sensitive and they behave independently between each other
# a = 5
# A = 5
# print (a == A)


# # ex 4, printing the type of a variable
# a = "Furina"
# b = 7
# c = True
# print(type(a)) # class str
# print(type(b)) # class int
# print(type(c)) # class bool

# # Try it yourself

# # 1: The variable type can change after its declaration
# a = "Furina"
# print(a, type(a), sep = " ") # Furina, class str
# a = 7
# print(a, type(a), sep = " ") # Now its 7, class int

# # 2: We can manually set a type for the variable like in C++. But the twist part is that it can be rechanged (not in all cases)
# a = 7
# b = str(7) # "7"
# c = float(7) # 7.0

# print(a, b, c, sep = "\n")