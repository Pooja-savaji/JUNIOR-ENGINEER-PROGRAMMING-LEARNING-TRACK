expenses = []
def add_expense(category, amount):
    if amount <= 0:
        return "Invalid amount"

    expenses.append({
        "category": category,
        "amount": amount
    })

    return "Expense added"

def total_expense():
    return sum(item["amount"] for item in expenses)

def category_summary():
    summary = {}

    for item in expenses:
        category = item["category"]
        summary[category] = summary.get(category, 0) + item["amount"]
    return summary
