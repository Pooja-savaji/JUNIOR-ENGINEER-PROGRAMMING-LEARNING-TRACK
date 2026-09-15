"""
cli_app.py
Interactive CLI and automated demo runner for Order Management System.
"""

from __future__ import annotations
from typing import Optional

from ..services.order_service import OrderService
from ..domain.models import CustomerTier, OrderStatus
from ..domain.exceptions import OrderManagementError


class OrderConsoleApp:
    """Terminal user interface for Order Management."""

    def __init__(self, service: OrderService) -> None:
        self.service = service

    def run_menu(self) -> None:
        while True:
            self._print_banner()
            print("  1. List All Orders")
            print("  2. Create New Draft Order")
            print("  3. Add Item to Order")
            print("  4. Confirm & Pay Order")
            print("  5. Ship Order with Tracking")
            print("  6. Cancel Order")
            print("  7. View Customer Orders")
            print("  8. Sales Analytics & Revenue Report")
            print("  9. Run Automated End-to-End Demo")
            print("  0. Exit")
            print("-" * 65)

            choice = input("Select an option [0-9]: ").strip()
            if choice == "1":
                self._handle_list_orders()
            elif choice == "2":
                self._handle_create_order()
            elif choice == "3":
                self._handle_add_item()
            elif choice == "4":
                self._handle_pay()
            elif choice == "5":
                self._handle_ship()
            elif choice == "6":
                self._handle_cancel()
            elif choice == "7":
                self._handle_customer_orders()
            elif choice == "8":
                self._handle_analytics()
            elif choice == "9":
                self.run_demo()
            elif choice == "0":
                print()
                print("Exiting Order Management System. Goodbye!")
                break
            else:
                print()
                print("[!] Invalid selection.")

    def _print_banner(self) -> None:
        print()
        print("=" * 65)
        print("  DELTA IOT — ENTERPRISE ORDER MANAGEMENT SERVICE")
        print("=" * 65)

    def _handle_list_orders(self) -> None:
        print()
        print("--- ORDER CATALOG ---")
        orders = self.service.list_orders()
        if not orders:
            print("  No orders recorded.")
            return

        w = 80
        print("-" * w)
        print(f"  {'ORDER ID':<14} {'CUSTOMER':<12} {'ITEMS':<6} {'STATUS':<14} {'TOTAL':>12}")
        print("-" * w)
        for o in orders:
            print(f"  {o.order_id:<14} {o.customer_id:<12} {len(o.items):<6} {o.status.value:<14} {str(o.calculate_total()):>12}")
        print("-" * w)

    def _handle_create_order(self) -> None:
        print()
        print("--- CREATE DRAFT ORDER ---")
        cid = input("Customer ID (e.g. CUST-001): ").strip()
        ship = input("Shipping fee (default: 0.00): ").strip() or "0.00"
        try:
            order = self.service.create_order(cid, shipping_fee=float(ship))
            print()
            print(f"[+] Draft order created: {order.order_id} (Customer discount rate: {order.discount_rate*100:.0f}%)")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_add_item(self) -> None:
        print()
        print("--- ADD ITEM TO ORDER ---")
        oid = input("Order ID: ").strip()
        pid = input("Product ID: ").strip()
        name = input("Product Name: ").strip()
        price = float(input("Unit Price: ").strip())
        qty = int(input("Quantity: ").strip())

        try:
            order = self.service.add_item_to_order(oid, pid, name, price, qty)
            print()
            print(f"[+] Added item to {oid}. Order total is now: {order.calculate_total()}")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_pay(self) -> None:
        print()
        print("--- CONFIRM & PAY ORDER ---")
        oid = input("Order ID: ").strip()
        try:
            self.service.confirm_order(oid)
            self.service.pay_order(oid)
            print()
            print(f"[+] Order {oid} successfully confirmed and PAID!")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_ship(self) -> None:
        print()
        print("--- SHIP ORDER ---")
        oid = input("Order ID: ").strip()
        tracking = input("Tracking Number (e.g. TRK-9901): ").strip()
        try:
            self.service.ship_order(oid, tracking)
            print()
            print(f"[+] Order {oid} marked as SHIPPED with tracking {tracking}.")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_cancel(self) -> None:
        print()
        print("--- CANCEL ORDER ---")
        oid = input("Order ID: ").strip()
        reason = input("Cancellation Reason: ").strip()
        try:
            self.service.cancel_order(oid, reason)
            print()
            print(f"[+] Order {oid} CANCELLED.")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_customer_orders(self) -> None:
        print()
        print("--- CUSTOMER ORDER LOOKUP ---")
        cid = input("Customer ID: ").strip()
        try:
            cust = self.service.get_customer(cid)
            orders = self.service.get_customer_orders(cid)
            print()
            print(f"Customer: {cust.name} ({cust.customer_id}) | Tier: {cust.tier.value} | Email: {cust.email}")
            print(f"Total Orders: {len(orders)}")
            for o in orders:
                print(f"  * {o.order_id}: {len(o.items)} items | Total: {o.calculate_total()} | Status: {o.status.value}")
        except OrderManagementError as err:
            print()
            print(f"[-] ERROR: {err}")

    def _handle_analytics(self) -> None:
        data = self.service.calculate_sales_analytics()
        print()
        print("=" * 65)
        print("  SALES & REVENUE PERFORMANCE METRICS")
        print("=" * 65)
        print(f"  Total Orders Placed     : {data['total_orders_placed']:>8}")
        print(f"  Settled Paid Orders     : {data['orders_settled']:>8}")
        print(f"  Gross Settled Revenue   : ${data['total_gross_revenue']:>11,.2f}")
        print(f"  Discounts Extended      : ${data['total_discounts_granted']:>11,.2f}")
        print(f"  Average Order Value     : ${data['average_order_value']:>11,.2f}")
        print("-" * 65)
        print("  Status Breakdown:")
        for st, cnt in data["orders_by_status"].items():
            print(f"    * {st:<15}: {cnt:>3} orders")
        print("=" * 65)

    def run_demo(self) -> None:
        """Automated end-to-end execution demonstrating all business logic and invariants."""
        print()
        print("=" * 65)
        print("  STARTING AUTOMATED ORDER MANAGEMENT DOMAIN WALKTHROUGH")
        print("=" * 65)

        # 1. Order creation with VIP discount
        print()
        print("[Step 1] Creating Order for VIP Customer Bob Jones (10% Tier Discount)...")
        order_vip = self.service.create_order("CUST-002", shipping_fee=15.00)
        print(f"  Created: {order_vip.order_id} (Discount rate applied: {order_vip.discount_rate*100:.0f}%)")

        # 2. Add items
        print()
        print("[Step 2] Adding Items to Order:")
        self.service.add_item_to_order(order_vip.order_id, "PROD-A", "IoT Gateway Gateway Node", 250.00, 2)
        self.service.add_item_to_order(order_vip.order_id, "PROD-B", "Industrial Temperature Sensor", 45.00, 4)

        subtotal = order_vip.calculate_subtotal()
        discount = order_vip.calculate_discount()
        total = order_vip.calculate_total()
        print(f"  Subtotal (2x $250 + 4x $45) : {subtotal}")
        print(f"  VIP Discount (10%)          : -{discount}")
        print(f"  Shipping Fee                : +{order_vip.shipping_fee}")
        print(f"  Net Total Due               : {total}")

        # 3. State Invariant: Cannot confirm empty order
        print()
        print("[Step 3] Invariant Check: Confirming Empty Order...")
        empty_order = self.service.create_order("CUST-001")
        try:
            self.service.confirm_order(empty_order.order_id)
        except OrderManagementError as err:
            print(f"  [Expected Error Caught]: {err}")

        # 4. State Invariant: Cannot pay unconfirmed order
        print()
        print("[Step 4] Invariant Check: Paying unconfirmed order...")
        try:
            self.service.pay_order(order_vip.order_id)
        except OrderManagementError as err:
            print(f"  [Expected Error Caught]: {err}")

        # 5. Normal Order Flow: Confirm -> Pay -> Ship -> Deliver
        print()
        print("[Step 5] Progressing Order State Machine:")
        self.service.confirm_order(order_vip.order_id)
        print(f"  1. Confirmed : Status = {order_vip.status.value}")

        self.service.pay_order(order_vip.order_id)
        print(f"  2. Paid      : Status = {order_vip.status.value}")

        self.service.ship_order(order_vip.order_id, "FEDEX-998822")
        print(f"  3. Shipped   : Status = {order_vip.status.value} (Tracking: {order_vip.tracking_number})")

        self.service.deliver_order(order_vip.order_id)
        print(f"  4. Delivered : Status = {order_vip.status.value}")

        # 6. State Invariant: Cannot cancel shipped / delivered order
        print()
        print("[Step 6] Invariant Check: Attempting to cancel delivered order...")
        try:
            self.service.cancel_order(order_vip.order_id, "Customer changed mind")
        except OrderManagementError as err:
            print(f"  [Expected Error Caught]: {err}")

        # 7. Cancel a confirmed order
        print()
        print("[Step 7] Order Cancellation Workflow:")
        order_cancelable = self.service.create_order("CUST-001")
        self.service.add_item_to_order(order_cancelable.order_id, "PROD-C", "Sensor Cable 5m", 15.00, 1)
        self.service.confirm_order(order_cancelable.order_id)
        self.service.cancel_order(order_cancelable.order_id, "Customer requested cancellation")
        print(f"  Order {order_cancelable.order_id} successfully cancelled. Status = {order_cancelable.status.value}")

        # 8. Sales Analytics
        self._handle_analytics()

        print()
        print("End-to-End Walkthrough Complete!")
