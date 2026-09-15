"""
test_asset_service.py
Unit tests for AssetService utilizing fast In-Memory mock repositories.
"""

import unittest
from datetime import date, datetime

from asset_tracker.models.asset import (
    Asset,
    HardwareAsset,
    SoftwareLicense,
    AssetCategory,
    AssetStatus,
)
from asset_tracker.models.employee import Employee
from asset_tracker.models.assignment import AssignmentRecord
from asset_tracker.repositories.json_repo import InMemoryRepository
from asset_tracker.services.asset_service import AssetService
from asset_tracker.exceptions.errors import (
    AssetNotFoundError,
    AssetAlreadyAssignedError,
    AssetNotAssignedError,
    AssetRetiredError,
    AssetInMaintenanceError,
    LicenseSeatsExhaustedError,
    ValidationError,
)


class TestAssetService(unittest.TestCase):
    """Unit test suite for business service logic."""

    def setUp(self) -> None:
        self.asset_repo = InMemoryRepository[Asset](id_getter=lambda a: a.asset_id)
        self.employee_repo = InMemoryRepository[Employee](id_getter=lambda e: e.emp_id)
        self.assignment_repo = InMemoryRepository[AssignmentRecord](id_getter=lambda a: a.assignment_id)

        self.service = AssetService(
            asset_repo=self.asset_repo,
            employee_repo=self.employee_repo,
            assignment_repo=self.assignment_repo,
        )

        # Register sample employee
        self.emp = self.service.register_employee(
            "EMP-01", "Test Alice", "alice@example.com", "Engineering"
        )

        # Register sample hardware
        self.laptop = self.service.register_hardware(
            asset_id="AST-01",
            name="ThinkPad T14",
            category=AssetCategory.LAPTOP,
            purchase_price=1200.0,
            purchase_date=date(2023, 1, 1),
            serial_number="SN-TEST-1234",
            lifespan_years=3,
        )

    def test_register_duplicate_employee_fails(self):
        with self.assertRaises(ValidationError):
            self.service.register_employee("EMP-01", "Duplicate Alice", "alice2@example.com", "HR")

    def test_checkout_and_checkin_success(self):
        asn = self.service.checkout_asset("AST-01", "EMP-01", condition="Good")
        self.assertTrue(asn.is_active)
        self.assertEqual(self.laptop.status, AssetStatus.ASSIGNED)

        # Verify employee custody
        deployed = self.service.get_employee_assets("EMP-01")
        self.assertEqual(len(deployed), 1)
        self.assertEqual(deployed[0].asset_id, "AST-01")

        # Check in
        returned = self.service.checkin_asset("AST-01", condition="Good", return_notes="Returned clean")
        self.assertFalse(returned.is_active)
        self.assertIsNotNone(returned.returned_at)
        self.assertEqual(self.laptop.status, AssetStatus.IN_STOCK)

    def test_double_checkout_raises_already_assigned(self):
        self.service.checkout_asset("AST-01", "EMP-01")
        with self.assertRaises(AssetAlreadyAssignedError):
            self.service.checkout_asset("AST-01", "EMP-01")

    def test_checkin_unassigned_raises_error(self):
        with self.assertRaises(AssetNotAssignedError):
            self.service.checkin_asset("AST-01")

    def test_cannot_checkout_maintenance_or_retired(self):
        self.service.send_to_maintenance("AST-01")
        with self.assertRaises(AssetInMaintenanceError):
            self.service.checkout_asset("AST-01", "EMP-01")

        self.service.return_from_maintenance("AST-01")
        self.service.retire_asset("AST-01")
        with self.assertRaises(AssetRetiredError):
            self.service.checkout_asset("AST-01", "EMP-01")

    def test_software_license_seat_exhaustion(self):
        lic = self.service.register_software_license(
            asset_id="LIC-01",
            name="IDE License",
            purchase_price=300.0,
            purchase_date=date(2023, 1, 1),
            license_key="KEY-123",
            total_seats=2,
            expiration_date=date(2030, 1, 1),
        )

        emp2 = self.service.register_employee("EMP-02", "Bob", "bob@example.com", "QA")
        emp3 = self.service.register_employee("EMP-03", "Carol", "carol@example.com", "Dev")

        # Seat 1
        self.service.checkout_asset("LIC-01", "EMP-01")
        self.assertEqual(lic.allocated_seats, 1)
        self.assertEqual(lic.available_seats, 1)

        # Seat 2
        self.service.checkout_asset("LIC-01", "EMP-02")
        self.assertEqual(lic.allocated_seats, 2)
        self.assertEqual(lic.available_seats, 0)
        self.assertEqual(lic.status, AssetStatus.ASSIGNED)

        # Seat 3 should fail
        with self.assertRaises(LicenseSeatsExhaustedError):
            self.service.checkout_asset("LIC-01", "EMP-03")

        # Release seat
        self.service.checkin_asset("LIC-01")
        self.assertEqual(lic.allocated_seats, 1)
        self.assertEqual(lic.available_seats, 1)

    def test_valuation_calculation(self):
        val = self.service.calculate_inventory_valuation(as_of_date=date(2024, 1, 1))
        self.assertEqual(val["asset_count"], 1)
        self.assertEqual(val["total_acquisition_cost"], 1200.0)
        # 1 year into 3 year lifespan: remaining is roughly $800
        self.assertAlmostEqual(val["total_depreciated_value"], 800.0, delta=10.0)


if __name__ == "__main__":
    unittest.main()
