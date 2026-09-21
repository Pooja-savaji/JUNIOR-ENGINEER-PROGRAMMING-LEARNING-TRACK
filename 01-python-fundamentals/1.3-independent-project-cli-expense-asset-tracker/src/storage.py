"""Storage engine for persisting expenses using pure Python standard library."""

import json
import os
from typing import Any, Dict, List

DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), "expenses.json")


def load_expenses(filepath: str = DEFAULT_DATA_FILE) -> List[Dict[str, Any]]:
    """Load expense records from a JSON file.

    Handles edge cases like missing files, empty files, or corrupted JSON.

    Args:
        filepath: Path to the JSON data file.

    Returns:
        List of expense dictionaries.
    """
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return []
            data = json.loads(content)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError) as err:
        print(f"[Warning] Could not read data file '{filepath}': {err}. Starting with empty list.")
        return []


def save_expenses(expenses: List[Dict[str, Any]], filepath: str = DEFAULT_DATA_FILE) -> bool:
    """Save expense records to a JSON file.

    Args:
        expenses: List of expense dictionaries to persist.
        filepath: Path to the target JSON file.

    Returns:
        True if save was successful, False otherwise.
    """
    try:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(expenses, f, indent=2)
        return True
    except OSError as err:
        print(f"[Error] Failed to save expenses to '{filepath}': {err}")
        return False
