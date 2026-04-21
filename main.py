a = input().split()
b = {}
for i in a:
    if i not in b:
        b[i]=1
    else:
        b[i]+=1
for i,x in b.items():
    if x>1:
        print(f"{i}:{x}")
    