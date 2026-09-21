"""Core business logic for tracking, calculating, and filtering expenses."""

from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple


VALID_CATEGORIES = [
    "Food & Dining",
    "Travel & Transport",
    "Hardware & Equipment",
    "Software & Subscriptions",
    "Office Supplies",
    "Utilities",
    "Miscellaneous",
]


class ExpenseTracker:
    """Manages an in-memory collection of expenses with persistence support."""

    def __init__(self, expenses: Optional[List[Dict[str, Any]]] = None) -> None:
        """Initialize the expense tracker.

        Args:
            expenses: Initial list of expense dicts.
        """
        self._expenses: List[Dict[str, Any]] = list(expenses) if expenses else []

    @property
    def expenses(self) -> List[Dict[str, Any]]:
        """Return a copy of the expenses list."""
        return list(self._expenses)

    def _get_next_id(self) -> int:
        """Calculate the next sequential unique integer ID."""
        if not self._expenses:
            return 1
        return max(exp.get("id", 0) for exp in self._expenses) + 1

    def add_expense(
        self,
        title: str,
        amount: float,
        category: str = "Miscellaneous",
        date_str: Optional[str] = None,
        notes: str = "",
    ) -> Dict[str, Any]:
        """Add a new validated expense entry.

        Args:
            title: Non-empty description of the expense.
            amount: Strictly positive monetary cost.
            category: Category name.
            date_str: ISO formatted date (YYYY-MM-DD) or None for today.
            notes: Optional additional notes.

        Returns:
            The created expense record dictionary.

        Raises:
            ValueError: If title is empty, amount <= 0, or date is invalid.
        """
        # Validate title
        clean_title = title.strip() if isinstance(title, str) else ""
        if not clean_title:
            raise ValueError("Expense title cannot be empty.")

        # Validate amount
        try:
            num_amount = round(float(amount), 2)
            if num_amount <= 0:
                raise ValueError("Amount must be strictly positive (> 0).")
        except (ValueError, TypeError) as err:
            raise ValueError(f"Invalid amount '{amount}': must be a positive number.") from err

        # Validate category
        clean_category = category.strip() if isinstance(category, str) else "Miscellaneous"
        if clean_category not in VALID_CATEGORIES:
            clean_category = "Miscellaneous"

        # Validate date
        if date_str:
            try:
                parsed_date = datetime.strptime(date_str.strip(), "%Y-%m-%d").date()
                formatted_date = parsed_date.strftime("%Y-%m-%d")
            except ValueError as err:
                raise ValueError(f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.") from err
        else:
            formatted_date = date.today().strftime("%Y-%m-%d")

        expense_record = {
            "id": self._get_next_id(),
            "title": clean_title,
            "amount": num_amount,
            "category": clean_category,
            "date": formatted_date,
            "notes": str(notes).strip(),
            "created_at": datetime.now().isoformat(),
        }

        self._expenses.append(expense_record)
        return expense_record

    def delete_expense(self, expense_id: int) -> bool:
        """Delete an expense record by its ID.

        Args:
            expense_id: The ID of the expense to remove.

        Returns:
            True if found and deleted, False otherwise.
        """
        initial_count = len(self._expenses)
        self._expenses = [e for e in self._expenses if e.get("id") != expense_id]
        return len(self._expenses) < initial_count

    def list_expenses(
        self,
        category: Optional[str] = None,
        sort_by: str = "date",
        reverse: bool = True,
    ) -> List[Dict[str, Any]]:
        """Retrieve and filter expense records.

        Args:
            category: Optional category filter.
            sort_by: Key to sort by ("date", "amount", "id", "title").
            reverse: Sort order (True for descending/newest first).

        Returns:
            List of matching expense dictionaries.
        """
        filtered = self._expenses
        if category and category != "All":
            filtered = [e for e in filtered if e.get("category", "").lower() == category.lower()]

        # Sort with safe default
        def sort_key(item: Dict[str, Any]) -> Any:
            val = item.get(sort_by, "")
            if sort_by == "amount":
                return float(val)
            return str(val)

        return sorted(filtered, key=sort_key, reverse=reverse)

    def calculate_total(self, category: Optional[str] = None) -> float:
        """Calculate the sum total of expenses, optionally filtered by category.

        Args:
            category: Optional category to filter before summing.

        Returns:
            Total amount as a rounded float.
        """
        items = self.list_expenses(category=category)
        return round(sum(item.get("amount", 0.0) for item in items), 2)

    def get_category_summary(self) -> List[Tuple[str, int, float, float]]:
        """Generate spending breakdown grouped by category.

        Returns:
            List of tuples: (category_name, count, total_amount, percentage_of_total).
        """
        total = self.calculate_total()
        categories: Dict[str, Dict[str, Any]] = {}

        for item in self._expenses:
            cat = item.get("category", "Miscellaneous")
            amt = item.get("amount", 0.0)
            if cat not in categories:
                categories[cat] = {"count": 0, "total": 0.0}
            categories[cat]["count"] += 1
            categories[cat]["total"] += amt

        summary = []
        for cat, data in sorted(categories.items(), key=lambda x: x[1]["total"], reverse=True):
            pct = (data["total"] / total * 100) if total > 0 else 0.0
            summary.append((cat, data["count"], round(data["total"], 2), round(pct, 1)))

        return summary
