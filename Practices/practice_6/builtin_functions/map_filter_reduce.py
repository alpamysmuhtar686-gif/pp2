n = int(input()) # is written from the external file directory_management/remained_functions, line 23
# ex 1: map
a, b = map(int, input().split()) # aggregate and assign every element by mapping integer values
print(a, b)

# ex 2: filter
import random
random_numbers = [random.randint(1, 100) for _ in range(10)]
even_numbers = list(filter(lambda x: x % 2 == 0, random_numbers)) # filters the list by checking if the element is even, so function -> bool expected
print(*random_numbers)
print(*even_numbers)

# ex 3: reduce
import functools
x = [2, 3, 4, 5]
b = []
s = functools.reduce(lambda a, b: a * b, x, 12) # the initial value 12 is included as stack pushing
s2 = functools.reduce(lambda a, b: a + b, b, 10) # if the list is empty or unexpected behaviour, taken the initial value
print(s, s2, sep = "\n")