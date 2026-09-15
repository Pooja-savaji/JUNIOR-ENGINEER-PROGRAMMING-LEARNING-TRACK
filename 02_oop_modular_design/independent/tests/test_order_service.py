"""
test_order_service.py
Comprehensive Unit Test Suite for OrderService using MockRepository.
"""

import unittest
from decimal import Decimal

from order_service.domain.models import (
    Customer,
    Order,
    OrderItem,
    CustomerTier,
    OrderStatus,
    Money,
)
from order_service.domain.exceptions import (
    OrderNotFoundError,
    CustomerNotFoundError,
    InvalidOrderStateError,
    EmptyOrderError,
    ValidationError,
)
from order_service.repositories.in_memory import MockRepository
from order_service.services.order_service import OrderService


class TestOrderService(unittest.TestCase):
    """Hermetic unit tests verifying business rules, state machine, and pricing."""

    def setUp(self) -> None:
        self.order_repo = MockRepository[Order](id_getter=lambda o: o.order_id)
        self.customer_repo = MockRepository[Customer](id_getter=lambda c: c.customer_id)
        self.service = OrderService(self.order_repo, self.customer_repo)

        # Create standard and VIP customers
        self.standard_cust = self.service.register_customer(
            "CUST-01", "Standard Sam", "sam@example.com", CustomerTier.STANDARD
        )
        self.vip_cust = self.service.register_customer(
            "CUST-02", "VIP Valerie", "val@example.com", CustomerTier.VIP
        )

    def test_money_value_object_arithmetic_and_equality(self):
        m1 = Money("50.25", "USD")
        m2 = Money("25.50", "USD")
        self.assertEqual(m1 + m2, Money("75.75", "USD"))
        self.assertEqual(m1 - m2, Money("24.75", "USD"))
        self.assertEqual(m1 * 2, Money("100.50", "USD"))
        self.assertTrue(m1 > m2)

    def test_customer_tier_discounts_applied_to_order(self):
        # Standard customer: 0% discount
        ord1 = self.service.create_order("CUST-01")
        self.assertEqual(ord1.discount_rate, 0.0)

        # VIP customer: 10% discount
        ord2 = self.service.create_order("CUST-02")
        self.assertEqual(ord2.discount_rate, 0.10)

    def test_add_and_remove_items(self):
        order = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 10.00, 2)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.calculate_subtotal(), Money("20.00", "USD"))

        # Add duplicate item: quantity merges
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 10.00, 3)
        self.assertEqual(len(order.items), 1)
        self.assertEqual(order.items[0].quantity, 5)
        self.assertEqual(order.calculate_subtotal(), Money("50.00", "USD"))

        # Remove item
        self.service.remove_item_from_order(order.order_id, "P-1")
        self.assertEqual(len(order.items), 0)

    def test_pricing_calculation_with_discount_and_shipping(self):
        # VIP order: $100 subtotal, 10% discount ($10), $5 shipping -> $95 total
        order = self.service.create_order("CUST-02", shipping_fee=5.00)
        self.service.add_item_to_order(order.order_id, "P-100", "Gadget", 50.00, 2)

        self.assertEqual(order.calculate_subtotal(), Money("100.00", "USD"))
        self.assertEqual(order.calculate_discount(), Money("10.00", "USD"))
        self.assertEqual(order.calculate_total(), Money("95.00", "USD"))

    def test_cannot_confirm_empty_order(self):
        order = self.service.create_order("CUST-01")
        with self.assertRaises(EmptyOrderError):
            self.service.confirm_order(order.order_id)

    def test_cannot_modify_items_after_confirmation(self):
        order = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 10.00, 1)
        self.service.confirm_order(order.order_id)

        # Cannot add item to confirmed order
        with self.assertRaises(InvalidOrderStateError):
            self.service.add_item_to_order(order.order_id, "P-2", "Gizmo", 15.00, 1)

        # Cannot remove item
        with self.assertRaises(InvalidOrderStateError):
            self.service.remove_item_from_order(order.order_id, "P-1")

    def test_full_successful_order_lifecycle(self):
        order = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 25.00, 1)

        # PENDING -> CONFIRMED
        self.service.confirm_order(order.order_id)
        self.assertEqual(order.status, OrderStatus.CONFIRMED)

        # CONFIRMED -> PAID
        self.service.pay_order(order.order_id)
        self.assertEqual(order.status, OrderStatus.PAID)

        # PAID -> SHIPPED
        self.service.ship_order(order.order_id, "TRACK-12345")
        self.assertEqual(order.status, OrderStatus.SHIPPED)
        self.assertEqual(order.tracking_number, "TRACK-12345")

        # SHIPPED -> DELIVERED
        self.service.deliver_order(order.order_id)
        self.assertEqual(order.status, OrderStatus.DELIVERED)

    def test_cannot_ship_unpaid_order(self):
        order = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 25.00, 1)
        self.service.confirm_order(order.order_id)

        with self.assertRaises(InvalidOrderStateError):
            self.service.ship_order(order.order_id, "TRACK-FAIL")

    def test_cannot_cancel_shipped_or_delivered_order(self):
        order = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order.order_id, "P-1", "Widget", 25.00, 1)
        self.service.confirm_order(order.order_id)
        self.service.pay_order(order.order_id)
        self.service.ship_order(order.order_id, "TRACK-999")

        # Cancelling after shipping must fail
        with self.assertRaises(InvalidOrderStateError):
            self.service.cancel_order(order.order_id, "Changed mind")

    def test_cancel_pending_and_paid_orders_succeeds(self):
        # Cancel pending order
        order1 = self.service.create_order("CUST-01")
        self.service.cancel_order(order1.order_id, "No longer needed")
        self.assertEqual(order1.status, OrderStatus.CANCELLED)

        # Cancel paid order
        order2 = self.service.create_order("CUST-01")
        self.service.add_item_to_order(order2.order_id, "P-1", "Widget", 10.00, 1)
        self.service.confirm_order(order2.order_id)
        self.service.pay_order(order2.order_id)
        self.service.cancel_order(order2.order_id, "Customer refund request")
        self.assertEqual(order2.status, OrderStatus.CANCELLED)

    def test_sales_analytics_calculation(self):
        # Order 1: Paid ($100)
        o1 = self.service.create_order("CUST-01")
        self.service.add_item_to_order(o1.order_id, "P-1", "Item A", 100.00, 1)
        self.service.confirm_order(o1.order_id)
        self.service.pay_order(o1.order_id)

        # Order 2: Cancelled (should not count towards gross revenue)
        o2 = self.service.create_order("CUST-01")
        self.service.add_item_to_order(o2.order_id, "P-2", "Item B", 200.00, 1)
        self.service.cancel_order(o2.order_id)

        analytics = self.service.calculate_sales_analytics()
        self.assertEqual(analytics["total_orders_placed"], 2)
        self.assertEqual(analytics["orders_settled"], 1)
        self.assertEqual(analytics["total_gross_revenue"], 100.0)


if __name__ == "__main__":
    unittest.main()
