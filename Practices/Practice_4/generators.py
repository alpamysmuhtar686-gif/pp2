n = int(input()) # universal for all exercies

# ex 1:

gen = (i ** 2 for i in range(n))

# ex 2
def yield_evens(n):
    init_val = 0
    while init_val <= n:
        if init_val % 2 == 0:
            yield init_val
        init_val += 1

gen_2 = yield_evens(n)
print("# ex 2 output: ")
first = True
for num in gen_2:
    if first:
        print(num, end = "")
        first = False
    else:
        print(f",{num}", end = "")

# ex 3
def generate_divisors(n: int):
    init_val = 0
    while init_val <= n:
        if init_val % 3 == 0 and init_val % 4 == 0:
            yield init_val
        init_val += 1

divident_list = generate_divisors(n)
first = True
print("\n# ex 3 outputs: ")
for number in divident_list:
    if first:
        print(number, end = "")
        first = False
    else:
        print(f", {number}", end = "")


# ex 4
print("\n# ex 4 outputs")
a, b = map(int, input().split())

def squares(a: int, b: int):
    init_val = a
    while init_val <= b:
        yield init_val ** 2
        init_val +=1

square = squares(a, b)
for number in square:
    print(number, end = " ")

# ex 5
print("\n # ex 5 outputs")

def reducing_generator(n: int):
    init_val = n
    while init_val >= 0:
        yield init_val
        init_val -= 1

final_gen = reducing_generator(n)

print(*final_gen)