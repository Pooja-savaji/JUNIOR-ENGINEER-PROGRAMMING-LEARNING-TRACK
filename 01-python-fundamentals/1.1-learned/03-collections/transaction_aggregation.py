"""Transaction Aggregation and Financial Summaries in Python (Beginner Friendly).

Demonstrates:
- Filtering and aggregating financial records (Income vs Expense)
- Grouping by category and calculating percentage distributions
- Finding top spending areas, net cash flow, and generating ASCII summaries
"""

from typing import Dict, List


SAMPLE_TRANSACTIONS = [
    {"id": "TX101", "date": "2026-09-01", "type": "Income", "category": "Consulting", "amount": 3500.00, "note": "Client Project A"},
    {"id": "TX102", "date": "2026-09-02", "type": "Expense", "category": "Cloud Hosting", "amount": 120.00, "note": "AWS Monthly"},
    {"id": "TX103", "date": "2026-09-03", "type": "Expense", "category": "Software", "amount": 45.00, "note": "GitHub Copilot"},
    {"id": "TX104", "date": "2026-09-04", "type": "Income", "category": "Product Sales", "amount": 1200.00, "note": "Asset Tracker Licenses"},
    {"id": "TX105", "date": "2026-09-05", "type": "Expense", "category": "Office", "amount": 85.50, "note": "Coffee & Supplies"},
    {"id": "TX106", "date": "2026-09-06", "type": "Expense", "category": "Cloud Hosting", "amount": 80.00, "note": "Domain & SSL"},
    {"id": "TX107", "date": "2026-09-07", "type": "Income", "category": "Consulting", "amount": 2000.00, "note": "Client Project B"},
]


def calculate_totals(transactions: List[dict]) -> dict:
    """Calculate total income, total expenses, and net profit/balance."""
    total_income = sum(t["amount"] for t in transactions if t["type"].lower() == "income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"].lower() == "expense")
    net_balance = total_income - total_expenses

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "net_balance": round(net_balance, 2),
        "transaction_count": len(transactions),
    }


def aggregate_by_category(transactions: List[dict], transaction_type: str = "Expense") -> Dict[str, float]:
    """Aggregate total spending or earnings grouped by category."""
    category_totals = {}

    for t in transactions:
        if t["type"].lower() == transaction_type.lower():
            cat = t["category"]
            category_totals[cat] = category_totals.get(cat, 0.0) + t["amount"]

    # Sort categories by highest amount first
    sorted_categories = dict(sorted(category_totals.items(), key=lambda x: x[1], reverse=True))
    return sorted_categories


def display_transaction_report(transactions: List[dict]):
    """Print an easy-to-read financial summary report with ASCII distribution."""
    totals = calculate_totals(transactions)
    expense_breakdown = aggregate_by_category(transactions, "Expense")
    income_breakdown = aggregate_by_category(transactions, "Income")

    print("\n" + "=" * 55)
    print("           💰 FINANCIAL TRANSACTION REPORT        ")
    print("=" * 55)
    print(f"Total Transactions : {totals['transaction_count']}")
    print(f"Total Income (+)   : ${totals['total_income']:>12,.2f}")
    print(f"Total Expenses (-) : ${totals['total_expenses']:>12,.2f}")
    print("-" * 55)
    print(f"Net Balance        : ${totals['net_balance']:>12,.2f} {'(Profitable ✅)' if totals['net_balance'] >= 0 else '(Deficit ❌)'}")
    print("=" * 55)

    # Expense Breakdown
    print("\n📊 Expense Breakdown by Category:")
    print("-" * 55)
    total_exp = totals["total_expenses"]
    for cat, amt in expense_breakdown.items():
        pct = (amt / total_exp * 100) if total_exp > 0 else 0
        bar = "█" * int(pct // 5)
        print(f"  {cat:<16} | ${amt:>8.2f} | {pct:>5.1f}% | {bar}")
    print("-" * 55)

    # Income Breakdown
    print("\n📈 Income Sources:")
    print("-" * 55)
    for cat, amt in income_breakdown.items():
        print(f"  {cat:<16} | ${amt:>10,.2f}")
    print("-" * 55)


def run_demo():
    print("=" * 55)
    print("     📊 TRANSACTION AGGREGATION DEMO          ")
    print("=" * 55)

    # Display raw transactions table
    print("\nRaw Transaction Log:")
    print("-" * 65)
    print(f"{'ID':<7} | {'Date':<10} | {'Type':<8} | {'Category':<15} | {'Amount':>10}")
    print("-" * 65)
    for t in SAMPLE_TRANSACTIONS:
        sign = "+" if t["type"] == "Income" else "-"
        amt_str = f"{sign}${t['amount']:,.2f}"
        print(f"{t['id']:<7} | {t['date']:<10} | {t['type']:<8} | {t['category']:<15} | {amt_str:>10}")
    print("-" * 65)

    # Run aggregation
    display_transaction_report(SAMPLE_TRANSACTIONS)


if __name__ == "__main__":
    run_demo()
