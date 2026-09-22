class Invoice:
    def __init__(self, customer, amount):
        self.customer = customer
        self.amount = amount

    def show(self):
        print("Customer:", self.customer)
        print("Amount:", self.amount)


invoice = Invoice("Pooja", 100000)
invoice.show()
