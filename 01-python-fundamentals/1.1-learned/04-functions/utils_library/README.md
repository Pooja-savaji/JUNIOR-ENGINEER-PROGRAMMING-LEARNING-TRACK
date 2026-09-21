# utils_library

A reusable Python utility library extracted from the Day-1 fundamentals exercises.
All modules are pure Python (no external dependencies).

---

## Modules

### `math_utils.py`
Number-analysis helpers.

| Function | Description |
|---|---|
| `is_even(n)` | True if n is even |
| `is_odd(n)` | True if n is odd |
| `is_prime(n)` | True if n is prime |
| `find_factors(n)` | List of all factors of n |
| `sum_of_digits(n)` | Sum of digits in n |
| `is_palindrome_number(n)` | True if n reads same forwards/backwards |
| `is_armstrong_number(n)` | True if n equals sum of digits^power |

### `string_utils.py`
Text-transformation helpers.

| Function | Description |
|---|---|
| `to_upper(text)` | UPPER CASE |
| `to_lower(text)` | lower case |
| `to_title_case(text)` | Title Case |
| `to_camel_case(text)` | camelCase |
| `to_snake_case(text)` | snake_case |
| `to_kebab_case(text)` | kebab-case |
| `generate_slug(text)` | url-friendly-slug |
| `wrap_text(text, width)` | Word-wrap to width chars |
| `analyze_text(text)` | Dict: chars, words, sentences, paragraphs, unique words |

### `validation_utils.py`
Input-validation helpers.

| Function | Description |
|---|---|
| `is_non_empty_string(v)` | Non-empty / non-whitespace string |
| `is_positive_number(v)` | Positive numeric value |
| `is_valid_email(email)` | Basic e-mail format check |
| `is_valid_asset_tag(tag)` | Pattern: 2-4 LETTERS + hyphen + 4-8 digits |

### `formatting_utils.py`
Display-formatting helpers.

| Function | Description |
|---|---|
| `format_currency(amount)` | "$1,234.50" |
| `format_date(date_input, fmt)` | Formatted date string |
| `format_asset_id(prefix, num)` | "ASSET-000042" |
| `format_percentage(value)` | "87.5%" |

### `collection_utils.py`
List search and filter helpers.

| Function | Description |
|---|---|
| `linear_search(items, target)` | First index of target, or -1 |
| `binary_search(sorted_items, target)` | Binary search, O(log n) |
| `filter_by_range(nums, min, max)` | Keep values in [min, max] |
| `find_duplicates(items)` | Values that appear more than once |

### `stats_utils.py`
Statistical and aggregation helpers.

| Function | Description |
|---|---|
| `mean(numbers)` | Arithmetic mean |
| `median(numbers)` | Median value |
| `mode(numbers)` | Most common value |
| `compute_statistics(numbers)` | Dict: mean, median, mode, min, max, total, count |
| `aggregate_by_category(records, cat_key, val_key)` | Sum a value field per category |

---

## Quick Usage Example

```python
from utils_library import is_prime, format_currency, compute_statistics

print(is_prime(17))                  # True
print(format_currency(1234.5))       # $1,234.50
print(compute_statistics([80, 90, 70]))
# {"mean": 80.0, "median": 80.0, "mode": 80, "min": 70, "max": 90,
#  "total": 240, "count": 3}
```

---

## demo.py

Run `python demo.py` in this directory to see all modules in action.
