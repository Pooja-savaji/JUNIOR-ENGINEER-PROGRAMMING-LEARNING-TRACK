"""
main.py
Application composition root: Wires repositories, seeds initial catalog if needed,
and boots the ConsoleApp interface.
"""

from __future__ import annotations
import sys
import os
from datetime import date

# Ensure asset_tracker is importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from asset_tracker.models.asset import Asset, HardwareAsset, SoftwareLicense, AssetCategory, AssetStatus
from asset_tracker.models.employee import Employee
from asset_tracker.models.assignment import AssignmentRecord
from asset_tracker.repositories.json_repo import JsonRepository
from asset_tracker.services.asset_service import AssetService
from asset_tracker.cli.console_app import ConsoleApp


def seed_initial_data(service: AssetService) -> None:
    """Pre-populate repository with standard enterprise dataset if empty."""
    if service.list_employees():
        return  # Data already exists

    print("  [INIT] Seeding initial employee and asset inventory data...")

    # Seed Employees
    service.register_employee("EMP-101", "Alice Smith", "alice.smith@deltaiot.com", "Engineering")
    service.register_employee("EMP-102", "Bob Jones", "bob.jones@deltaiot.com", "DevOps")
    service.register_employee("EMP-103", "Carol White", "carol.white@deltaiot.com", "Product")
    service.register_employee("EMP-104", "David Lee", "david.lee@deltaiot.com", "Security")

    # Seed Hardware
    service.register_hardware(
        asset_id="AST-1001",
        name="Lenovo ThinkPad X1 Carbon Gen 11",
        category=AssetCategory.LAPTOP,
        purchase_price=2100.00,
        purchase_date=date(2023, 3, 10),
        serial_number="LN-X1-99214",
        warranty_expiry=date(2026, 3, 10),
        lifespan_years=3,
        specs={"cpu": "i7-1365U", "ram_gb": 32, "storage_gb": 1000},
    )
    service.register_hardware(
        asset_id="AST-1002",
        name="Apple MacBook Pro 16 M3 Max",
        category=AssetCategory.LAPTOP,
        purchase_price=3499.00,
        purchase_date=date(2024, 1, 15),
        serial_number="APL-MBP-8831",
        warranty_expiry=date(2027, 1, 15),
        lifespan_years=4,
        specs={"chip": "M3 Max", "unified_memory_gb": 48, "storage_gb": 1000},
    )
    service.register_hardware(
        asset_id="AST-1003",
        name="Dell PowerEdge R750 Server",
        category=AssetCategory.SERVER,
        purchase_price=8200.00,
        purchase_date=date(2022, 6, 1),
        serial_number="DEL-PE-4410",
        warranty_expiry=date(2025, 6, 1),
        lifespan_years=5,
        specs={"cpu": "Dual Xeon Gold", "ram_gb": 256, "storage_tb": 16},
    )

    # Seed Software Licenses
    service.register_software_license(
        asset_id="AST-1004",
        name="JetBrains All Products Pack",
        purchase_price=799.00,
        purchase_date=date(2024, 1, 1),
        license_key="JB-ALL-8374-9921",
        total_seats=5,
        expiration_date=date(2028, 1, 1),
    )
    service.register_software_license(
        asset_id="AST-1005",
        name="Figma Enterprise Seat",
        purchase_price=540.00,
        purchase_date=date(2024, 2, 1),
        license_key="FIG-ENT-2024-0091",
        total_seats=2,
        expiration_date=date(2025, 2, 1),
    )


def build_application() -> ConsoleApp:
    """Composition root: instantiate repositories and wire services."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    # Polymorphic asset deserializer
    def asset_from_dict(d: dict) -> Asset:
        if d.get("type") == "SoftwareLicense" or d.get("category") == "SOFTWARE_LICENSE":
            return SoftwareLicense.from_dict(d)
        return HardwareAsset.from_dict(d)

    asset_repo = JsonRepository[Asset](
        file_path=os.path.join(data_dir, "assets.json"),
        id_getter=lambda a: a.asset_id,
        to_dict_fn=lambda a: a.to_dict(),
        from_dict_fn=asset_from_dict,
    )

    employee_repo = JsonRepository[Employee](
        file_path=os.path.join(data_dir, "employees.json"),
        id_getter=lambda e: e.emp_id,
        to_dict_fn=lambda e: e.to_dict(),
        from_dict_fn=Employee.from_dict,
    )

    assignment_repo = JsonRepository[AssignmentRecord](
        file_path=os.path.join(data_dir, "assignments.json"),
        id_getter=lambda a: a.assignment_id,
        to_dict_fn=lambda a: a.to_dict(),
        from_dict_fn=AssignmentRecord.from_dict,
    )

    service = AssetService(
        asset_repo=asset_repo,
        employee_repo=employee_repo,
        assignment_repo=assignment_repo,
    )

    seed_initial_data(service)
    return ConsoleApp(service)


def main():
    app = build_application()

    # If --demo passed in CLI, run automated walkthrough
    if "--demo" in sys.argv:
        app.run_demo()
    else:
        app.run_menu()


if __name__ == "__main__":
    main()
