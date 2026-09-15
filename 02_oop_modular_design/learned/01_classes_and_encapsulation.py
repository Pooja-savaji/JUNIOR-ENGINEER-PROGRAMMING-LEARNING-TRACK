"""
01_classes_and_encapsulation.py
================================
Module 2: Object-Oriented Programming & Modular Design
Topic: Classes, State, Encapsulation, Properties, and Class Registries

Concepts Covered:
  - Instance state vs. Class state (`self` vs. `cls`)
  - Public, protected (`_`), and private (`__`) naming conventions
  - Encapsulation using `@property` and `@<prop>.setter`
  - Strict input validation, state transitions, and business invariants
  - Class-level registry tracking all instances and aggregate metrics
  - Safe, atomic financial transfers with rollback semantics
"""

from __future__ import annotations
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict, Tuple


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    CLOSED = "CLOSED"


class TransactionType(Enum):
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"
    TRANSFER_OUT = "TRANSFER_OUT"
    TRANSFER_IN = "TRANSFER_IN"
    FEE = "FEE"


class TransactionRecord:
    """Immutable audit record for a single financial transaction."""

    def __init__(
        self,
        tx_id: str,
        tx_type: TransactionType,
        amount: float,
        balance_after: float,
        description: str = "",
        timestamp: Optional[datetime] = None,
    ) -> None:
        self._tx_id: str = tx_id
        self._tx_type: TransactionType = tx_type
        self._amount: float = round(float(amount), 2)
        self._balance_after: float = round(float(balance_after), 2)
        self._description: str = description
        self._timestamp: datetime = timestamp or datetime.now()

    @property
    def tx_id(self) -> str:
        return self._tx_id

    @property
    def tx_type(self) -> TransactionType:
        return self._tx_type

    @property
    def amount(self) -> float:
        return self._amount

    @property
    def balance_after(self) -> float:
        return self._balance_after

    @property
    def description(self) -> str:
        return self._description

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __repr__(self) -> str:
        return (
            f"TransactionRecord(id={self._tx_id!r}, type={self._tx_type.value}, "
            f"amount={self._amount:.2f}, balance={self._balance_after:.2f})"
        )


class BankAccount:
    """Production-grade Bank Account demonstrating encapsulation and state invariants.

    Class Attributes:
        _accounts_registry: Mapping of account_number -> BankAccount instance
        _total_reserves: Running tally of all funds held across all accounts
        _next_tx_sequence: Global sequence for unique transaction IDs
    """

    # Class-level state (Institutional ledger)
    _accounts_registry: Dict[str, BankAccount] = {}
    _total_reserves: float = 0.0
    _next_tx_sequence: int = 1000

    def __init__(
        self,
        account_number: str,
        holder_name: str,
        initial_deposit: float = 0.0,
        overdraft_limit: float = 0.0,
    ) -> None:
        # Validate account number uniqueness
        if not account_number or not isinstance(account_number, str):
            raise ValueError("Account number must be a non-empty string.")
        acc_clean = account_number.strip().upper()
        if acc_clean in BankAccount._accounts_registry:
            raise ValueError(f"Account number {account_number!r} already exists.")

        self._account_number: str = acc_clean
        self._holder_name: str = ""
        self.holder_name = holder_name  # triggers property setter validation

        if overdraft_limit < 0:
            raise ValueError("Overdraft limit cannot be negative.")
        self._overdraft_limit: float = round(float(overdraft_limit), 2)

        self._balance: float = 0.0
        self._status: AccountStatus = AccountStatus.ACTIVE
        self._transactions: List[TransactionRecord] = []
        self._created_at: datetime = datetime.now()

        # Execute initial deposit if provided
        if initial_deposit > 0:
            self._apply_balance_change(
                TransactionType.DEPOSIT,
                initial_deposit,
                "Initial opening deposit",
            )

        # Register account in class registry
        BankAccount._accounts_registry[self._account_number] = self

    # ─────────────────────────────────────────────────────────────────────────
    # Properties & Setters (Controlled Encapsulation)
    # ─────────────────────────────────────────────────────────────────────────

    @property
    def account_number(self) -> str:
        """Read-only account identifier."""
        return self._account_number

    @property
    def holder_name(self) -> str:
        """Account holder's legal name."""
        return self._holder_name

    @holder_name.setter
    def holder_name(self, value: str) -> None:
        if not value or not isinstance(value, str) or not value.strip():
            raise ValueError("Holder name must be a non-empty string.")
        self._holder_name = value.strip()

    @property
    def balance(self) -> float:
        """Read-only balance. Modifications must go through deposit/withdraw."""
        return round(self._balance, 2)

    @property
    def available_funds(self) -> float:
        """Total funds available including approved overdraft."""
        if self._status != AccountStatus.ACTIVE:
            return 0.0
        return round(self._balance + self._overdraft_limit, 2)

    @property
    def overdraft_limit(self) -> float:
        return self._overdraft_limit

    @property
    def status(self) -> AccountStatus:
        return self._status

    @property
    def transactions(self) -> List[TransactionRecord]:
        """Return defensive shallow copy to prevent external mutation."""
        return list(self._transactions)

    # ─────────────────────────────────────────────────────────────────────────
    # Internal Mutators & Helpers
    # ─────────────────────────────────────────────────────────────────────────

    def _next_tx_id(self) -> str:
        BankAccount._next_tx_sequence += 1
        return f"TX-{BankAccount._next_tx_sequence}"

    def _apply_balance_change(
        self,
        tx_type: TransactionType,
        amount: float,
        description: str,
    ) -> TransactionRecord:
        """Single internal bottleneck for all balance mutations."""
        amount = round(float(amount), 2)
        if tx_type in (TransactionType.DEPOSIT, TransactionType.TRANSFER_IN):
            self._balance += amount
            BankAccount._total_reserves += amount
        else:
            self._balance -= amount
            BankAccount._total_reserves -= amount

        tx = TransactionRecord(
            tx_id=self._next_tx_id(),
            tx_type=tx_type,
            amount=amount,
            balance_after=self._balance,
            description=description,
        )
        self._transactions.append(tx)
        return tx

    # ─────────────────────────────────────────────────────────────────────────
    # Public Operations & Invariant Enforcement
    # ─────────────────────────────────────────────────────────────────────────

    def deposit(self, amount: float, description: str = "Deposit") -> TransactionRecord:
        """Deposit funds into the account with strict validation."""
        if self._status != AccountStatus.ACTIVE:
            raise ValueError(f"Cannot deposit to account with status: {self._status.value}")
        if amount <= 0:
            raise ValueError(f"Deposit amount must be positive. Received: {amount}")

        return self._apply_balance_change(TransactionType.DEPOSIT, amount, description)

    def withdraw(self, amount: float, description: str = "Withdrawal") -> TransactionRecord:
        """Withdraw funds ensuring overdraft bounds are respected."""
        if self._status != AccountStatus.ACTIVE:
            raise ValueError(f"Cannot withdraw from account with status: {self._status.value}")
        if amount <= 0:
            raise ValueError(f"Withdrawal amount must be positive. Received: {amount}")

        amount = round(float(amount), 2)
        if amount > self.available_funds:
            raise ValueError(
                f"Insufficient funds. Requested: ${amount:.2f}, Available: ${self.available_funds:.2f} "
                f"(Balance: ${self._balance:.2f}, Overdraft Limit: ${self._overdraft_limit:.2f})"
            )

        return self._apply_balance_change(TransactionType.WITHDRAWAL, amount, description)

    def transfer(
        self,
        recipient: BankAccount,
        amount: float,
        note: str = "P2P Transfer",
    ) -> Tuple[TransactionRecord, TransactionRecord]:
        """Atomically transfer funds to another account.

        Guarantees that either both debit and credit succeed, or neither takes effect.
        """
        if not isinstance(recipient, BankAccount):
            raise TypeError("Recipient must be a valid BankAccount instance.")
        if recipient.account_number == self.account_number:
            raise ValueError("Cannot transfer funds to the same account.")
        if self._status != AccountStatus.ACTIVE:
            raise ValueError(f"Source account {self.account_number} is not ACTIVE.")
        if recipient.status != AccountStatus.ACTIVE:
            raise ValueError(f"Recipient account {recipient.account_number} is not ACTIVE.")
        if amount <= 0:
            raise ValueError(f"Transfer amount must be positive. Received: {amount}")

        amount = round(float(amount), 2)
        if amount > self.available_funds:
            raise ValueError(
                f"Transfer failed: insufficient funds in account {self.account_number}."
            )

        # Debit source
        debit_tx = self._apply_balance_change(
            TransactionType.TRANSFER_OUT,
            amount,
            f"Transfer to {recipient.account_number} - {note}",
        )

        try:
            # Credit destination
            credit_tx = recipient._apply_balance_change(
                TransactionType.TRANSFER_IN,
                amount,
                f"Transfer from {self.account_number} - {note}",
            )
        except Exception as err:
            # Rollback debit if credit fails unexpectedly
            self._apply_balance_change(
                TransactionType.DEPOSIT,
                amount,
                f"ROLLBACK: Transfer to {recipient.account_number} failed",
            )
            raise RuntimeError(f"Transfer rolled back due to error: {err}") from err

        return debit_tx, credit_tx

    def suspend(self, reason: str = "") -> None:
        """Suspend account activity."""
        if self._status == AccountStatus.CLOSED:
            raise ValueError("Cannot suspend a closed account.")
        self._status = AccountStatus.SUSPENDED

    def reactivate(self) -> None:
        """Reactivate a suspended account."""
        if self._status == AccountStatus.CLOSED:
            raise ValueError("Cannot reactivate a closed account.")
        self._status = AccountStatus.ACTIVE

    def close(self) -> None:
        """Close account if balance is zero."""
        if round(self._balance, 2) != 0.0:
            raise ValueError(
                f"Cannot close account with non-zero balance (${self._balance:.2f}). "
                "Please withdraw or transfer all funds before closing."
            )
        self._status = AccountStatus.CLOSED

    # ─────────────────────────────────────────────────────────────────────────
    # Class-Level Inquiries & Reporting
    # ─────────────────────────────────────────────────────────────────────────

    @classmethod
    def get_account(cls, account_number: str) -> Optional[BankAccount]:
        """Look up an account by its account number from the registry."""
        return cls._accounts_registry.get(account_number.strip().upper())

    @classmethod
    def total_liquidity(cls) -> float:
        """Total reserves currently held across all bank accounts."""
        return round(cls._total_reserves, 2)

    @classmethod
    def active_account_count(cls) -> int:
        """Count of accounts in ACTIVE status."""
        return sum(1 for acc in cls._accounts_registry.values() if acc.status == AccountStatus.ACTIVE)

    @classmethod
    def reset_registry(cls) -> None:
        """Utility for test suites to clear registry."""
        cls._accounts_registry.clear()
        cls._total_reserves = 0.0
        cls._next_tx_sequence = 1000

    def print_statement(self) -> None:
        """Print a formatted bank account statement."""
        w = 64
        print("=" * w)
        print(f"  STATEMENT: {self._account_number}  [{self._status.value}]")
        print(f"  Holder    : {self._holder_name}")
        print(f"  Balance   : ${self._balance:>10.2f}")
        print(f"  Overdraft : ${self._overdraft_limit:>10.2f}")
        print(f"  Available : ${self.available_funds:>10.2f}")
        print("-" * w)
        print(f"  {'TX ID':<10} {'TYPE':<14} {'AMOUNT':>10} {'BALANCE':>10}  {'NOTE'}")
        print("-" * w)
        for tx in self._transactions:
            sign = "+" if tx.tx_type in (TransactionType.DEPOSIT, TransactionType.TRANSFER_IN) else "-"
            print(
                f"  {tx.tx_id:<10} {tx.tx_type.value:<14} "
                f"{sign}${tx.amount:>8.2f} ${tx.balance_after:>9.2f}  {tx.description[:20]}"
            )
        print("=" * w)

    def __repr__(self) -> str:
        return (
            f"BankAccount(acc={self._account_number!r}, holder={self._holder_name!r}, "
            f"balance={self._balance:.2f}, status={self._status.value})"
        )


def main():
    print("=" * 64)
    print("  EXERCISE 01: CLASSES & ENCAPSULATION")
    print("=" * 64)

    # 1. Create accounts
    print("\n[1] Creating Accounts...")
    alice = BankAccount("ACC-101", "Alice Smith", initial_deposit=1000.0, overdraft_limit=200.0)
    bob = BankAccount("ACC-102", "Bob Jones", initial_deposit=500.0, overdraft_limit=0.0)
    carol = BankAccount("ACC-103", "Carol White", initial_deposit=2500.0)

    print(f"  Created: {alice}")
    print(f"  Created: {bob}")
    print(f"  Created: {carol}")
    print(f"  Total Institutional Liquidity: ${BankAccount.total_liquidity():,.2f}")
    print(f"  Active Accounts Count: {BankAccount.active_account_count()}")

    # 2. Regular operations
    print("\n[2] Executing Deposits and Withdrawals...")
    alice.deposit(350.0, "Consulting fee")
    bob.withdraw(150.0, "Groceries payment")
    print(f"  Alice balance: ${alice.balance:.2f}")
    print(f"  Bob balance  : ${bob.balance:.2f}")

    # 3. Overdraft utilization
    print("\n[3] Overdraft Demonstration...")
    print(f"  Bob available funds: ${bob.available_funds:.2f}")
    try:
        bob.withdraw(400.0, "Excessive purchase")
    except ValueError as e:
        print(f"  [Expected Error Caught] Bob overdraft prevented: {e}")

    print(f"  Alice balance: ${alice.balance:.2f}, Overdraft limit: ${alice.overdraft_limit:.2f}")
    alice.withdraw(1400.0, "Emergency car repair")
    print(f"  Alice new balance: ${alice.balance:.2f} (Using overdraft! Available: ${alice.available_funds:.2f})")

    # 4. Atomic transfer
    print("\n[4] Safe P2P Transfer...")
    carol.transfer(bob, 300.0, "Dinner split reimbursement")
    print(f"  Carol balance after transfer: ${carol.balance:.2f}")
    print(f"  Bob balance after receipt   : ${bob.balance:.2f}")

    # 5. Account lookup from registry
    print("\n[5] Class Registry Lookup...")
    looked_up = BankAccount.get_account("ACC-102")
    print(f"  Registry lookup for 'ACC-102': {looked_up}")

    # 6. Print statement
    print("\n[6] Detailed Account Statements...")
    alice.print_statement()
    bob.print_statement()

    print(f"\nFinal Bank Reserves: ${BankAccount.total_liquidity():,.2f}")
    print("Classes & Encapsulation demonstration complete!\n")


if __name__ == "__main__":
    main()
