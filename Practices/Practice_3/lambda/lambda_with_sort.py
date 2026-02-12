# ex 1: sort with second element
students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

# ex 2: sort with lenght
archons = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "colombina"]
sorted_archons = sorted(archons, key = lambda x: len(x))
print(sorted_archons)