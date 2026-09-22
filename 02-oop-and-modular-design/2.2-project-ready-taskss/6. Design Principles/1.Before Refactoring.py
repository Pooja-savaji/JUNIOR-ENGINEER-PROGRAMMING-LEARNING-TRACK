class Order:
    def __init__(self, items):
        self.items = items

    def calculate_total(self):
        total = 0
        for item in self.items:
            total += item["price"] * item["qty"]
        return total

    def save(self):
        print("Saving order to database...")

    def send_email(self):
        print("Sending order email...")
