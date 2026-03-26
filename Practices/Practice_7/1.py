result = ""
with open("C:/Users/User/Downloads/XenForo Users 2026-03-17.csv", "r", encoding = "UTF-8") as f:
    while True:
        x = f.readline()
        if not x:
            break
        print(x)

print("\n", "Program ended succesfully")