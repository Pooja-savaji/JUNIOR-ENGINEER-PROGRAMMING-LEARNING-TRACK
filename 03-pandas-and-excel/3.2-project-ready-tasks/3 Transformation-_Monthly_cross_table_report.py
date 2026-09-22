import pandas as pd

sales = pd.DataFrame({
    "CustomerID": [1, 2, 1, 3, 2],
    "Month": ["Jan", "Jan", "Feb", "Feb", "Mar"],
    "Product": ["Laptop", "Mouse", "Laptop", "Keyboard", "Mouse"],
    "Quantity": [2, 5, 1, 2, 3],
    "Price": [50000, 1000, 50000, 2000, 1000]
})

customers = pd.DataFrame({
    "CustomerID": [1, 2, 3],
    "Name": ["Pooja", "Rahul", "Sneha"],
    "City": ["Pune", "Mumbai", "Nashik"]
})

sales["Total"] = sales["Quantity"] * sales["Price"]
monthly = sales.groupby("Month")["Total"].sum()
report = sales.merge(customers, on="CustomerID")

print("Monthly Summary:")
print(monthly)

print("\nCross-Table Report:")
print(report)
