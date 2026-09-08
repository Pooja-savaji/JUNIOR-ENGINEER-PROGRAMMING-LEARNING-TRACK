"""Search and Filter Problems in Python (Beginner Friendly).

Covers:
- Linear Search vs Binary Search
- Filtering numbers by condition (evens, range)
- Searching and filtering record collections (e.g. Products / Students)
- Finding duplicates and unique elements
"""


# --- 1. SEARCHING ALGORITHMS ---

def linear_search(items: list, target) -> int:
    """Find the index of target in items. Returns -1 if not found.

    Time Complexity: O(n) - checks each element one by one.
    """
    for index, value in enumerate(items):
        if value == target:
            return index
    return -1


def binary_search(sorted_items: list, target) -> int:
    """Fast search on a SORTED list by repeatedly halving the search area.

    Returns the index if found, or -1 if not found.
    Time Complexity: O(log n).
    """
    left = 0
    right = len(sorted_items) - 1

    while left <= right:
        mid = (left + right) // 2
        if sorted_items[mid] == target:
            return mid
        elif sorted_items[mid] < target:
            left = mid + 1  # Search right half
        else:
            right = mid - 1  # Search left half

    return -1


# --- 2. FILTERING FUNCTIONS ---

def filter_even_numbers(numbers: list) -> list:
    """Return only even numbers from a list."""
    return [x for x in numbers if x % 2 == 0]


def filter_by_range(numbers: list, min_val: float, max_val: float) -> list:
    """Return numbers that fall within [min_val, max_val] inclusive."""
    return [x for x in numbers if min_val <= x <= max_val]


def find_duplicates(items: list) -> list:
    """Find all values that appear more than once."""
    seen = set()
    duplicates = set()
    for item in items:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


# --- 3. FILTERING RECORD COLLECTIONS ---

SAMPLE_PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "category": "Electronics", "price": 25.99, "in_stock": True},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Electronics", "price": 89.99, "in_stock": True},
    {"id": 3, "name": "Desk Chair", "category": "Furniture", "price": 199.99, "in_stock": False},
    {"id": 4, "name": "USB-C Hub", "category": "Electronics", "price": 34.50, "in_stock": True},
    {"id": 5, "name": "Notebook Journal", "category": "Stationery", "price": 12.00, "in_stock": True},
]


def search_products_by_name(products: list, keyword: str) -> list:
    """Find all products whose name contains the keyword (case-insensitive)."""
    clean_keyword = keyword.strip().lower()
    return [p for p in products if clean_keyword in p["name"].lower()]


def filter_products_by_category(products: list, category: str) -> list:
    """Filter products belonging to a specific category."""
    clean_cat = category.strip().lower()
    return [p for p in products if p["category"].lower() == clean_cat]


def filter_in_stock_under_price(products: list, max_price: float) -> list:
    """Filter products that are in stock and cost less than or equal to max_price."""
    return [p for p in products if p["in_stock"] and p["price"] <= max_price]


def run_demo():
    print("=" * 55)
    print("       🔍 SEARCH & FILTER PROBLEMS DEMO           ")
    print("=" * 55)

    # 1. Searching
    numbers = [10, 25, 33, 47, 56, 72, 88, 99]
    target = 56
    print(f"List: {numbers}")
    print(f"• Linear search for {target} -> Index: {linear_search(numbers, target)}")
    print(f"• Binary search for {target} -> Index: {binary_search(numbers, target)}")
    print(f"• Binary search for 100 -> Index: {binary_search(numbers, 100)} (Not found)")

    # 2. Filtering
    data = [1, 4, 7, 12, 18, 23, 30, 4, 12, 99]
    print(f"\nRaw Data: {data}")
    print(f"• Even Numbers: {filter_even_numbers(data)}")
    print(f"• Range [10 to 30]: {filter_by_range(data, 10, 30)}")
    print(f"• Duplicate elements: {find_duplicates(data)}")

    # 3. Product Catalog Searching
    print("\nProduct Catalog Filtering:")
    print("• Products containing 'Board':")
    for p in search_products_by_name(SAMPLE_PRODUCTS, "board"):
        print(f"   - {p['name']} (${p['price']})")

    print("\n• Available Electronics under $50:")
    for p in filter_in_stock_under_price(SAMPLE_PRODUCTS, 50.0):
        print(f"   - {p['name']} (${p['price']}) [{p['category']}]")


if __name__ == "__main__":
    run_demo()
