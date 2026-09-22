class Order:
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity

    def total(self):
        return self.product.price * self.quantity


order = Order("Laptop", 2)

print(order.product)
print(order.quantity)
