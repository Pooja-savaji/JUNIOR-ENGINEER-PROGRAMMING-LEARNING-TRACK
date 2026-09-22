from src.order import Order
class OrderService:
    def __init__(self, repository):
        self.repository = repository

    def create_order(self, order_id, customer, amount):
        order = Order(order_id, customer, amount)
        self.repository.save(order)
        return order

    def cancel_order(self, order_id):
        order = self.repository.get(order_id)

        if not order:
            raise ValueError("Order not found")

        order.status = "Cancelled"
        return order
