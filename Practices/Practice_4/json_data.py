import json

# print the interface table appearance
print("=" * 80)
print(f"{"DN":50} {"Description":15} {"Speed":7} {"MTU":5}")
print("-" * 80)


# load the data from the external source (in the same directory as this file)

with open("simple-data(not-simple).json", "r") as json_file:
    parsed_data = json.load(json_file)


# take the necessary part: totalCount is not necessart
data = parsed_data["imdata"]

# now loop through this dictionary consisting ~ 400 l1Physlf files
count = 1
for part in data:
    if count <= 3:
        inner_data = part["l1PhysIf"]
        attr = inner_data["attributes"]
        dn = attr.get("dn", "") # if value is assigned for "dn" - get, otherwise None (empty space)
        description = attr.get("descr", "")
        speed = attr.get("speed", "")
        mtu = attr.get("mtu", "")

        print(f"{dn:50} {description:15} {speed:7} {mtu:5}")
        count += 1
    else:
        break


# for more general form, we can replace the loop top of this by the code below
# print("\n")
# for part in data:
#     inner_data = part["l1PhysIf"]
#     attr = inner_data["attributes"]
#     dn = attr.get("dn", "") # if value is assigned for "dn" - get, otherwise None (empty space)
#     description = attr.get("descr", "")
#     speed = attr.get("speed", "")
#     mtu = attr.get("mtu", "")

#     print(f"{dn:50} {description:15} {speed:7} {mtu:5}")