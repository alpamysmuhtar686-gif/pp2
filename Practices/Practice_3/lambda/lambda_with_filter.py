# ex 1: output only odd numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8]
odd_numbers = list(filter(lambda x: x % 2 != 0, numbers))
print(odd_numbers)

# ex 2: output only even numbers
numbers = [1, 2, 3, 4, 5]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)

# ex 3: output numbers in odd positions
numbers = [1, 2, 3, 4, 5, 6, 7]
odd_pos_numbers = list(filter(lambda x: numbers.index(x) % 2 == 0, numbers))
print(odd_pos_numbers)

# ex 4: output only prime numbers
def isPrime(a):
    result = True
    if a == 1 or a == 0:
        pass
    for i in range(2, a):
        if a % i == 0:
            result = False
            return result
    return result
numbers = [1, 2, 3, 4, 5, 6, 7]
prime_numbers = list(filter(lambda x: isPrime(x), numbers))
print(prime_numbers)