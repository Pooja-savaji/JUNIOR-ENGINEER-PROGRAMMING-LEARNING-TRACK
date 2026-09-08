"""
stats_utils.py
==============
Statistics and aggregation helpers extracted from grade_calculator.py
and transaction_aggregation.py.
"""

from collections import Counter


def mean(numbers: list) -> float:
    """Return the arithmetic mean of *numbers*. Returns 0 for empty lists."""
    if not numbers:
        return 0.0
    return sum(numbers) / len(numbers)


def median(numbers: list) -> float:
    """Return the median of *numbers*. Returns 0 for empty lists."""
    if not numbers:
        return 0.0
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2
    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return float(sorted_nums[mid])


def mode(numbers: list):
    """Return the most common value in *numbers*, or None for empty lists."""
    if not numbers:
        return None
    counts = Counter(numbers)
    return counts.most_common(1)[0][0]


def compute_statistics(numbers: list) -> dict:
    """Return a dict with mean, median, mode, min, max, and total.

    Keys: mean, median, mode, min, max, total, count
    """
    if not numbers:
        return {"mean": 0, "median": 0, "mode": None,
                "min": 0, "max": 0, "total": 0, "count": 0}
    return {
        "mean":   round(mean(numbers), 2),
        "median": median(numbers),
        "mode":   mode(numbers),
        "min":    min(numbers),
        "max":    max(numbers),
        "total":  sum(numbers),
        "count":  len(numbers),
    }


def aggregate_by_category(records: list, category_key: str,
                           value_key: str) -> dict:
    """Sum *value_key* per unique value of *category_key* across *records*.

    Each record is a dict, e.g. {"category": "food", "amount": 12.5}.
    Returns {"food": 12.5, ...}.
    """
    result: dict = {}
    for record in records:
        cat = record.get(category_key, "unknown")
        val = record.get(value_key, 0)
        result[cat] = result.get(cat, 0) + val
    return result
