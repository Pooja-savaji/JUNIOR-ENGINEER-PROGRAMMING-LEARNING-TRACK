"""Number Analysis in Python (Beginner Friendly).

This program provides easy-to-understand functions to analyze numbers:
- Even vs Odd
- Prime number check
- Factors and divisors
- Sum of digits
- List statistics (Min, Max, Sum, Average)
- Palindrome and Armstrong number checks
"""


def is_even(n: int) -> bool:
    """Check if a number is divisible by 2."""
    return n % 2 == 0


def is_positive(n: float) -> str:
    """Check if a number is positive, negative, or zero."""
    if n > 0:
        return "Positive"
    elif n < 0:
        return "Negative"
    else:
        return "Zero"


def is_prime(n: int) -> bool:
    """Check if a number is prime (only divisible by 1 and itself)."""
    if n <= 1:
        return False
    # Check factors up to square root of n
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def find_factors(n: int) -> list:
    """Find all whole numbers that divide evenly into n."""
    if n <= 0:
        return []
    factors = []
    for i in range(1, n + 1):
        if n % i == 0:
            factors.append(i)
    return factors


def sum_of_digits(n: int) -> int:
    """Calculate the sum of all digits in a number."""
    total = 0
    for digit_char in str(abs(n)):
        total += int(digit_char)
    return total


def is_palindrome_number(n: int) -> bool:
    """Check if a number reads the same forwards and backwards (e.g. 121, 1331)."""
    s = str(abs(n))
    return s == s[::-1]


def is_armstrong_number(n: int) -> bool:
    """Check if sum of each digit raised to power of total digits equals the number (e.g. 153 = 1^3 + 5^3 + 3^3)."""
    if n < 0:
        return False
    digits = str(n)
    power = len(digits)
    total = sum(int(d) ** power for d in digits)
    return total == n


def analyze_list(numbers: list) -> dict:
    """Calculate summary statistics for a list of numbers."""
    if not numbers:
        return {}

    total_sum = sum(numbers)
    count = len(numbers)
    avg = total_sum / count
    smallest = min(numbers)
    largest = max(numbers)

    even_count = sum(1 for x in numbers if x % 2 == 0)
    odd_count = count - even_count

    return {
        "count": count,
        "sum": total_sum,
        "average": round(avg, 2),
        "min": smallest,
        "max": largest,
        "evens": even_count,
        "odds": odd_count,
    }


def run_demo():
    print("=" * 50)
    print("          🔢 NUMBER ANALYSIS DEMO              ")
    print("=" * 50)

    # Test single number analysis
    num = 153
    print(f"Analyzing Number: {num}")
    print(f"  • Sign: {is_positive(num)}")
    print(f"  • Even or Odd: {'Even' if is_even(num) else 'Odd'}")
    print(f"  • Is Prime? {is_prime(num)}")
    print(f"  • Factors: {find_factors(num)}")
    print(f"  • Sum of Digits: {sum_of_digits(num)}")
    print(f"  • Is Palindrome? {is_palindrome_number(num)}")
    print(f"  • Is Armstrong? {is_armstrong_number(num)}")

    # Test list analysis
    scores = [12, 45, 67, 88, 23, 90, 15]
    print(f"\nAnalyzing Number List: {scores}")
    stats = analyze_list(scores)
    for k, v in stats.items():
        print(f"  • {k.capitalize()}: {v}")


if __name__ == "__main__":
    run_demo()
