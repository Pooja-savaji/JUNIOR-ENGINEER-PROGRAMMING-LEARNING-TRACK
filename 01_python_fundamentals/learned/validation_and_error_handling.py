"""
validation_and_error_handling.py
=================================
Day 1 - Python Fundamentals Exercise
Topic  : Validation utilities and failure-handling patterns

What you will learn
-------------------
1. Custom exception classes
2. Input-validation functions that RAISE errors (not just return True/False)
3. try / except / else / finally blocks
4. Retrying on failure (retry loop pattern)
5. Graceful degradation (fallback values)
6. Chaining multiple validators
7. Simulated real-world scenarios

Run:
    python validation_and_error_handling.py
"""

import re
import time
import random
import os


# =============================================================================
# PART 1 — CUSTOM EXCEPTION CLASSES
# =============================================================================
# Python lets you create your own exception types by subclassing Exception.
# This makes errors more descriptive and easier to catch selectively.

class ValidationError(Exception):
    """Raised when a value fails validation."""
    pass


class EmptyValueError(ValidationError):
    """Raised when a required field is empty or whitespace-only."""
    pass


class TypeMismatchError(ValidationError):
    """Raised when a value is the wrong data type."""
    pass


class RangeError(ValidationError):
    """Raised when a numeric value is outside the allowed range."""
    pass


class FormatError(ValidationError):
    """Raised when a string does not match the expected format."""
    pass


class FileProcessingError(Exception):
    """Raised when a file cannot be read or parsed."""
    pass


class NetworkError(Exception):
    """Raised when a simulated network call fails."""
    pass


# =============================================================================
# PART 2 — VALIDATION UTILITY FUNCTIONS
# =============================================================================
# Each function either returns the (possibly cleaned) value on success,
# or RAISES a specific exception on failure.

def require_non_empty(value: str, field_name: str = "field") -> str:
    """Ensure *value* is a non-empty, non-whitespace string.

    Returns the stripped string on success.
    Raises EmptyValueError on failure.
    """
    if not isinstance(value, str):
        raise TypeMismatchError(
            f"'{field_name}' must be a string, got {type(value).__name__}."
        )
    stripped = value.strip()
    if not stripped:
        raise EmptyValueError(f"'{field_name}' must not be empty.")
    return stripped


def validate_integer(value, field_name: str = "value",
                     min_val: int = None, max_val: int = None) -> int:
    """Convert *value* to int and optionally check it is within [min_val, max_val].

    Returns the integer on success.
    Raises TypeMismatchError or RangeError on failure.
    """
    try:
        n = int(value)
    except (ValueError, TypeError):
        raise TypeMismatchError(
            f"'{field_name}' must be an integer, got: {value!r}"
        )
    if min_val is not None and n < min_val:
        raise RangeError(
            f"'{field_name}' must be >= {min_val}, got {n}."
        )
    if max_val is not None and n > max_val:
        raise RangeError(
            f"'{field_name}' must be <= {max_val}, got {n}."
        )
    return n


def validate_float(value, field_name: str = "value",
                   min_val: float = None, max_val: float = None) -> float:
    """Convert *value* to float and optionally check range.

    Returns the float on success.
    Raises TypeMismatchError or RangeError on failure.
    """
    try:
        n = float(value)
    except (ValueError, TypeError):
        raise TypeMismatchError(
            f"'{field_name}' must be a number, got: {value!r}"
        )
    if min_val is not None and n < min_val:
        raise RangeError(f"'{field_name}' must be >= {min_val}, got {n}.")
    if max_val is not None and n > max_val:
        raise RangeError(f"'{field_name}' must be <= {max_val}, got {n}.")
    return n


def validate_email(email: str) -> str:
    """Validate *email* against a standard email pattern.

    Returns the lowercased email on success.
    Raises FormatError on failure.
    """
    email = require_non_empty(email, "email")
    pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, email):
        raise FormatError(
            f"Invalid email address: {email!r}. "
            "Expected format: user@example.com"
        )
    return email.lower()


def validate_password(password: str) -> str:
    """Check that *password* meets minimum security requirements:
    - At least 8 characters
    - Contains at least one digit
    - Contains at least one uppercase letter

    Returns the password on success.
    Raises FormatError on failure.
    """
    require_non_empty(password, "password")
    errors = []
    if len(password) < 8:
        errors.append("at least 8 characters")
    if not any(c.isdigit() for c in password):
        errors.append("at least one digit (0-9)")
    if not any(c.isupper() for c in password):
        errors.append("at least one uppercase letter (A-Z)")
    if errors:
        raise FormatError(
            "Password does not meet requirements: " + "; ".join(errors)
        )
    return password


def validate_asset_tag(tag: str) -> str:
    """Validate asset tag format: 2-4 uppercase letters, hyphen, 4-8 digits.

    Example valid tags: ASET-001234, IT-9999, HR-00001234
    Returns the uppercased tag on success.
    Raises FormatError on failure.
    """
    tag = require_non_empty(tag, "asset_tag")
    tag = tag.upper()
    pattern = r"^[A-Z]{2,4}-\d{4,8}$"
    if not re.match(pattern, tag):
        raise FormatError(
            f"Invalid asset tag: {tag!r}. "
            "Expected: 2-4 letters + hyphen + 4-8 digits  e.g. ASSET-001234"
        )
    return tag


def validate_date_string(date_str: str, fmt: str = "%Y-%m-%d") -> str:
    """Validate that *date_str* matches *fmt* (default YYYY-MM-DD).

    Returns the date string unchanged on success.
    Raises FormatError on failure.
    """
    from datetime import datetime
    date_str = require_non_empty(date_str, "date")
    try:
        datetime.strptime(date_str, fmt)
    except ValueError:
        raise FormatError(
            f"Invalid date: {date_str!r}. Expected format: {fmt}"
        )
    return date_str


# =============================================================================
# PART 3 — CHAINED VALIDATOR (validate multiple fields at once)
# =============================================================================

def validate_user_form(data: dict) -> dict:
    """Validate a user-registration form dict.

    Expected keys: name, email, age, password
    Returns a cleaned dict on success.
    Raises ValidationError (or subclass) on the first invalid field.
    """
    cleaned = {}
    cleaned["name"]     = require_non_empty(data.get("name", ""), "name")
    cleaned["email"]    = validate_email(data.get("email", ""))
    cleaned["age"]      = validate_integer(data.get("age", ""), "age",
                                           min_val=1, max_val=120)
    cleaned["password"] = validate_password(data.get("password", ""))
    return cleaned


# =============================================================================
# PART 4 — TRY / EXCEPT / ELSE / FINALLY PATTERNS
# =============================================================================

def safe_divide(a, b):
    """Demonstrate try / except / else / finally.

    - try    : code that might fail
    - except : handle specific errors
    - else   : runs ONLY if no exception was raised
    - finally: ALWAYS runs (cleanup)
    """
    print(f"\n  Dividing {a} / {b} ...")
    try:
        result = a / b                  # may raise ZeroDivisionError
    except ZeroDivisionError:
        print("  ERROR: Cannot divide by zero!")
        return None
    except TypeError as e:
        print(f"  ERROR: Wrong type — {e}")
        return None
    else:
        # Only reached when try succeeded
        print(f"  Result: {result:.4f}")
        return result
    finally:
        # Always reached — great for cleanup (closing files, DB connections)
        print("  [finally] Division attempt finished.")


def safe_open_file(filepath: str) -> str:
    """Read a file safely, returning its contents or raising FileProcessingError."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            contents = f.read()
    except FileNotFoundError:
        raise FileProcessingError(f"File not found: {filepath!r}")
    except PermissionError:
        raise FileProcessingError(f"Permission denied reading: {filepath!r}")
    except OSError as e:
        raise FileProcessingError(f"OS error reading {filepath!r}: {e}")
    return contents


# =============================================================================
# PART 5 — RETRY PATTERN
# =============================================================================

def simulate_network_call(fail_rate: float = 0.6) -> str:
    """Simulate a network call that randomly fails.

    *fail_rate* = probability of failure (0.0 to 1.0).
    Raises NetworkError on simulated failure.
    """
    if random.random() < fail_rate:
        raise NetworkError("Simulated network timeout!")
    return "{'status': 'ok', 'data': [1, 2, 3]}"


def fetch_with_retry(max_attempts: int = 3, delay_seconds: float = 0.3) -> str:
    """Call simulate_network_call() up to *max_attempts* times.

    Returns the response on success.
    Raises NetworkError if all attempts fail.
    """
    last_error = None
    for attempt in range(1, max_attempts + 1):
        try:
            print(f"  Attempt {attempt}/{max_attempts} ...", end=" ")
            result = simulate_network_call(fail_rate=0.6)
            print("SUCCESS")
            return result
        except NetworkError as e:
            last_error = e
            print(f"FAILED ({e})")
            if attempt < max_attempts:
                print(f"  Waiting {delay_seconds}s before retry ...")
                time.sleep(delay_seconds)

    # All attempts exhausted
    raise NetworkError(
        f"All {max_attempts} attempts failed. Last error: {last_error}"
    )


# =============================================================================
# PART 6 — GRACEFUL DEGRADATION (fallback values)
# =============================================================================

def get_config_value(config: dict, key: str, default=None):
    """Safely retrieve a value from a config dict.

    Returns *default* instead of raising KeyError.
    This is the 'graceful degradation' pattern — fail softly.
    """
    try:
        value = config[key]
        if value is None:
            return default
        return value
    except KeyError:
        print(f"  Config key {key!r} not found, using default: {default!r}")
        return default


def parse_number_safe(text: str, default: float = 0.0) -> float:
    """Convert *text* to float, returning *default* if conversion fails.

    Useful when reading data from CSV files or user input.
    """
    try:
        return float(text)
    except (ValueError, TypeError):
        return default


# =============================================================================
# PART 7 — COLLECT ALL ERRORS (bulk validation)
# =============================================================================

def validate_batch(records: list) -> dict:
    """Validate a list of asset tag strings, collecting ALL errors.

    Instead of stopping at the first error, this pattern gathers every
    problem so the user can fix them all at once.

    Returns:
        {
          "valid":  [list of valid tags],
          "errors": [{"index": i, "value": v, "error": msg}, ...]
        }
    """
    valid_tags  = []
    error_list  = []

    for i, tag in enumerate(records):
        try:
            cleaned = validate_asset_tag(tag)
            valid_tags.append(cleaned)
        except ValidationError as e:
            error_list.append({
                "index": i,
                "value": tag,
                "error": str(e),
            })

    return {"valid": valid_tags, "errors": error_list}


# =============================================================================
# PART 8 — DEMO / RUNNER
# =============================================================================

def section(title: str) -> None:
    print()
    print("=" * 60)
    print(f"  {title}")
    print("=" * 60)


def demo_validators():
    section("PART 1 — Basic Validators")

    # ---- require_non_empty
    print("\n[require_non_empty]")
    for val in ["hello", "  ", "", 42]:
        try:
            result = require_non_empty(str(val) if not isinstance(val, str) else val, "name")
            # treat int specially to trigger TypeMismatchError
            if isinstance(val, int):
                result = require_non_empty(val, "name")
            print(f"  OK : {val!r}  ->  {result!r}")
        except (EmptyValueError, TypeMismatchError) as e:
            print(f"  ERR: {val!r}  ->  {e}")

    # ---- validate_integer
    print("\n[validate_integer  age, range 1-120]")
    for val in ["25", "0", "200", "abc", None]:
        try:
            result = validate_integer(val, "age", min_val=1, max_val=120)
            print(f"  OK : {val!r}  ->  {result}")
        except (TypeMismatchError, RangeError) as e:
            print(f"  ERR: {val!r}  ->  {e}")

    # ---- validate_email
    print("\n[validate_email]")
    for email in ["user@example.com", "bad-email", "@no-user.com", ""]:
        try:
            result = validate_email(email)
            print(f"  OK : {email!r}  ->  {result!r}")
        except (EmptyValueError, FormatError) as e:
            print(f"  ERR: {email!r}  ->  {e}")

    # ---- validate_password
    print("\n[validate_password]")
    for pw in ["Secret1!", "short", "nouppercase1", "NoDigitHere"]:
        try:
            validate_password(pw)
            print(f"  OK : {pw!r}")
        except FormatError as e:
            print(f"  ERR: {pw!r}  ->  {e}")

    # ---- validate_asset_tag
    print("\n[validate_asset_tag]")
    for tag in ["ASSET-001234", "it-99", "TOOLONG-12345", "HR-00001234"]:
        try:
            result = validate_asset_tag(tag)
            print(f"  OK : {tag!r}  ->  {result!r}")
        except FormatError as e:
            print(f"  ERR: {tag!r}  ->  {e}")


def demo_form_validation():
    section("PART 2 — Chained Form Validation")

    forms = [
        # Good form
        {"name": "Alice Smith", "email": "alice@example.com",
         "age": "28", "password": "SecurePass1"},
        # Missing name
        {"name": "", "email": "bob@example.com",
         "age": "30", "password": "SecurePass1"},
        # Bad email
        {"name": "Charlie", "email": "not-an-email",
         "age": "25", "password": "SecurePass1"},
        # Age out of range
        {"name": "Diana", "email": "diana@test.com",
         "age": "150", "password": "SecurePass1"},
    ]

    for i, form in enumerate(forms, 1):
        print(f"\n  Form {i}: {form}")
        try:
            cleaned = validate_user_form(form)
            print(f"  VALID -> {cleaned}")
        except ValidationError as e:
            # Catch the base class so we catch ALL subclasses
            print(f"  INVALID -> {type(e).__name__}: {e}")


def demo_try_except():
    section("PART 3 — try / except / else / finally")
    safe_divide(10, 3)
    safe_divide(10, 0)
    safe_divide("ten", 2)

    print("\n[safe_open_file]")
    for path in ["sample_app.log", "missing_file.txt"]:
        try:
            contents = safe_open_file(path)
            lines = contents.strip().splitlines()
            print(f"  OK : {path!r} -> {len(lines)} lines")
        except FileProcessingError as e:
            print(f"  ERR: {e}")


def demo_retry():
    section("PART 4 — Retry Pattern")
    random.seed(42)   # fixed seed for reproducible demo
    print("\n  Attempting network call with up to 3 retries ...")
    try:
        response = fetch_with_retry(max_attempts=3, delay_seconds=0.1)
        print(f"  Got response: {response}")
    except NetworkError as e:
        print(f"  All retries failed: {e}")


def demo_graceful_degradation():
    section("PART 5 — Graceful Degradation (fallbacks)")

    config = {"host": "localhost", "port": 5432, "timeout": None}
    for key, default in [("host", "127.0.0.1"), ("port", 5432),
                         ("timeout", 30), ("db_name", "mydb")]:
        value = get_config_value(config, key, default=default)
        print(f"  {key} = {value!r}")

    print("\n[parse_number_safe]")
    for raw in ["3.14", "99", "abc", None, ""]:
        result = parse_number_safe(raw, default=-1.0)
        print(f"  {raw!r} -> {result}")


def demo_batch_validation():
    section("PART 6 — Batch Validation (collect all errors)")

    tags = ["ASET-001234", "bad-tag", "IT-9999", "x-1",
            "HR-00005678", "TOOLONG-123", "PC-00042"]
    print(f"\n  Input tags: {tags}")
    result = validate_batch(tags)

    print(f"\n  Valid ({len(result['valid'])}): {result['valid']}")
    print(f"\n  Errors ({len(result['errors'])}):")
    for err in result["errors"]:
        print(f"    [{err['index']}] {err['value']!r} -> {err['error']}")


def main():
    print("=" * 60)
    print("  VALIDATION UTILITIES & FAILURE-HANDLING EXERCISES")
    print("=" * 60)

    demo_validators()
    demo_form_validation()
    demo_try_except()
    demo_retry()
    demo_graceful_degradation()
    demo_batch_validation()

    print()
    print("=" * 60)
    print("  All exercises complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
