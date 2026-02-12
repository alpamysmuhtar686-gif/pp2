# ex 1: basic return
def my_function(x, y):
  return x + y

result = my_function(5, 3)
print(result)

# ex 2: returning the extraordinary data types
def my_function():
  return ["apple", "banana", "cherry"] # function can return lists, and even dicts

fruits = my_function()
print(fruits[0])
print(fruits[1])
print(fruits[2])

# ex 3: restricting implemented arguments: only positional arguments can be implied
def my_function(name, /): # / comes after par.
  print("Hello", name)

my_function("Emil") # my_function(name = "Emil") < -- this is an error due to the (name, /) parameter in a function

# ex 4: inverse to the previous example: only keyword values can be permitted
def my_function(*, name): # * comes before par.
  print("Hello", name)

my_function(name = "Emil") # my_function("Emil") < -- this is an error due to the (*, name). Be careful in the order of writing key restrictions

# ex 5: combining restrictors
def my_function(a, b, /, *, c, d): # Arguments before / are positional-only, and arguments after * are keyword-only
  return a + b + c + d

result = my_function(5, 10, c = 15, d = 20)
print(result)