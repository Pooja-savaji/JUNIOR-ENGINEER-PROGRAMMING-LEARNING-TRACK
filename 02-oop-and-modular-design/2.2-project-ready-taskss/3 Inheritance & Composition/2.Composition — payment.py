class Payment:
    def pay(self, amount):
        print("Paid:", amount)


class Order:
    def __init__(self, payment):
        self.payment = payment

    def checkout(self, amount):
        self.payment.pay(amount)


payment = Payment()
order = Order(payment)

order.checkout(500)
