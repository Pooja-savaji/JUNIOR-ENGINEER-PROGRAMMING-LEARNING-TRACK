"""Interactive and Modular CLI Calculator.

Covers: arithmetic operators, precedence, float/int handling, math functions,
loop control, error handling (ZeroDivisionError, ValueError), and history tracking.
"""

import math
from typing import List, Tuple, Union


class Calculator:
    """Core calculation engine with history support."""

    def __init__(self) -> None:
        self.history: List[str] = []

    def add(self, a: float, b: float) -> float:
        """Return the sum of a and b."""
        res = a + b
        self._record(f"{a} + {b} = {res}")
        return res

    def subtract(self, a: float, b: float) -> float:
        """Return the difference of a and b."""
        res = a - b
        self._record(f"{a} - {b} = {res}")
        return res

    def multiply(self, a: float, b: float) -> float:
        """Return the product of a and b."""
        res = a * b
        self._record(f"{a} * {b} = {res}")
        return res

    def divide(self, a: float, b: float) -> float:
        """Return the division of a by b. Raises ZeroDivisionError if b == 0."""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        res = a / b
        self._record(f"{a} / {b} = {res}")
        return res

    def floor_divide(self, a: float, b: float) -> float:
        """Return the floor division of a by b."""
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        res = a // b
        self._record(f"{a} // {b} = {res}")
        return res

    def modulo(self, a: float, b: float) -> float:
        """Return a modulo b."""
        if b == 0:
            raise ZeroDivisionError("Cannot modulo by zero.")
        res = a % b
        self._record(f"{a} % {b} = {res}")
        return res

    def power(self, base: float, exponent: float) -> float:
        """Return base raised to the power of exponent."""
        res = math.pow(base, exponent)
        self._record(f"{base} ** {exponent} = {res}")
        return res

    def square_root(self, a: float) -> float:
        """Return the square root of a. Raises ValueError if a < 0."""
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number in real domain.")
        res = math.sqrt(a)
        self._record(f"sqrt({a}) = {res}")
        return res

    def percentage(self, part: float, total: float) -> float:
        """Calculate what percentage 'part' is of 'total'."""
        if total == 0:
            raise ZeroDivisionError("Total cannot be zero.")
        res = (part / total) * 100
        self._record(f"({part} / {total}) * 100 = {res:.2f}%")
        return res

    def _record(self, entry: str) -> None:
        self.history.append(entry)

    def get_history(self) -> List[str]:
        return list(self.history)

    def clear_history(self) -> None:
        self.history.clear()


def get_float_input(prompt: str) -> float:
    """Prompt user for a valid floating point number."""
    while True:
        raw = input(prompt).strip()
        try:
            return float(raw)
        except ValueError:
            print("[Error] Invalid input. Please enter a valid number (e.g., 42, 3.14).")


def run_calculator_cli():
    """Interactive loop for the calculator."""
    calc = Calculator()
    print("=" * 50)
    print("           🔢 PYTHON CLI CALCULATOR               ")
    print("=" * 50)

    menu = """
Select Operation:
  1. ➕ Addition (a + b)
  2. ➖ Subtraction (a - b)
  3. ✖️  Multiplication (a * b)
  4. ➗ Division (a / b)
  5. 📐 Floor Division (a // b)
  6. 🔄 Modulo (a % b)
  7. ⚡ Power (a ^ b)
  8. 🌿 Square Root (√a)
  9. 📊 Percentage (part of total)
 10. 📜 View History
 11. 🧹 Clear History
  0. 🚪 Exit
"""

    while True:
        print(menu)
        choice = input("Enter choice (0-11): ").strip()

        if choice == "0":
            print("\nThank you for using Python Calculator. Goodbye! 👋\n")
            break

        if choice in ("1", "2", "3", "4", "5", "6", "7"):
            a = get_float_input("Enter first number (a): ")
            b = get_float_input("Enter second number (b): ")
            try:
                if choice == "1":
                    res = calc.add(a, b)
                    print(f"\nResult: {a} + {b} = {res:,}")
                elif choice == "2":
                    res = calc.subtract(a, b)
                    print(f"\nResult: {a} - {b} = {res:,}")
                elif choice == "3":
                    res = calc.multiply(a, b)
                    print(f"\nResult: {a} * {b} = {res:,}")
                elif choice == "4":
                    res = calc.divide(a, b)
                    print(f"\nResult: {a} / {b} = {res:,}")
                elif choice == "5":
                    res = calc.floor_divide(a, b)
                    print(f"\nResult: {a} // {b} = {res:,}")
                elif choice == "6":
                    res = calc.modulo(a, b)
                    print(f"\nResult: {a} % {b} = {res:,}")
                elif choice == "7":
                    res = calc.power(a, b)
                    print(f"\nResult: {a} ^ {b} = {res:,}")
            except ZeroDivisionError as err:
                print(f"\n[Math Error] {err}")
            except OverflowError:
                print("\n[Math Error] Number too large to compute.")

        elif choice == "8":
            a = get_float_input("Enter number (a): ")
            try:
                res = calc.square_root(a)
                print(f"\nResult: √{a} = {res:,}")
            except ValueError as err:
                print(f"\n[Math Error] {err}")

        elif choice == "9":
            part = get_float_input("Enter part: ")
            total = get_float_input("Enter total: ")
            try:
                res = calc.percentage(part, total)
                print(f"\nResult: {part} is {res:.2f}% of {total}")
            except ZeroDivisionError as err:
                print(f"\n[Math Error] {err}")

        elif choice == "10":
            history = calc.get_history()
            print("\n--- Calculation History ---")
            if not history:
                print("No calculations performed yet.")
            else:
                for idx, entry in enumerate(history, 1):
                    print(f"  {idx}. {entry}")

        elif choice == "11":
            calc.clear_history()
            print("\n[Success] History cleared.")
        else:
            print("\n[Error] Invalid choice. Please select from 0 to 11.")


if __name__ == "__main__":
    run_calculator_cli()
