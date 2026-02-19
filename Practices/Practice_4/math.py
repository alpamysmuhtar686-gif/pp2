import math
# ex 1:
degree = int(input("Input degree: "))
print(f"Output radian: {math.radians(degree):.6f}") # in example degree = 15, the error is 0.000095 -> 9,5 * 10^-5


# ex 2
def area(height: int, base_1: int, base_2: int) -> float:
    return (base_1 + base_2) * height / 2

height = int(input("Height: "))
b1 = int(input("Base, first value: "))
b2 = int(input("Base, second value: "))

print(f"Expected output: {area(height, b1, b2)}")

# ex 3

def area_for_regular_polygon(size_n: int, size_len: int):
    return (size_n * size_len ** 2) / (4 * math.tan(math.pi / size_n))
n = int(input("Input number of sides: "))
a = int(input("Input the length of a side: "))

result = area_for_regular_polygon(n, a)
print(f"The area of the polygon is: {result:.0f}")

# ex 4
l = int(input("Length of base: "))
h = int(input("Height of parallelogram: "))
print(f"Expected output: {l * h}")