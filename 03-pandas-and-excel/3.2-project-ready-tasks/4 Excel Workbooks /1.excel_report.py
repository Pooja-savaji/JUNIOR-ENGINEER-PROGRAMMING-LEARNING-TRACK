import pandas as pd

sales = pd.DataFrame({
    "Product": ["Laptop", "Mouse", "Keyboard"],
    "Quantity": [2, 5, 3],
    "Price": [50000, 1000, 2000]
})

sales["Total"] = sales["Quantity"] * sales["Price"]

summary = pd.DataFrame({
    "Total Sales": [sales["Total"].sum()],
    "Total Quantity": [sales["Quantity"].sum()]
})

with pd.ExcelWriter("sales_report.xlsx", engine="openpyxl") as writer:
    sales.to_excel(writer, sheet_name="Sales", index=False)
    summary.to_excel(writer, sheet_name="Summary", index=False)

print("Excel report created successfully!")
