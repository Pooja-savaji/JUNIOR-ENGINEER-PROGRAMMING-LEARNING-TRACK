numbers = [10, 20, 30, 40, 50]
search = int(input("Enter number: "))

found = False

for num in numbers:
    if num == search:
        found = True
        break

print("Found" if found else "Not Found")
