"""
demo.py  -  Quick demonstration of utils_library
Run:  python demo.py
"""

from utils_library.math_utils       import is_prime, find_factors, is_armstrong_number
from utils_library.string_utils     import to_camel_case, generate_slug, analyze_text
from utils_library.validation_utils import is_valid_email, is_valid_asset_tag
from utils_library.formatting_utils import format_currency, format_asset_id
from utils_library.collection_utils import binary_search, find_duplicates
from utils_library.stats_utils      import compute_statistics, aggregate_by_category


def section(title):
    print()
    print("=" * 50)
    print(f"  {title}")
    print("=" * 50)


section("math_utils")
print(f"is_prime(17)           = {is_prime(17)}")
print(f"find_factors(12)       = {find_factors(12)}")
print(f"is_armstrong_number(153) = {is_armstrong_number(153)}")

section("string_utils")
print(f"to_camel_case('hello world') = {to_camel_case('hello world')}")
print(f"generate_slug('Hello, World!') = {generate_slug('Hello, World!')}")
stats = analyze_text("The quick brown fox. Jumps over the lazy dog!")
print(f"analyze_text => words={stats['words']}, sentences={stats['sentences']}")

section("validation_utils")
print(f"is_valid_email('user@example.com') = {is_valid_email('user@example.com')}")
print(f"is_valid_asset_tag('IT-001234')    = {is_valid_asset_tag('IT-001234')}")

section("formatting_utils")
print(f"format_currency(4999.9) = {format_currency(4999.9)}")
print(f"format_asset_id('ASSET', 42) = {format_asset_id('ASSET', 42)}")

section("collection_utils")
nums = [10, 20, 30, 40, 50]
print(f"binary_search({nums}, 30) = {binary_search(nums, 30)}")
print(f"find_duplicates([1,2,2,3,3,3]) = {find_duplicates([1,2,2,3,3,3])}")

section("stats_utils")
scores = [78, 92, 88, 65, 92, 71]
print(f"compute_statistics({scores})")
for k, v in compute_statistics(scores).items():
    print(f"  {k}: {v}")

records = [
    {"cat": "food",  "amount": 20},
    {"cat": "travel","amount": 50},
    {"cat": "food",  "amount": 15},
]
print(f"aggregate_by_category => {aggregate_by_category(records, 'cat', 'amount')}")

print()
print("All demos complete!")
