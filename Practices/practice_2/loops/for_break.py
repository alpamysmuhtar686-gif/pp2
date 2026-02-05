# ex 1: break the loop when the condition is met
archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "mualani"]
for archon in archons_list:
    print(archon)
    if (archon == "Furina"):
        break


# ex 2: break the loop but not inclusively
archons_list = ["venti", "zhongli", "raiden", "nahida", "furina", "mavuika", "mualani"]
for archon in archons_list:
    if archon == "Mavuika": # 1 step after
        break
    print(archon)