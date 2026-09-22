class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price


product = Product("Laptop", 50000)

print(product.name)
print(product.price)
