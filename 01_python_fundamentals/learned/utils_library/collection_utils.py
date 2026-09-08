"""
collection_utils.py
===================
List search, filter, and deduplication helpers extracted from
search_filter_problems.py and number_analysis.py.
"""


def linear_search(items: list, target) -> int:
    """Return the first index of *target* in *items*, or -1 if not found.

    Works on any list (strings, numbers, dicts, …).
    """
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1


def binary_search(sorted_items: list, target) -> int:
    """Return the index of *target* in a sorted list, or -1 if not found.

    Uses iterative binary search — O(log n).
    """
    low, high = 0, len(sorted_items) - 1
    while low <= high:
        mid = (low + high) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def filter_by_range(numbers: list, min_val: float, max_val: float) -> list:
    """Return elements from *numbers* that fall within [min_val, max_val]."""
    return [n for n in numbers if min_val <= n <= max_val]


def find_duplicates(items: list) -> list:
    """Return a sorted list of values that appear more than once in *items*."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        seen.add(item)
    return sorted(duplicates)
