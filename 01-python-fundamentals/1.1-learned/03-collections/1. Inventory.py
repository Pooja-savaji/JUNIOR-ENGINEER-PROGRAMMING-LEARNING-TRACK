inventory = {
    "Pen": 20,
    "Book": 10,
    "Bag": 5
}

item = input("Enter item: ")

if item in inventory:
    print("Stock:", inventory[item])
else:
    print("Item not found")
