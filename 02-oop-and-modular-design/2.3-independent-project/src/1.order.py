class Order:
    def __init__(self, order_id, customer, amount):
        if not customer:
            raise ValueError("Customer is required")

        if amount <= 0:
            raise ValueError("Amount must be greater than 0")

        self.order_id = order_id
        self.customer = customer
        self.amount = amount
        self.status = "Pending"
