status = True
candidates_list = []
while status:
    name, server_name, server_id = map(str, input().split())
    candidates_list.append([name, server_name, server_id])
    if name == "stop":
        status = False
        break
for i in range(len(candidates_list)):
    candidates_list[i][2] = int(candidates_list[i][2])
# sorted_candidates = sorted(candidates_list, key = server_id)
print(*candidates_list, sep = "\n")

def is_even(number) -> bool: return number % 2 == 0
for info in candidates_list:
    print(info) if is_even(info[2]) else None