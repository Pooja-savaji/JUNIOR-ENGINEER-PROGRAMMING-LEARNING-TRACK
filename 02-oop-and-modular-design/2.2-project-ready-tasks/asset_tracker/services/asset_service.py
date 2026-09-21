"""
asset_service.py
Core application service orchestrating asset lifecycle, assignment workflows,
inventory depreciation, and regulatory audit summaries.
"""

from __future__ import annotations
from datetime import date, datetime
from typing import Optional, List, Dict, Any
import uuid

from ..models.asset import Asset, HardwareAsset, SoftwareLicense, AssetStatus, AssetCategory
from ..models.employee import Employee
from ..models.assignment import AssignmentRecord
from ..repositories.base import BaseRepository
from ..exceptions.errors import (
    AssetNotFoundError,
    AssetAlreadyAssignedError,
    AssetNotAssignedError,
    AssetInMaintenanceError,
    AssetRetiredError,
    EmployeeNotFoundError,
    LicenseSeatsExhaustedError,
    ValidationError,
)


class AssetService:
    """Enterprise Business Logic Service for IT Asset Lifecycle Management."""

    def __init__(
        self,
        asset_repo: BaseRepository[Asset],
        employee_repo: BaseRepository[Employee],
        assignment_repo: BaseRepository[AssignmentRecord],
    ) -> None:
        self._asset_repo = asset_repo
        self._employee_repo = employee_repo
        self._assignment_repo = assignment_repo

    # ─────────────────────────────────────────────────────────────────────────
    # Employee Management
    # ─────────────────────────────────────────────────────────────────────────

    def register_employee(
        self, emp_id: str, name: str, email: str, department: str
    ) -> Employee:
        """Register a new staff member."""
        existing = self._employee_repo.get_by_id(emp_id)
        if existing:
            raise ValidationError(f"Employee with ID {emp_id!r} already exists.")

        emp = Employee(emp_id=emp_id, name=name, email=email, department=department)
        self._employee_repo.add(emp)
        return emp

    def get_employee(self, emp_id: str) -> Employee:
        emp = self._employee_repo.get_by_id(emp_id)
        if not emp:
            raise EmployeeNotFoundError(f"Employee {emp_id!r} not found.")
        return emp

    def list_employees(self) -> List[Employee]:
        return self._employee_repo.list_all()

    # ─────────────────────────────────────────────────────────────────────────
    # Asset Registration
    # ─────────────────────────────────────────────────────────────────────────

    def register_hardware(
        self,
        asset_id: str,
        name: str,
        category: AssetCategory,
        purchase_price: float,
        purchase_date: date,
        serial_number: str,
        warranty_expiry: Optional[date] = None,
        lifespan_years: int = 4,
        specs: Optional[Dict[str, Any]] = None,
    ) -> HardwareAsset:
        """Register physical device in company inventory."""
        if self._asset_repo.get_by_id(asset_id):
            raise ValidationError(f"Asset ID {asset_id!r} already registered.")

        # Ensure serial number uniqueness among hardware
        existing_sn = self._asset_repo.find(
            lambda a: isinstance(a, HardwareAsset) and a.serial_number == serial_number
        )
        if existing_sn:
            raise ValidationError(f"Serial number {serial_number!r} is already assigned to asset {existing_sn[0].asset_id}.")

        hardware = HardwareAsset(
            asset_id=asset_id,
            name=name,
            category=category,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            serial_number=serial_number,
            warranty_expiry=warranty_expiry,
            lifespan_years=lifespan_years,
            specs=specs,
        )
        self._asset_repo.add(hardware)
        return hardware

    def register_software_license(
        self,
        asset_id: str,
        name: str,
        purchase_price: float,
        purchase_date: date,
        license_key: str,
        total_seats: int = 1,
        expiration_date: Optional[date] = None,
    ) -> SoftwareLicense:
        """Register enterprise software license."""
        if self._asset_repo.get_by_id(asset_id):
            raise ValidationError(f"Asset ID {asset_id!r} already registered.")

        license_obj = SoftwareLicense(
            asset_id=asset_id,
            name=name,
            purchase_price=purchase_price,
            purchase_date=purchase_date,
            license_key=license_key,
            total_seats=total_seats,
            expiration_date=expiration_date,
        )
        self._asset_repo.add(license_obj)
        return license_obj

    def get_asset(self, asset_id: str) -> Asset:
        asset = self._asset_repo.get_by_id(asset_id)
        if not asset:
            raise AssetNotFoundError(f"Asset {asset_id!r} not found in inventory.")
        return asset

    def list_assets(self, category: Optional[AssetCategory] = None, status: Optional[AssetStatus] = None) -> List[Asset]:
        results = self._asset_repo.list_all()
        if category:
            results = [a for a in results if a.category == category]
        if status:
            results = [a for a in results if a.status == status]
        return results

    # ─────────────────────────────────────────────────────────────────────────
    # Checkout & Checkin Workflows
    # ─────────────────────────────────────────────────────────────────────────

    def checkout_asset(
        self, asset_id: str, emp_id: str, condition: str = "Good", notes: str = ""
    ) -> AssignmentRecord:
        """Deploy an asset or software license seat to an active employee."""
        asset = self.get_asset(asset_id)
        emp = self.get_employee(emp_id)

        if not emp.is_active:
            raise ValidationError(f"Cannot assign assets to inactive employee {emp.name} ({emp_id}).")

        if asset.status == AssetStatus.RETIRED:
            raise AssetRetiredError(f"Asset {asset_id} has been decommissioned/retired.")
        if asset.status == AssetStatus.UNDER_MAINTENANCE:
            raise AssetInMaintenanceError(f"Asset {asset_id} is currently under maintenance.")

        if isinstance(asset, HardwareAsset):
            if asset.status == AssetStatus.ASSIGNED:
                raise AssetAlreadyAssignedError(f"Hardware asset {asset_id} is already checked out.")
            asset.status = AssetStatus.ASSIGNED
            self._asset_repo.update(asset)

        elif isinstance(asset, SoftwareLicense):
            try:
                asset.allocate_seat()
                self._asset_repo.update(asset)
            except ValueError as err:
                raise LicenseSeatsExhaustedError(str(err)) from err

        # Create audit assignment record
        assignment_id = f"ASN-{uuid.uuid4().hex[:8].upper()}"
        assignment = AssignmentRecord(
            assignment_id=assignment_id,
            asset_id=asset.asset_id,
            emp_id=emp.emp_id,
            assigned_at=datetime.now(),
            condition_on_checkout=condition,
            notes=notes,
        )
        self._assignment_repo.add(assignment)
        return assignment

    def checkin_asset(
        self, asset_id: str, condition: str = "Good", return_notes: str = ""
    ) -> AssignmentRecord:
        """Return an asset or license seat back to stock."""
        asset = self.get_asset(asset_id)

        # Find active assignment record
        active_assignments = self._assignment_repo.find(
            lambda a: a.asset_id == asset.asset_id and a.is_active
        )
        if not active_assignments:
            raise AssetNotAssignedError(f"No active deployment found for asset {asset_id}.")

        assignment = active_assignments[0]
        assignment.close_assignment(condition=condition, notes=return_notes)
        self._assignment_repo.update(assignment)

        if isinstance(asset, HardwareAsset):
            asset.status = AssetStatus.IN_STOCK
            self._asset_repo.update(asset)
        elif isinstance(asset, SoftwareLicense):
            asset.release_seat()
            self._asset_repo.update(asset)

        return assignment

    # ─────────────────────────────────────────────────────────────────────────
    # Maintenance & Retirement Workflows
    # ─────────────────────────────────────────────────────────────────────────

    def send_to_maintenance(self, asset_id: str, reason: str = "") -> None:
        asset = self.get_asset(asset_id)
        if asset.status == AssetStatus.ASSIGNED:
            raise ValidationError(f"Asset {asset_id} must be checked in before sending to maintenance.")
        if asset.status == AssetStatus.RETIRED:
            raise AssetRetiredError(f"Cannot service retired asset {asset_id}.")

        asset.status = AssetStatus.UNDER_MAINTENANCE
        self._asset_repo.update(asset)

    def return_from_maintenance(self, asset_id: str) -> None:
        asset = self.get_asset(asset_id)
        if asset.status != AssetStatus.UNDER_MAINTENANCE:
            raise ValidationError(f"Asset {asset_id} is not currently under maintenance.")

        asset.status = AssetStatus.IN_STOCK
        self._asset_repo.update(asset)

    def retire_asset(self, asset_id: str) -> None:
        asset = self.get_asset(asset_id)
        if asset.status == AssetStatus.ASSIGNED:
            raise ValidationError(f"Asset {asset_id} must be checked in before retiring.")

        asset.status = AssetStatus.RETIRED
        self._asset_repo.update(asset)

    # ─────────────────────────────────────────────────────────────────────────
    # Queries, Valuations & Audits
    # ─────────────────────────────────────────────────────────────────────────

    def get_employee_assets(self, emp_id: str) -> List[Asset]:
        """List all assets currently checked out by a given employee."""
        self.get_employee(emp_id)  # validate employee exists
        active_assignments = self._assignment_repo.find(
            lambda a: a.emp_id == emp_id and a.is_active
        )
        asset_ids = {a.asset_id for a in active_assignments}
        return [self.get_asset(aid) for aid in asset_ids]

    def get_asset_history(self, asset_id: str) -> List[AssignmentRecord]:
        """Audit trail of all checkout/return events for an asset."""
        self.get_asset(asset_id)  # validate asset exists
        return sorted(
            self._assignment_repo.find(lambda a: a.asset_id == asset_id),
            key=lambda a: a.assigned_at,
            reverse=True,
        )

    def calculate_inventory_valuation(self, as_of_date: Optional[date] = None) -> Dict[str, Any]:
        """Perform comprehensive straight-line inventory valuation."""
        all_assets = self._asset_repo.list_all()
        cur_date = as_of_date or date.today()

        total_acquisition = sum(a.purchase_price for a in all_assets)
        total_current_val = sum(a.calculate_current_value(cur_date) for a in all_assets)

        category_breakdown: Dict[str, Dict[str, float]] = {}
        for a in all_assets:
            cat = a.category.value
            if cat not in category_breakdown:
                category_breakdown[cat] = {"count": 0, "acquisition": 0.0, "current_value": 0.0}
            category_breakdown[cat]["count"] += 1
            category_breakdown[cat]["acquisition"] += a.purchase_price
            category_breakdown[cat]["current_value"] += a.calculate_current_value(cur_date)

        return {
            "as_of_date": cur_date.isoformat(),
            "asset_count": len(all_assets),
            "total_acquisition_cost": round(total_acquisition, 2),
            "total_depreciated_value": round(total_current_val, 2),
            "accumulated_depreciation": round(total_acquisition - total_current_val, 2),
            "by_category": category_breakdown,
        }

    def generate_audit_report(self) -> Dict[str, Any]:
        """Generate high-level operational health report."""
        assets = self._asset_repo.list_all()
        total = len(assets)
        by_status: Dict[str, int] = {s.value: 0 for s in AssetStatus}
        for a in assets:
            by_status[a.status.value] += 1

        utilization_rate = (
            (by_status[AssetStatus.ASSIGNED.value] / total * 100.0) if total > 0 else 0.0
        )

        return {
            "total_assets": total,
            "in_stock": by_status[AssetStatus.IN_STOCK.value],
            "assigned": by_status[AssetStatus.ASSIGNED.value],
            "under_maintenance": by_status[AssetStatus.UNDER_MAINTENANCE.value],
            "retired": by_status[AssetStatus.RETIRED.value],
            "utilization_rate_pct": round(utilization_rate, 1),
            "active_assignments": self._assignment_repo.count(),
            "total_employees": self._employee_repo.count(),
        }
