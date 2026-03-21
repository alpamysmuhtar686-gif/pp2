# ex 1: enumerate -> returns enumerate object with its index and value
l1 = [1, 4, 7, 10, 12]
x = list(enumerate(l1, start = 1)) # makes it as a list, assigning initial value = 1, so the indexation starts with 1
print(x)

# ex 2: zip
l2 = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "colombina"]
l3 = ["mondstat", "liyue", "inazuma", "sumeru", "fontaine", "natlan", "nod-krai"]
archon_region_list = list(zip(l2, l3)) # the value of the same index are assigned between two lists -> (venti, mondstat) etc.
print(*archon_region_list)
archons_dict = dict(archon_region_list)
print(archons_dict)

print(archons_dict["furina"])