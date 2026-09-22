from repository import get_products

def show_products():
    for product in get_products():
        print(product["name"], product["price"])
