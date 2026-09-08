"""
validation_utils.py
===================
Input-validation helpers extracted from validators.py and menu_loops.py.
"""

import re


def is_non_empty_string(value: str) -> bool:
    """Return True if *value* is a non-empty, non-whitespace string."""
    return isinstance(value, str) and bool(value.strip())


def is_positive_number(value) -> bool:
    """Return True if *value* can be converted to a positive float."""
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_valid_email(email: str) -> bool:
    """Return True if *email* matches a basic e-mail pattern."""
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email.strip()))


def is_valid_asset_tag(tag: str) -> bool:
    """Return True if *tag* follows the asset-tag pattern: 2-4 uppercase letters
    followed by a hyphen and 4-8 digits (e.g. ASSET-1234, IT-00042)."""
    pattern = r"^[A-Z]{2,4}-\d{4,8}$"
    return bool(re.match(pattern, tag.strip()))
