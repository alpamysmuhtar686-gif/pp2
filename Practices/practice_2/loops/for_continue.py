# ex 1: skip a value, or continue usage
archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "mualani"]
for archon in archons_list:
    if archon == "Mavuika":
        continue
    print(archon)


# ex 2: skip a value to avoid errors:
divison_values = [-5, -4, -3, -2, -1, 0, 1, 2, 3, 4, 5]
for i in divison_values:
    if i == 0:
        continue
    print(1 / i)