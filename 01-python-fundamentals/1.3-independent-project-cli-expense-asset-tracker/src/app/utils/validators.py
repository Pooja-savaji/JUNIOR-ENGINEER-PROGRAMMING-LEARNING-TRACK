"""Validation utilities for the Asset Tracker application.

Provides standalone validation helper functions for asset tags, emails,
strings, and numeric inputs using pure Python without external libraries.
"""

import re
from typing import Any, Optional


def is_non_empty_string(value: Any) -> bool:
    """Check if the provided value is a non-empty string.

    Args:
        value: Any Python object to test.

    Returns:
        True if value is an instance of str and contains non-whitespace characters;
        False otherwise (including None, numbers, collections, or empty/whitespace strings).

    Examples:
        >>> is_non_empty_string("Laptop")
        True
        >>> is_non_empty_string("   ")
        False
        >>> is_non_empty_string(None)
        False
    """
    if not isinstance(value, str):
        return False
    return bool(value.strip())


def is_valid_asset_tag(
    tag: str,
    expected_prefix: Optional[str] = None,
) -> bool:
    """Validate whether a string adheres to the standard asset tag pattern.

    Standard pattern:
    - 2 to 6 uppercase letters prefix
    - Hyphen separator '-'
    - 3 to 8 numeric digits

    Args:
        tag: The asset tag string to validate.
        expected_prefix: Optional prefix string to enforce (case-insensitive).

    Returns:
        True if the asset tag is valid; False otherwise.

    Examples:
        >>> is_valid_asset_tag("AST-000123")
        True
        >>> is_valid_asset_tag("SRV-000001", expected_prefix="SRV")
        True
        >>> is_valid_asset_tag("INVALID_TAG")
        False
    """
    if not is_non_empty_string(tag):
        return False

    clean_tag = tag.strip().upper()
    pattern = r"^[A-Z]{2,6}-\d{3,8}$"

    if not re.match(pattern, clean_tag):
        return False

    if expected_prefix is not None:
        clean_prefix = expected_prefix.strip().upper()
        tag_prefix = clean_tag.split("-")[0]
        if tag_prefix != clean_prefix:
            return False

    return True


def is_valid_email(email: str) -> bool:
    """Validate whether an email address format is valid.

    Checks:
    - Non-empty string without leading/trailing whitespace or internal spaces.
    - Exactly one '@' symbol separating local-part and domain.
    - Local part contains valid characters (alphanumeric, dot, underscore, plus, hyphen).
    - Domain contains at least one dot '.' with a valid top-level domain (2+ alpha chars).
    - No consecutive dots in local part or domain.

    Args:
        email: The email string to validate.

    Returns:
        True if email format is valid; False otherwise.

    Examples:
        >>> is_valid_email("pooja@company.com")
        True
        >>> is_valid_email("user.name+tag@sub.domain.org")
        True
        >>> is_valid_email("invalid-email@")
        False
        >>> is_valid_email("plainaddress")
        False
    """
    if not is_non_empty_string(email):
        return False

    clean_email = email.strip()

    # Standard RFC 5322 compatible practical regex
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

    if not re.match(pattern, clean_email):
        return False

    # Check for consecutive dots
    if ".." in clean_email:
        return False

    # Domain TLD check (must have at least 2 alpha characters after last dot)
    parts = clean_email.split("@")
    if len(parts) != 2:
        return False

    domain = parts[1]
    tld = domain.split(".")[-1]
    if len(tld) < 2 or not tld.isalpha():
        return False

    return True


def is_positive_number(value: Any) -> bool:
    """Check if the provided value is a strictly positive numeric number (> 0).

    Args:
        value: Any Python object to test.

    Returns:
        True if value is int or float (excluding bool) and > 0; False otherwise.

    Examples:
        >>> is_positive_number(42)
        True
        >>> is_positive_number(0.01)
        True
        >>> is_positive_number(0)
        False
        >>> is_positive_number(-5.5)
        False
        >>> is_positive_number(True)
        False
    """
    # bool is a subclass of int in Python, so explicitly exclude it
    if isinstance(value, bool):
        return False
    if isinstance(value, (int, float)):
        return value > 0
    return False


def is_valid_date_format(date_str: str, format_str: str = "%Y-%m-%d") -> bool:
    """Check if a date string strictly matches the given date format.

    Args:
        date_str: The date string to validate.
        format_str: The expected strptime format string (default: "%Y-%m-%d").

    Returns:
        True if date_str is valid and can be parsed; False otherwise.
    """
    if not is_non_empty_string(date_str):
        return False
    from datetime import datetime
    try:
        datetime.strptime(date_str.strip(), format_str)
        return True
    except ValueError:
        return False
