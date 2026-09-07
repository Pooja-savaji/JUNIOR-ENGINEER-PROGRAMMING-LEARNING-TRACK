# Day 1: Python Fundamentals Notes (§4)

## 1. Variables & Types
- **Variables**: Named references to objects in memory; dynamic typing (no declaration needed).
- **Primitive Types**:
  - `int`: Arbitrary precision integers (`42`, `-10`).
  - `float`: Double-precision 64-bit IEEE 754 floating point numbers (`3.14159`).
  - `str`: Immutable sequence of Unicode characters (`"hello"`, `'asset'`).
  - `bool`: Subtype of integer (`True`, `False`).
  - `NoneType`: Singleton representing the absence of a value (`None`).
- **Type Checking & Conversion**: `type(x)`, `isinstance(x, int)`, `int("42")`, `str(100)`, `float("3.5")`.

## 2. Expressions & Operators
- **Arithmetic**: `+`, `-`, `*`, `/` (float division), `//` (floor division), `%` (modulus), `**` (exponentiation).
- **Comparison**: `==`, `!=`, `<`, `<=`, `>`, `>=`.
- **Logical**: `and`, `or`, `not` (short-circuit evaluation).
- **Identity & Membership**: `is`, `is not`, `in`, `not in`.

## 3. Input & Output (I/O)
- **Standard Output**: `print(*objects, sep=' ', end='\n')`.
- **String Formatting**:
  - f-strings: `f"Asset ID: {asset_id:06d}, Price: ${price:,.2f}"`.
- **Standard Input**: `input(prompt)` returns a string; always cast with error handling.

## 4. Indentation & Control Flow
- Indentation denotes code blocks (standard is 4 spaces).
- `if / elif / else` conditionals.
- `for item in iterable:` loops.
- `while condition:` loops.
- Loop control: `break`, `continue`, `pass`.

## 5. Modules, Functions & Imports
- Functions defined with `def function_name(param1: type) -> return_type:`.
- Docstrings using triple quotes `"""` for documentation.
- Module imports: `import math`, `from datetime import datetime, date`.
- Executable script guard: `if __name__ == "__main__":`.
