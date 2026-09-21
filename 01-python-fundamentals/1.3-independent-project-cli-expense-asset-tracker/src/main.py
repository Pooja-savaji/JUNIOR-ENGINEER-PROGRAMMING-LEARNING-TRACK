"""Command-Line Interface (CLI) for the Day 1 Expense Tracker."""

import sys
from datetime import date
from typing import Optional

from storage import DEFAULT_DATA_FILE, load_expenses, save_expenses
from tracker import VALID_CATEGORIES, ExpenseTracker


def print_banner():
    print("=" * 60)
    print("       💰 CLI EXPENSE TRACKER (Day 1 Independent)        ")
    print("=" * 60)


def format_currency(amount: float) -> str:
    """Format a number into currency string with comma separators."""
    if amount < 0:
        return f"-${abs(amount):,.2f}"
    return f"${amount:,.2f}"


def display_table(expenses: list):
    """Display expenses in an aligned ASCII table."""
    if not expenses:
        print("\n[Info] No expenses recorded yet.")
        return

    print("\n" + "-" * 75)
    print(f"{'ID':<5} | {'Date':<10} | {'Category':<24} | {'Amount':>10} | {'Title'}")
    print("-" * 75)
    for exp in expenses:
        exp_id = exp.get("id", 0)
        exp_date = exp.get("date", "")
        exp_cat = exp.get("category", "")[:24]
        exp_amt = format_currency(exp.get("amount", 0.0))
        exp_title = exp.get("title", "")[:24]
        print(f"{exp_id:<5} | {exp_date:<10} | {exp_cat:<24} | {exp_amt:>10} | {exp_title}")
    print("-" * 75)


def prompt_add_expense(tracker: ExpenseTracker):
    """Interactive prompt to add a new expense."""
    print("\n--- Add New Expense ---")

    # Title
    while True:
        title = input("Description / Title: ").strip()
        if title:
            break
        print("[Error] Title cannot be empty. Please enter a description.")

    # Amount
    while True:
        amount_raw = input("Amount ($): ").strip().replace("$", "").replace(",", "")
        try:
            amount = float(amount_raw)
            if amount <= 0:
                print("[Error] Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("[Error] Invalid numeric amount. Please enter a valid number (e.g. 19.99).")

    # Category selection
    print("\nSelect Category:")
    for idx, cat in enumerate(VALID_CATEGORIES, start=1):
        print(f"  {idx}. {cat}")
    
    cat_choice = input(f"Choice (1-{len(VALID_CATEGORIES)}, default 1): ").strip()
    try:
        cat_idx = int(cat_choice) - 1
        if 0 <= cat_idx < len(VALID_CATEGORIES):
            category = VALID_CATEGORIES[cat_idx]
        else:
            category = VALID_CATEGORIES[0]
    except ValueError:
        category = VALID_CATEGORIES[0]

    # Date
    today_str = date.today().strftime("%Y-%m-%d")
    date_input = input(f"Date (YYYY-MM-DD, default '{today_str}'): ").strip()
    date_val = date_input if date_input else today_str

    # Optional notes
    notes = input("Optional notes: ").strip()

    try:
        created = tracker.add_expense(
            title=title,
            amount=amount,
            category=category,
            date_str=date_val,
            notes=notes,
        )
        print(f"\n[Success] Added expense #{created['id']}: {created['title']} ({format_currency(created['amount'])})")
    except ValueError as err:
        print(f"\n[Error] Failed to add expense: {err}")


def display_summary(tracker: ExpenseTracker):
    """Show grand total and category breakdown."""
    total = tracker.calculate_total()
    summary = tracker.get_category_summary()
    count = len(tracker.expenses)

    print("\n" + "=" * 50)
    print("             EXPENSE SUMMARY")
    print("=" * 50)
    print(f"Total Transactions: {count}")
    print(f"Grand Total Spent : {format_currency(total)}")
    print("-" * 50)
    if summary:
        print(f"{'Category':<26} | {'Count':<5} | {'Total':>10} | {'Share'}")
        print("-" * 50)
        for cat, c_count, c_tot, pct in summary:
            print(f"{cat:<26} | {c_count:<5} | {format_currency(c_tot):>10} | {pct:>5.1f}%")
        print("-" * 50)
    else:
        print("No expenses to summarize.")


def prompt_delete(tracker: ExpenseTracker):
    """Prompt user to delete an expense by ID."""
    print("\n--- Delete Expense ---")
    id_raw = input("Enter Expense ID to delete: ").strip()
    try:
        exp_id = int(id_raw)
        if tracker.delete_expense(exp_id):
            print(f"[Success] Expense #{exp_id} removed.")
        else:
            print(f"[Error] Expense with ID #{exp_id} not found.")
    except ValueError:
        print("[Error] Please enter a valid numeric ID.")


def interactive_menu():
    """Main interactive loop."""
    expenses_data = load_expenses()
    tracker = ExpenseTracker(expenses_data)

    print_banner()

    while True:
        print("\nMain Menu:")
        print("  1. 📝 Add Expense")
        print("  2. 📋 List All Expenses")
        print("  3. 📊 View Total & Category Breakdown")
        print("  4. 🔍 Filter by Category")
        print("  5. ❌ Delete an Expense")
        print("  6. 💾 Save & Exit")

        choice = input("\nEnter choice (1-6): ").strip()

        if choice == "1":
            prompt_add_expense(tracker)
            save_expenses(tracker.expenses)
        elif choice == "2":
            display_table(tracker.list_expenses())
        elif choice == "3":
            display_summary(tracker)
        elif choice == "4":
            print("\nSelect Category to Filter:")
            for idx, cat in enumerate(VALID_CATEGORIES, start=1):
                print(f"  {idx}. {cat}")
            cat_choice = input(f"Choice (1-{len(VALID_CATEGORIES)}): ").strip()
            try:
                cat_idx = int(cat_choice) - 1
                if 0 <= cat_idx < len(VALID_CATEGORIES):
                    selected_cat = VALID_CATEGORIES[cat_idx]
                    filtered = tracker.list_expenses(category=selected_cat)
                    display_table(filtered)
                    print(f"Category Total ({selected_cat}): {format_currency(tracker.calculate_total(selected_cat))}")
                else:
                    print("[Error] Invalid choice.")
            except ValueError:
                print("[Error] Please enter a valid number.")
        elif choice == "5":
            display_table(tracker.list_expenses())
            prompt_delete(tracker)
            save_expenses(tracker.expenses)
        elif choice == "6":
            save_expenses(tracker.expenses)
            print("\n[Saved] All data saved. Goodbye! 👋\n")
            break
        else:
            print("[Error] Invalid choice. Please enter a number between 1 and 6.")


def main():
    # Basic CLI arg support (e.g. `python main.py --summary`)
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        tracker = ExpenseTracker(load_expenses())
        if arg in ("--list", "-l", "list"):
            display_table(tracker.list_expenses())
        elif arg in ("--summary", "-s", "summary", "total"):
            display_summary(tracker)
        else:
            print(f"Usage: python main.py [list | summary]")
    else:
        interactive_menu()


if __name__ == "__main__":
    main()
