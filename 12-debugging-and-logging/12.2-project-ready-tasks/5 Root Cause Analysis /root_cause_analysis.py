# 15.5 Root Cause Analysis

# Defect 1: Division by Zero
def calculate_average(total, count):
    return total / count
print(calculate_average(100, 0))

# Defect 2: Wrong Calculation
def calculate_total(price, quantity):
    return price + quantity
print(calculate_total(100, 2))

# Defect 3: Missing Dictionary Key
user = {
    "name": "Pooja"
}
print(user["email"])


# Defect 4: Empty List
numbers = []
print(numbers[0])


# Defect 5: Invalid User Input
age = "twenty"
print(int(age))
