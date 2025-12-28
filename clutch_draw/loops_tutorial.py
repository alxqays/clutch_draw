stuff = ["a", "b", "c"]

for item in stuff:
    print(item)

    if item != "b":
        print("Not b!")
        continue

    print("Found b!")
