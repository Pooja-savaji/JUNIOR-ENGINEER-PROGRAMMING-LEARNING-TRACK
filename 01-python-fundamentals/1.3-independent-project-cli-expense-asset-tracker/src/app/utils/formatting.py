"""Formatting utilities for the Asset Tracker application.

Provides consistent formatting functions for currency, dates, percentages,
and standardized asset identifiers without external dependencies.
"""

from datetime import date, datetime
from typing import Union


def format_currency(
    amount: Union[float, int],
    currency_symbol: str = "$",
    decimal_places: int = 2,
) -> str:
    """Format a numeric value as a standardized currency string.

    Args:
        amount: The monetary amount to format (int or float).
        currency_symbol: The currency symbol to prepend (default: "$").
        decimal_places: Number of decimal places to include (default: 2).

    Returns:
        A formatted currency string with comma thousands separators.
        Negative amounts are formatted as "-$1,234.56".

    Examples:
        >>> format_currency(1234.5)
        '$1,234.50'
        >>> format_currency(-500)
        '-$500.00'
        >>> format_currency(0)
        '$0.00'
    """
    if not isinstance(amount, (int, float)):
        raise TypeError(f"amount must be int or float, got {type(amount).__name__}")

    is_negative = amount < 0
    abs_amount = abs(amount)
    formatted_number = f"{abs_amount:,.{decimal_places}f}"

    if is_negative:
        return f"-{currency_symbol}{formatted_number}"
    return f"{currency_symbol}{formatted_number}"


def format_date(
    date_val: Union[date, datetime, str],
    output_format: str = "%Y-%m-%d",
) -> str:
    """Format a date object, datetime object, or ISO date string consistently.

    Args:
        date_val: A date, datetime, or ISO formatted string (e.g. "2026-09-07").
        output_format: The target strftime format (default: "%Y-%m-%d").

    Returns:
        A formatted date string.

    Raises:
        ValueError: If a string cannot be parsed as an ISO date.
        TypeError: If the input type is unsupported.

    Examples:
        >>> from datetime import date
        >>> format_date(date(2026, 9, 7))
        '2026-09-07'
        >>> format_date("2026-09-07T14:30:00", output_format="%d/%m/%Y")
        '07/09/2026'
    """
    if isinstance(date_val, datetime):
        return date_val.strftime(output_format)
    elif isinstance(date_val, date):
        return date_val.strftime(output_format)
    elif isinstance(date_val, str):
        clean_str = date_val.strip()
        # Handle ISO date or ISO datetime strings
        try:
            if "T" in clean_str or " " in clean_str:
                # Replace space with T for standard isoformat parsing
                iso_clean = clean_str.replace(" ", "T")
                dt = datetime.fromisoformat(iso_clean)
            else:
                dt = datetime.strptime(clean_str, "%Y-%m-%d")
            return dt.strftime(output_format)
        except ValueError as err:
            raise ValueError(
                f"Cannot parse date string '{date_val}' with format '%Y-%m-%d' or ISO format."
            ) from err
    else:
        raise TypeError(
            f"date_val must be date, datetime, or str, got {type(date_val).__name__}"
        )


def format_asset_id(
    id_number: Union[int, str],
    prefix: str = "AST",
    padding: int = 6,
) -> str:
    """Format a raw ID number into a standardized, zero-padded asset identifier tag.

    Args:
        id_number: The sequential number or string representation of the ID.
        prefix: The prefix code representing the asset category (default: "AST").
        padding: The total number of digits to pad with leading zeros (default: 6).

    Returns:
        Standardized asset tag, e.g., "AST-000042".

    Raises:
        ValueError: If id_number cannot be converted to a positive integer.

    Examples:
        >>> format_asset_id(42)
        'AST-000042'
        >>> format_asset_id("105", prefix="SRV", padding=5)
        'SRV-00105'
    """
    try:
        numeric_val = int(str(id_number).strip())
        if numeric_val < 0:
            raise ValueError("Asset ID number must be non-negative.")
    except (ValueError, TypeError) as err:
        raise ValueError(
            f"Invalid asset ID '{id_number}'. Must be a non-negative integer."
        ) from err

    clean_prefix = str(prefix).strip().upper()
    return f"{clean_prefix}-{numeric_val:0{padding}d}"


def format_percentage(ratio: Union[float, int], decimal_places: int = 1) -> str:
    """Format a ratio (0.0 to 1.0 or higher) as a human-readable percentage.

    Args:
        ratio: Numeric value representing fraction (e.g., 0.854 -> 85.4%).
        decimal_places: Number of decimal digits to display (default: 1).

    Returns:
        Formatted percentage string.
    """
    if not isinstance(ratio, (int, float)):
        raise TypeError(f"ratio must be int or float, got {type(ratio).__name__}")
    percentage = ratio * 100
    return f"{percentage:.{decimal_places}f}%"
