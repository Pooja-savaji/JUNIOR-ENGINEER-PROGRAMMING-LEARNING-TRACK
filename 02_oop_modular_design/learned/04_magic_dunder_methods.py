"""
04_magic_dunder_methods.py
===========================
Module 2: Object-Oriented Programming & Modular Design
Topic: Python Magic (Dunder) Methods, Operator Overloading, and Context Managers

Concepts Covered:
  - Domain Value Object: `Money` with Decimal precision
  - String representations: `__str__` (user-facing) vs. `__repr__` (developer/eval-ready)
  - Equality and Hashing: `__eq__`, `__hash__` (allowing set/dict key usage)
  - Operator Overloading: `__add__`, `__sub__`, `__mul__`, `__rmul__`, `__truediv__`, `__neg__`
  - Total Ordering: `@total_ordering` with `__lt__` (safeguarded against currency mismatches)
  - Container / Collection Dunders: `Portfolio` with `__len__`, `__getitem__`, `__contains__`, `__iter__`
  - Context Management: `SafeTransactionScope` using `__enter__` and `__exit__` for rollback semantics
"""

from __future__ import annotations
from decimal import Decimal, ROUND_HALF_UP
from functools import total_ordering
from typing import Any, List, Iterator, Dict


@total_ordering
class Money:
    """Immutable financial Value Object with currency safeguards and operator overloading."""

    def __init__(self, amount: Any, currency: str = "USD") -> None:
        if not currency or not isinstance(currency, str):
            raise ValueError("Currency must be a 3-letter uppercase string.")

        # Ensure exact Decimal precision for currency arithmetic
        try:
            dec_amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except Exception as err:
            raise ValueError(f"Invalid monetary amount: {amount!r}") from err

        self._amount: Decimal = dec_amount
        self._currency: str = currency.strip().upper()

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    # ─────────────────────────────────────────────────────────────────────────
    # String Representations
    # ─────────────────────────────────────────────────────────────────────────

    def __repr__(self) -> str:
        """Precise unambiguous representation for debugging."""
        return f"Money('{self._amount}', '{self._currency}')"

    def __str__(self) -> str:
        """Human-friendly formatted output."""
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "JPY": "¥", "INR": "₹"}
        sym = symbols.get(self._currency, f"{self._currency} ")
        return f"{sym}{self._amount:,.2f}"

    # ─────────────────────────────────────────────────────────────────────────
    # Equality and Hashing
    # ─────────────────────────────────────────────────────────────────────────

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._currency == other._currency and self._amount == other._amount

    def __hash__(self) -> int:
        """Allows Money instances to be inserted into sets or used as dict keys."""
        return hash((self._amount, self._currency))

    # ─────────────────────────────────────────────────────────────────────────
    # Ordering (__lt__ required by @total_ordering)
    # ─────────────────────────────────────────────────────────────────────────

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise TypeError(
                f"Cannot compare different currencies: {self._currency} vs {other._currency}."
            )
        return self._amount < other._amount

    # ─────────────────────────────────────────────────────────────────────────
    # Operator Overloading (Arithmetic)
    # ─────────────────────────────────────────────────────────────────────────

    def __add__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValueError(
                f"Cannot add different currencies: {self._currency} and {other._currency}."
            )
        return Money(self._amount + other._amount, self._currency)

    def __sub__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValueError(
                f"Cannot subtract different currencies: {self._currency} and {other._currency}."
            )
        return Money(self._amount - other._amount, self._currency)

    def __mul__(self, factor: Any) -> Money:
        """Multiply money by a scalar number."""
        try:
            scalar = Decimal(str(factor))
        except Exception:
            return NotImplemented
        return Money(self._amount * scalar, self._currency)

    def __rmul__(self, factor: Any) -> Money:
        """Support commutativity: factor * money."""
        return self.__mul__(factor)

    def __truediv__(self, divisor: Any) -> Money:
        """Divide money by a scalar number."""
        try:
            scalar = Decimal(str(divisor))
            if scalar == 0:
                raise ZeroDivisionError("Cannot divide monetary amount by zero.")
        except ZeroDivisionError:
            raise
        except Exception:
            return NotImplemented
        return Money(self._amount / scalar, self._currency)

    def __neg__(self) -> Money:
        return Money(-self._amount, self._currency)

    def __bool__(self) -> bool:
        """Truthiness: returns True if amount is non-zero."""
        return self._amount != Decimal("0.00")


# ─────────────────────────────────────────────────────────────────────────────
# CONTAINER / COLLECTION DUNDERS
# ─────────────────────────────────────────────────────────────────────────────

class AssetPortfolio:
    """Collection class demonstrating container dunder methods."""

    def __init__(self, name: str) -> None:
        self.name: str = name
        self._holdings: List[Dict[str, Any]] = []

    def add_asset(self, symbol: str, quantity: int, unit_value: Money) -> None:
        self._holdings.append({
            "symbol": symbol.upper(),
            "quantity": quantity,
            "unit_value": unit_value,
            "total_value": unit_value * quantity,
        })

    def __len__(self) -> int:
        """Returns number of unique assets in the portfolio."""
        return len(self._holdings)

    def __getitem__(self, index_or_symbol: Any) -> Dict[str, Any]:
        """Support indexing portfolio[0] as well as lookup by symbol portfolio['AAPL']."""
        if isinstance(index_or_symbol, int):
            return self._holdings[index_or_symbol]
        elif isinstance(index_or_symbol, str):
            sym = index_or_symbol.strip().upper()
            for item in self._holdings:
                if item["symbol"] == sym:
                    return item
            raise KeyError(f"Asset symbol {index_or_symbol!r} not found in portfolio.")
        raise TypeError(f"Invalid index or key type: {type(index_or_symbol)}")

    def __contains__(self, symbol: object) -> bool:
        """Support `'AAPL' in portfolio`."""
        if not isinstance(symbol, str):
            return False
        sym = symbol.strip().upper()
        return any(item["symbol"] == sym for item in self._holdings)

    def __iter__(self) -> Iterator[Dict[str, Any]]:
        """Support iterating `for item in portfolio:`."""
        return iter(self._holdings)


# ─────────────────────────────────────────────────────────────────────────────
# CONTEXT MANAGER DUNDERS (__enter__ and __exit__)
# ─────────────────────────────────────────────────────────────────────────────

class SafeTransactionScope:
    """Context manager demonstrating __enter__ and __exit__ for atomic rollback safety."""

    def __init__(self, ledger: Dict[str, Money], description: str = "Batch Operation") -> None:
        self._ledger = ledger
        self._description = description
        self._snapshot: Dict[str, Money] = {}

    def __enter__(self) -> SafeTransactionScope:
        print(f"  [TX SCOPE BEGIN] {self._description}")
        # Capture deep snapshot of ledger state before mutations
        self._snapshot = {k: Money(v.amount, v.currency) for k, v in self._ledger.items()}
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if exc_type is not None:
            # An error occurred: Roll back to original snapshot
            print(f"  [TX SCOPE ROLLBACK] Exception caught ({exc_type.__name__}: {exc_val}).")
            print("    Restoring ledger to pre-transaction snapshot...")
            self._ledger.clear()
            self._ledger.update(self._snapshot)
            # Returning False lets exception propagate to caller after rollback
            return False

        # Clean exit: commit transaction
        print(f"  [TX SCOPE COMMIT] {self._description} applied successfully.")
        return True


def main():
    print("=" * 70)
    print("  EXERCISE 04: MAGIC (DUNDER) METHODS & OPERATOR OVERLOADING")
    print("=" * 70)

    # 1. Money Arithmetic & Representations
    print("\n[1] Value Object (Money) Operator Overloading:")
    price_a = Money("125.50", "USD")
    price_b = Money("74.25", "USD")

    print(f"  repr(price_a) : {repr(price_a)}")
    print(f"  str(price_a)  : {price_a}")
    print(f"  price_a + price_b = {price_a + price_b}")
    print(f"  price_a - price_b = {price_a - price_b}")
    print(f"  price_a * 3       = {price_a * 3}")
    print(f"  3 * price_a       = {3 * price_a} (Commutative)")
    print(f"  price_a / 2       = {price_a / 2}")

    # 2. Currency mismatch safeguard
    print("\n[2] Currency Safety Enforcement:")
    euro_price = Money("50.00", "EUR")
    try:
        _ = price_a + euro_price
    except ValueError as err:
        print(f"  [Expected Error Caught] Multi-currency addition blocked: {err}")

    # 3. Ordering and Sets (Hashing)
    print("\n[3] Ordering and Hashability (Sets & Sorting):")
    prices = [Money("99.99", "USD"), Money("14.50", "USD"), Money("250.00", "USD"), Money("14.50", "USD")]
    print(f"  Original list: {prices}")
    print(f"  Sorted prices: {sorted(prices)}")

    unique_prices = set(prices)
    print(f"  Unique in set (Hashing): {unique_prices}")

    # 4. Container Collection (AssetPortfolio)
    print("\n[4] Container Protocol (__len__, __getitem__, __contains__, __iter__):")
    portfolio = AssetPortfolio("Tech Growth")
    portfolio.add_asset("AAPL", 10, Money("180.50", "USD"))
    portfolio.add_asset("MSFT", 5, Money("420.00", "USD"))
    portfolio.add_asset("NVDA", 8, Money("125.00", "USD"))

    print(f"  Portfolio size (len): {len(portfolio)} assets")
    print(f"  'MSFT' in portfolio : {'MSFT' in portfolio}")
    print(f"  'TSLA' in portfolio : {'TSLA' in portfolio}")
    print(f"  portfolio['AAPL']   : {portfolio['AAPL']['total_value']}")
    print(f"  portfolio[1]        : {portfolio[1]['symbol']} (by integer index)")

    print("  Iterating through portfolio:")
    for holding in portfolio:
        print(f"    {holding['symbol']:<5} x {holding['quantity']:>2} @ {holding['unit_value']} = {holding['total_value']}")

    # 5. Context Manager (SafeTransactionScope)
    print("\n[5] Context Manager (__enter__ / __exit__ Rollback Test):")
    ledger = {
        "alice": Money("500.00", "USD"),
        "bob": Money("200.00", "USD"),
    }
    print(f"  Initial Ledger: {ledger}")

    # Successful Transaction
    with SafeTransactionScope(ledger, "Valid Transfer $100 Alice -> Bob"):
        ledger["alice"] = ledger["alice"] - Money("100.00", "USD")
        ledger["bob"] = ledger["bob"] + Money("100.00", "USD")
    print(f"  Post-commit Ledger: {ledger}")

    # Failed Transaction with Rollback
    print("\n  Executing Failing Transaction:")
    try:
        with SafeTransactionScope(ledger, "Failing Transfer with Crash"):
            ledger["alice"] = ledger["alice"] - Money("300.00", "USD")
            raise RuntimeError("Network failure while crediting recipient!")
    except RuntimeError as err:
        print(f"  Handled outer exception: {err}")

    print(f"  Post-rollback Ledger (Restored!): {ledger}")

    print("\nMagic methods & context managers demonstration complete!\n")


if __name__ == "__main__":
    main()
