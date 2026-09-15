"""
order_service.py
Application service orchestrating business use cases for orders and customers.
"""

from __future__ import annotations
from decimal import Decimal
from typing import Optional, List, Dict, Any
import uuid

from ..domain.models import Order, OrderItem, Customer, OrderStatus, CustomerTier, Money
from ..domain.exceptions import (
    OrderNotFoundError,
    CustomerNotFoundError,
    ValidationError,
)
from ..repositories.base import BaseRepository


class OrderService:
    """Core Business Service orchestrating order operations."""

    def __init__(
        self,
        order_repo: BaseRepository[Order],
        customer_repo: BaseRepository[Customer],
    ) -> None:
        self._order_repo = order_repo
        self._customer_repo = customer_repo

    # ─────────────────────────────────────────────────────────────────────────
    # Customer Use Cases
    # ─────────────────────────────────────────────────────────────────────────

    def register_customer(
        self, customer_id: str, name: str, email: str, tier: CustomerTier = CustomerTier.STANDARD
    ) -> Customer:
        if self._customer_repo.get_by_id(customer_id):
            raise ValidationError(f"Customer {customer_id!r} already exists.")
        cust = Customer(customer_id=customer_id, name=name, email=email, tier=tier)
        self._customer_repo.add(cust)
        return cust

    def get_customer(self, customer_id: str) -> Customer:
        cust = self._customer_repo.get_by_id(customer_id)
        if not cust:
            raise CustomerNotFoundError(f"Customer {customer_id!r} not found.")
        return cust

    def list_customers(self) -> List[Customer]:
        return self._customer_repo.list_all()

    # ─────────────────────────────────────────────────────────────────────────
    # Order Lifecycle Use Cases
    # ─────────────────────────────────────────────────────────────────────────

    def create_order(
        self, customer_id: str, shipping_fee: float = 0.0, currency: str = "USD"
    ) -> Order:
        """Start a new draft order, applying customer tier discounts automatically."""
        customer = self.get_customer(customer_id)
        if not customer.is_active:
            raise ValidationError(f"Cannot create orders for inactive customer {customer.name}.")

        order_id = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        order = Order(
            order_id=order_id,
            customer_id=customer.customer_id,
            discount_rate=customer.discount_percentage,
            shipping_fee=Money(shipping_fee, currency),
        )
        self._order_repo.add(order)
        return order

    def get_order(self, order_id: str) -> Order:
        order = self._order_repo.get_by_id(order_id)
        if not order:
            raise OrderNotFoundError(f"Order {order_id!r} not found.")
        return order

    def add_item_to_order(
        self,
        order_id: str,
        product_id: str,
        product_name: str,
        unit_price: float,
        quantity: int,
        currency: str = "USD",
    ) -> Order:
        """Add line item to order and save changes."""
        order = self.get_order(order_id)
        item = OrderItem(
            product_id=product_id,
            product_name=product_name,
            unit_price=Money(unit_price, currency),
            quantity=quantity,
        )
        order.add_item(item)
        self._order_repo.update(order)
        return order

    def remove_item_from_order(self, order_id: str, product_id: str) -> Order:
        order = self.get_order(order_id)
        removed = order.remove_item(product_id)
        if not removed:
            raise ValidationError(f"Product {product_id!r} not found in order {order_id}.")
        self._order_repo.update(order)
        return order

    def confirm_order(self, order_id: str) -> Order:
        order = self.get_order(order_id)
        order.confirm()
        self._order_repo.update(order)
        return order

    def pay_order(self, order_id: str) -> Order:
        order = self.get_order(order_id)
        order.pay()
        self._order_repo.update(order)
        return order

    def ship_order(self, order_id: str, tracking_number: str) -> Order:
        order = self.get_order(order_id)
        order.ship(tracking_number)
        self._order_repo.update(order)
        return order

    def deliver_order(self, order_id: str) -> Order:
        order = self.get_order(order_id)
        order.deliver()
        self._order_repo.update(order)
        return order

    def cancel_order(self, order_id: str, reason: str = "") -> Order:
        order = self.get_order(order_id)
        order.cancel(reason)
        self._order_repo.update(order)
        return order

    # ─────────────────────────────────────────────────────────────────────────
    # Queries and Reporting
    # ─────────────────────────────────────────────────────────────────────────

    def get_customer_orders(self, customer_id: str) -> List[Order]:
        self.get_customer(customer_id)
        return sorted(
            self._order_repo.find(lambda o: o.customer_id == customer_id.strip().upper()),
            key=lambda o: o.created_at,
            reverse=True,
        )

    def list_orders(self, status: Optional[OrderStatus] = None) -> List[Order]:
        if status:
            return self._order_repo.find(lambda o: o.status == status)
        return self._order_repo.list_all()

    def calculate_sales_analytics(self) -> Dict[str, Any]:
        """Aggregate sales metrics across non-cancelled orders."""
        orders = self._order_repo.list_all()
        total_orders = len(orders)
        by_status = {s.value: 0 for s in OrderStatus}
        total_gross_revenue = Decimal("0.00")
        total_discounts_granted = Decimal("0.00")

        for o in orders:
            by_status[o.status.value] += 1
            if o.status in (OrderStatus.PAID, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED):
                total_gross_revenue += o.calculate_total().amount
                total_discounts_granted += o.calculate_discount().amount

        settled_count = sum(
            by_status[s.value]
            for s in (OrderStatus.PAID, OrderStatus.PROCESSING, OrderStatus.SHIPPED, OrderStatus.DELIVERED)
        )
        avg_order_value = (total_gross_revenue / settled_count) if settled_count > 0 else Decimal("0.00")

        return {
            "total_orders_placed": total_orders,
            "orders_settled": settled_count,
            "total_gross_revenue": float(total_gross_revenue),
            "total_discounts_granted": float(total_discounts_granted),
            "average_order_value": float(round(avg_order_value, 2)),
            "orders_by_status": by_status,
        }
