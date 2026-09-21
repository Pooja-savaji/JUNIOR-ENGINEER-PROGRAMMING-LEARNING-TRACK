"""
formatting_utils.py
===================
Display-formatting helpers extracted from formatting.py.
"""

from datetime import datetime


def format_currency(amount: float, symbol: str = "$", decimals: int = 2) -> str:
    """Format *amount* as a currency string.

    Example: format_currency(1234.5) -> "$1,234.50"
    """
    return f"{symbol}{amount:,.{decimals}f}"


def format_date(date_input, fmt: str = "%Y-%m-%d") -> str:
    """Format a date object or ISO string as *fmt*.

    Accepts datetime objects or strings like "2024-01-15".
    """
    if isinstance(date_input, str):
        date_input = datetime.fromisoformat(date_input)
    return date_input.strftime(fmt)


def format_asset_id(prefix: str, number: int, padding: int = 6) -> str:
    """Generate a zero-padded asset ID.

    Example: format_asset_id("ASSET", 42) -> "ASSET-000042"
    """
    return f"{prefix.upper()}-{str(number).zfill(padding)}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """Format *value* (0-100) as a percentage string.

    Example: format_percentage(87.5) -> "87.5%"
    """
    return f"{value:.{decimals}f}%"
