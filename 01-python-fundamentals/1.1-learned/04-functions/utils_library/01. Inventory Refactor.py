def check_stock(inventory, item):
    return inventory.get(item, "Item not found")


inventory = {
    "Pen": 20,
    "Book": 10,
    "Bag": 5
}

item = input("Enter item: ")

print("Stock:", check_stock(inventory, item))
