def calculate_discount(price, discount):
    discount_amount = price * discount
    return price - discount_amount

price = 1000
discount = 20

print(calculate_discount(price, discount))

Bug: The discount is given as 20 instead of 0.20.
