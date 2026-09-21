"""
models.py
Domain Entities and Value Objects for Order Management.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
from enum import Enum
from functools import total_ordering
from typing import List, Dict, Any, Optional
import re

from .exceptions import (
    ValidationError,
    InvalidOrderStateError,
    EmptyOrderError,
)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class OrderStatus(str, Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    PAID = "PAID"
    PROCESSING = "PROCESSING"
    SHIPPED = "SHIPPED"
    DELIVERED = "DELIVERED"
    CANCELLED = "CANCELLED"


class CustomerTier(str, Enum):
    STANDARD = "STANDARD"      # 0% discount
    VIP = "VIP"                # 10% discount
    ENTERPRISE = "ENTERPRISE"  # 15% discount


@total_ordering
class Money:
    """Immutable monetary Value Object preventing float precision issues."""

    def __init__(self, amount: Any, currency: str = "USD") -> None:
        if not currency or not isinstance(currency, str):
            raise ValidationError("Currency must be a non-empty string.")
        try:
            self._amount = Decimal(str(amount)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        except Exception as err:
            raise ValidationError(f"Invalid monetary value: {amount!r}") from err
        self._currency = currency.strip().upper()

    @property
    def amount(self) -> Decimal:
        return self._amount

    @property
    def currency(self) -> str:
        return self._currency

    def __repr__(self) -> str:
        return f"Money('{self._amount}', '{self._currency}')"

    def __str__(self) -> str:
        symbols = {"USD": "$", "EUR": "€", "GBP": "£", "INR": "₹"}
        sym = symbols.get(self._currency, f"{self._currency} ")
        return f"{sym}{self._amount:,.2f}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        return self._currency == other._currency and self._amount == other._amount

    def __hash__(self) -> int:
        return hash((self._amount, self._currency))

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValidationError(f"Cannot compare {self._currency} with {other._currency}.")
        return self._amount < other._amount

    def __add__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValidationError(f"Cannot add {self._currency} and {other._currency}.")
        return Money(self._amount + other._amount, self._currency)

    def __sub__(self, other: object) -> Money:
        if not isinstance(other, Money):
            return NotImplemented
        if self._currency != other._currency:
            raise ValidationError(f"Cannot subtract {self._currency} and {other._currency}.")
        return Money(self._amount - other._amount, self._currency)

    def __mul__(self, factor: Any) -> Money:
        try:
            scalar = Decimal(str(factor))
        except Exception:
            return NotImplemented
        return Money(self._amount * scalar, self._currency)

    def __rmul__(self, factor: Any) -> Money:
        return self.__mul__(factor)


@dataclass
class Customer:
    """Customer entity eligible to place orders."""
    customer_id: str
    name: str
    email: str
    tier: CustomerTier = CustomerTier.STANDARD
    is_active: bool = True

    def __post_init__(self) -> None:
        self.customer_id = self.customer_id.strip().upper()
        if not self.customer_id:
            raise ValidationError("customer_id cannot be empty.")
        self.name = self.name.strip()
        if not self.name:
            raise ValidationError("Customer name cannot be empty.")
        self.email = self.email.strip().lower()
        if not EMAIL_REGEX.match(self.email):
            raise ValidationError(f"Invalid email address: {self.email!r}")
        if isinstance(self.tier, str):
            self.tier = CustomerTier(self.tier)

    @property
    def discount_percentage(self) -> float:
        """Discount applicable to customer based on membership tier."""
        if self.tier == CustomerTier.VIP:
            return 0.10
        elif self.tier == CustomerTier.ENTERPRISE:
            return 0.15
        return 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "tier": self.tier.value,
            "is_active": self.is_active,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Customer:
        return cls(
            customer_id=data["customer_id"],
            name=data["name"],
            email=data["email"],
            tier=CustomerTier(data.get("tier", "STANDARD")),
            is_active=bool(data.get("is_active", True)),
        )


@dataclass
class OrderItem:
    """Line item within an order."""
    product_id: str
    product_name: str
    unit_price: Money
    quantity: int

    def __post_init__(self) -> None:
        self.product_id = self.product_id.strip().upper()
        if not self.product_id:
            raise ValidationError("product_id cannot be empty.")
        self.product_name = self.product_name.strip()
        if not self.product_name:
            raise ValidationError("product_name cannot be empty.")
        if not isinstance(self.unit_price, Money):
            self.unit_price = Money(self.unit_price)
        if self.unit_price < Money("0.00", self.unit_price.currency):
            raise ValidationError("unit_price cannot be negative.")
        if self.quantity <= 0:
            raise ValidationError(f"Quantity must be greater than zero. Received: {self.quantity}")

    def subtotal(self) -> Money:
        return self.unit_price * self.quantity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "product_id": self.product_id,
            "product_name": self.product_name,
            "unit_price": str(self.unit_price.amount),
            "currency": self.unit_price.currency,
            "quantity": self.quantity,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> OrderItem:
        return cls(
            product_id=data["product_id"],
            product_name=data["product_name"],
            unit_price=Money(data["unit_price"], data.get("currency", "USD")),
            quantity=int(data["quantity"]),
        )


class Order:
    """Aggregate Root managing line items, pricing, and lifecycle transitions."""

    def __init__(
        self,
        order_id: str,
        customer_id: str,
        items: Optional[List[OrderItem]] = None,
        status: OrderStatus = OrderStatus.PENDING,
        discount_rate: float = 0.0,
        shipping_fee: Optional[Money] = None,
        created_at: Optional[datetime] = None,
        tracking_number: Optional[str] = None,
        notes: str = "",
    ) -> None:
        self._order_id = order_id.strip().upper()
        if not self._order_id:
            raise ValidationError("Order ID cannot be empty.")
        self._customer_id = customer_id.strip().upper()
        if not self._customer_id:
            raise ValidationError("Customer ID cannot be empty.")

        self._items: List[OrderItem] = list(items) if items else []
        self._status = OrderStatus(status) if isinstance(status, str) else status
        self._discount_rate = max(0.0, float(discount_rate))
        self._shipping_fee = shipping_fee or Money("0.00", "USD")
        self._created_at = created_at or datetime.now()
        self._tracking_number = tracking_number
        self._notes = notes

    @property
    def order_id(self) -> str:
        return self._order_id

    @property
    def customer_id(self) -> str:
        return self._customer_id

    @property
    def items(self) -> List[OrderItem]:
        return list(self._items)

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def discount_rate(self) -> float:
        return self._discount_rate

    @discount_rate.setter
    def discount_rate(self, value: float) -> None:
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStateError("Cannot change discount rate on a non-pending order.")
        self._discount_rate = max(0.0, float(value))

    @property
    def shipping_fee(self) -> Money:
        return self._shipping_fee

    @shipping_fee.setter
    def shipping_fee(self, fee: Money) -> None:
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStateError("Cannot change shipping fee on a non-pending order.")
        self._shipping_fee = fee

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def tracking_number(self) -> Optional[str]:
        return self._tracking_number

    # ─────────────────────────────────────────────────────────────────────────
    # Line Item Operations (Invariants enforced)
    # ─────────────────────────────────────────────────────────────────────────

    def add_item(self, item: OrderItem) -> None:
        """Add item or increment quantity if already present."""
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStateError(
                f"Cannot modify items on order with status '{self._status.value}'. Must be PENDING."
            )
        for existing in self._items:
            if existing.product_id == item.product_id:
                existing.quantity += item.quantity
                return
        self._items.append(item)

    def remove_item(self, product_id: str) -> bool:
        """Remove a product line item from the order."""
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStateError(
                f"Cannot remove items from order with status '{self._status.value}'."
            )
        pid = product_id.strip().upper()
        for i, item in enumerate(self._items):
            if item.product_id == pid:
                del self._items[i]
                return True
        return False

    # ─────────────────────────────────────────────────────────────────────────
    # Calculations
    # ─────────────────────────────────────────────────────────────────────────

    def calculate_subtotal(self) -> Money:
        currency = self._items[0].unit_price.currency if self._items else "USD"
        total = Money("0.00", currency)
        for item in self._items:
            total = total + item.subtotal()
        return total

    def calculate_discount(self) -> Money:
        subtotal = self.calculate_subtotal()
        return subtotal * self._discount_rate

    def calculate_total(self) -> Money:
        subtotal = self.calculate_subtotal()
        discount = self.calculate_discount()
        return (subtotal - discount) + self._shipping_fee

    # ─────────────────────────────────────────────────────────────────────────
    # State Machine Transitions
    # ─────────────────────────────────────────────────────────────────────────

    def confirm(self) -> None:
        """Transition PENDING -> CONFIRMED."""
        if self._status != OrderStatus.PENDING:
            raise InvalidOrderStateError(f"Cannot confirm order in state '{self._status.value}'.")
        if not self._items:
            raise EmptyOrderError(f"Cannot confirm order {self._order_id} with 0 items.")
        self._status = OrderStatus.CONFIRMED

    def pay(self) -> None:
        """Transition CONFIRMED -> PAID."""
        if self._status != OrderStatus.CONFIRMED:
            raise InvalidOrderStateError(
                f"Cannot pay for order in state '{self._status.value}'. Must be CONFIRMED first."
            )
        self._status = OrderStatus.PAID

    def ship(self, tracking_number: str) -> None:
        """Transition PAID -> SHIPPED."""
        if self._status != OrderStatus.PAID:
            raise InvalidOrderStateError(
                f"Cannot ship unpaid order (current status: '{self._status.value}')."
            )
        if not tracking_number or not tracking_number.strip():
            raise ValidationError("Tracking number is required to ship an order.")
        self._tracking_number = tracking_number.strip().upper()
        self._status = OrderStatus.SHIPPED

    def deliver(self) -> None:
        """Transition SHIPPED -> DELIVERED."""
        if self._status != OrderStatus.SHIPPED:
            raise InvalidOrderStateError(
                f"Cannot mark order as delivered from state '{self._status.value}'."
            )
        self._status = OrderStatus.DELIVERED

    def cancel(self, reason: str = "") -> None:
        """Transition to CANCELLED. Forbidden once shipped or delivered."""
        if self._status in (OrderStatus.SHIPPED, OrderStatus.DELIVERED):
            raise InvalidOrderStateError(
                f"Cannot cancel order {self._order_id} that has already reached '{self._status.value}'."
            )
        if self._status == OrderStatus.CANCELLED:
            raise InvalidOrderStateError(f"Order {self._order_id} is already cancelled.")

        self._status = OrderStatus.CANCELLED
        if reason:
            self._notes = f"{self._notes} | Cancel reason: {reason}".strip(" | ")

    # ─────────────────────────────────────────────────────────────────────────
    # Serialization
    # ─────────────────────────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        return {
            "order_id": self._order_id,
            "customer_id": self._customer_id,
            "status": self._status.value,
            "discount_rate": self._discount_rate,
            "shipping_fee": str(self._shipping_fee.amount),
            "currency": self._shipping_fee.currency,
            "created_at": self._created_at.isoformat(),
            "tracking_number": self._tracking_number,
            "notes": self._notes,
            "items": [item.to_dict() for item in self._items],
            "subtotal": str(self.calculate_subtotal().amount),
            "discount": str(self.calculate_discount().amount),
            "total": str(self.calculate_total().amount),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Order:
        items = [OrderItem.from_dict(i) for i in data.get("items", [])]
        currency = data.get("currency", "USD")
        shipping = Money(data.get("shipping_fee", "0.00"), currency)

        return cls(
            order_id=data["order_id"],
            customer_id=data["customer_id"],
            items=items,
            status=OrderStatus(data.get("status", "PENDING")),
            discount_rate=float(data.get("discount_rate", 0.0)),
            shipping_fee=shipping,
            created_at=datetime.fromisoformat(data["created_at"]),
            tracking_number=data.get("tracking_number"),
            notes=data.get("notes", ""),
        )

    def __repr__(self) -> str:
        return (
            f"Order({self._order_id}, Customer={self._customer_id}, "
            f"Items={len(self._items)}, Total={self.calculate_total()}, Status={self._status.value})"
        )
