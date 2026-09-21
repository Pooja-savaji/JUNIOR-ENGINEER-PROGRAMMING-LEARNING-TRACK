price = float(input("Enter price: "))
discount = float(input("Enter discount percentage: "))

discount_amount = price * discount / 100
final_price = price - discount_amount

print("Discount:", discount_amount)
print("Final Price:", final_price)
