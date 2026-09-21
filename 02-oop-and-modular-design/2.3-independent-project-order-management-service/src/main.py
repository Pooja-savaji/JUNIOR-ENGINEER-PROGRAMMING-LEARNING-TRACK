"""
main.py
Composition Root for Order Management System.
Wires repositories, injects service dependencies, seeds data, and boots CLI.
"""

from __future__ import annotations
import sys
import os

# Ensure package is resolvable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from order_service.domain.models import Customer, Order, CustomerTier
from order_service.repositories.json_file import JsonFileRepository
from order_service.services.order_service import OrderService
from order_service.cli.cli_app import OrderConsoleApp


def seed_demo_data(service: OrderService) -> None:
    """Pre-populate sample customers and orders if catalog is fresh."""
    if service.list_customers():
        return

    print("  [INIT] Seeding sample customers...")
    service.register_customer("CUST-001", "Acme Corporation", "purchasing@acme.com", CustomerTier.STANDARD)
    service.register_customer("CUST-002", "Bob Jones", "bob.jones@deltaiot.com", CustomerTier.VIP)
    service.register_customer("CUST-003", "MegaCorp Global", "supply@megacorp.com", CustomerTier.ENTERPRISE)


def build_app() -> OrderConsoleApp:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    customer_repo = JsonFileRepository[Customer](
        file_path=os.path.join(data_dir, "customers.json"),
        id_getter=lambda c: c.customer_id,
        to_dict_fn=lambda c: c.to_dict(),
        from_dict_fn=Customer.from_dict,
    )

    order_repo = JsonFileRepository[Order](
        file_path=os.path.join(data_dir, "orders.json"),
        id_getter=lambda o: o.order_id,
        to_dict_fn=lambda o: o.to_dict(),
        from_dict_fn=Order.from_dict,
    )

    service = OrderService(order_repo=order_repo, customer_repo=customer_repo)
    seed_demo_data(service)
    return OrderConsoleApp(service)


def main():
    app = build_app()
    if "--demo" in sys.argv:
        app.run_demo()
    else:
        app.run_menu()


if __name__ == "__main__":
    main()
