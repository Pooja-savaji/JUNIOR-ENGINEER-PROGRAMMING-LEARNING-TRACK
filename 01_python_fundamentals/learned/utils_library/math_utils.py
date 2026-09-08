"""
math_utils.py
=============
Number-analysis helpers extracted from number_analysis.py.
"""


def is_even(n: int) -> bool:
    """Return True if *n* is even."""
    return n % 2 == 0


def is_odd(n: int) -> bool:
    """Return True if *n* is odd."""
    return n % 2 != 0


def is_prime(n: int) -> bool:
    """Return True if *n* is a prime number (>1 and divisible only by 1 and itself)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n ** 0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def find_factors(n: int) -> list:
    """Return a sorted list of all factors of *n*."""
    if n <= 0:
        return []
    return [i for i in range(1, n + 1) if n % i == 0]


def sum_of_digits(n: int) -> int:
    """Return the sum of all digits in *n* (ignores sign)."""
    return sum(int(d) for d in str(abs(n)))


def is_palindrome_number(n: int) -> bool:
    """Return True if *n* reads the same forwards and backwards."""
    s = str(abs(n))
    return s == s[::-1]


def is_armstrong_number(n: int) -> bool:
    """Return True if *n* equals the sum of its digits each raised to the power
    of the number of digits (e.g. 153 = 1^3 + 5^3 + 3^3)."""
    digits = str(abs(n))
    power = len(digits)
    return sum(int(d) ** power for d in digits) == abs(n)
