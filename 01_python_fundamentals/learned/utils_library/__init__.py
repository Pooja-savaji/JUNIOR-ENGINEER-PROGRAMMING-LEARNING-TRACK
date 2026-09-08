"""
utils_library
=============
A reusable utility library extracted from Day-1 Python fundamentals exercises.

Modules
-------
- math_utils       : number checks and analysis helpers
- string_utils     : text transformation and analysis helpers
- validation_utils : input-validation helpers
- formatting_utils : display-formatting helpers
- collection_utils : list search, filter, and dedup helpers
- stats_utils      : statistics and aggregation helpers
"""

from .math_utils       import (is_even, is_odd, is_prime, find_factors,
                                sum_of_digits, is_palindrome_number,
                                is_armstrong_number)
from .string_utils     import (to_upper, to_lower, to_title_case,
                                to_camel_case, to_snake_case, to_kebab_case,
                                generate_slug, wrap_text, analyze_text)
from .validation_utils import (is_non_empty_string, is_positive_number,
                                is_valid_email, is_valid_asset_tag)
from .formatting_utils import (format_currency, format_date,
                                format_asset_id, format_percentage)
from .collection_utils import (linear_search, binary_search,
                                filter_by_range, find_duplicates)
from .stats_utils      import (mean, median, mode, compute_statistics,
                                aggregate_by_category)

__all__ = [
    # math
    "is_even", "is_odd", "is_prime", "find_factors",
    "sum_of_digits", "is_palindrome_number", "is_armstrong_number",
    # string
    "to_upper", "to_lower", "to_title_case",
    "to_camel_case", "to_snake_case", "to_kebab_case",
    "generate_slug", "wrap_text", "analyze_text",
    # validation
    "is_non_empty_string", "is_positive_number",
    "is_valid_email", "is_valid_asset_tag",
    # formatting
    "format_currency", "format_date", "format_asset_id", "format_percentage",
    # collection
    "linear_search", "binary_search", "filter_by_range", "find_duplicates",
    # stats
    "mean", "median", "mode", "compute_statistics", "aggregate_by_category",
]
