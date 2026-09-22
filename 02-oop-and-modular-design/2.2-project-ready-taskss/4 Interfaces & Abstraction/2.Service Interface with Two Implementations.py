from abc import ABC, abstractmethod


class PaymentService(ABC):
    @abstractmethod
    def pay(self, amount):
        pass


class CardPayment(PaymentService):
    def pay(self, amount):
        return f"Card payment: {amount}"


class UPIPayment(PaymentService):
    def pay(self, amount):
        return f"UPI payment: {amount}"


print(CardPayment().pay(500))
print(UPIPayment().pay(500))
