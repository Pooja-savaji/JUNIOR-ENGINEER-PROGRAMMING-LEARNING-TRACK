"""
05_dataclasses_and_domain_models.py
====================================
Module 2: Object-Oriented Programming & Modular Design
Topic: Modern Data Modeling with Python Dataclasses

Concepts Covered:
  - `@dataclass` decorator for clean, boilerplate-free data structures
  - `frozen=True` for immutability and hashability
  - Default factory values (`field(default_factory=list)`)
  - Invariant validation and post-processing with `__post_init__`
  - Domain entities: `User`, `MaintenanceLog`, `AssetCategory`, `HardwareAsset`
  - Bidirectional JSON serialization (to_dict, from_dict, to_json, from_json)
  - Handling dates, enums, and nested dataclass relationships cleanly
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict, is_dataclass
from datetime import date, datetime
from enum import Enum
from typing import Optional, List, Dict, Any
import json


class AssetCategory(str, Enum):
    LAPTOP = "LAPTOP"
    SERVER = "SERVER"
    MONITOR = "MONITOR"
    NETWORKING = "NETWORKING"
    MOBILE = "MOBILE"


class AssetStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    ASSIGNED = "ASSIGNED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    RETIRED = "RETIRED"


@dataclass(frozen=True)
class User:
    """Immutable domain model representing an employee or asset custodian."""
    user_id: str
    name: str
    email: str
    department: str

    def __post_init__(self) -> None:
        if not self.user_id.strip():
            raise ValueError("user_id cannot be empty.")
        if "@" not in self.email:
            raise ValueError(f"Invalid email address: {self.email!r}")


@dataclass(frozen=True)
class MaintenanceLog:
    """Record of a single service or repair event."""
    log_id: str
    service_date: date
    technician: str
    cost: float
    description: str

    def __post_init__(self) -> None:
        if self.cost < 0:
            raise ValueError("Maintenance cost cannot be negative.")


@dataclass
class HardwareAsset:
    """Core domain model representing a physical corporate device."""
    asset_id: str
    model_name: str
    category: AssetCategory
    purchase_price: float
    purchase_date: date
    serial_number: str
    status: AssetStatus = AssetStatus.IN_STOCK
    assigned_user: Optional[User] = None
    maintenance_history: List[MaintenanceLog] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate domain invariants upon instantiation."""
        self.asset_id = self.asset_id.strip().upper()
        if not self.asset_id:
            raise ValueError("asset_id cannot be empty.")
        if self.purchase_price < 0:
            raise ValueError("purchase_price cannot be negative.")
        if not self.serial_number.strip():
            raise ValueError("serial_number cannot be empty.")

        # Ensure enums are resolved if raw strings were supplied
        if isinstance(self.category, str):
            self.category = AssetCategory(self.category)
        if isinstance(self.status, str):
            self.status = AssetStatus(self.status)

    # ─────────────────────────────────────────────────────────────────────────
    # Domain Behaviors & Lifecycle Transitions
    # ─────────────────────────────────────────────────────────────────────────

    def assign_to(self, user: User) -> None:
        """Assign hardware device to an active user."""
        if self.status == AssetStatus.RETIRED:
            raise ValueError(f"Cannot assign retired asset {self.asset_id}.")
        if self.status == AssetStatus.UNDER_MAINTENANCE:
            raise ValueError(f"Asset {self.asset_id} is currently under maintenance.")

        self.assigned_user = user
        self.status = AssetStatus.ASSIGNED

    def check_in(self) -> None:
        """Unassign device and return to warehouse stock."""
        self.assigned_user = None
        self.status = AssetStatus.IN_STOCK

    def log_maintenance(self, log: MaintenanceLog) -> None:
        """Append maintenance record and set status."""
        self.maintenance_history.append(log)
        self.status = AssetStatus.UNDER_MAINTENANCE

    def complete_maintenance(self) -> None:
        """Restore asset status after maintenance concludes."""
        if self.assigned_user is not None:
            self.status = AssetStatus.ASSIGNED
        else:
            self.status = AssetStatus.IN_STOCK

    @property
    def total_maintenance_cost(self) -> float:
        """Total spent on maintenance across lifetime."""
        return round(sum(item.cost for item in self.maintenance_history), 2)

    def calculate_depreciated_value(self, current_date: Optional[date] = None, lifespan_years: int = 4) -> float:
        """Straight-line depreciation calculation."""
        cur = current_date or date.today()
        years_held = (cur - self.purchase_date).days / 365.25
        if years_held <= 0:
            return round(self.purchase_price, 2)
        if years_held >= lifespan_years:
            return 0.0

        depreciation_per_year = self.purchase_price / lifespan_years
        remaining = self.purchase_price - (depreciation_per_year * years_held)
        return round(max(0.0, remaining), 2)

    # ─────────────────────────────────────────────────────────────────────────
    # Bidirectional Serialization (to_dict / from_dict)
    # ─────────────────────────────────────────────────────────────────────────

    def to_dict(self) -> Dict[str, Any]:
        """Convert domain entity to a JSON-serializable dictionary."""
        return {
            "asset_id": self.asset_id,
            "model_name": self.model_name,
            "category": self.category.value,
            "purchase_price": self.purchase_price,
            "purchase_date": self.purchase_date.isoformat(),
            "serial_number": self.serial_number,
            "status": self.status.value,
            "assigned_user": asdict(self.assigned_user) if self.assigned_user else None,
            "maintenance_history": [
                {
                    "log_id": m.log_id,
                    "service_date": m.service_date.isoformat(),
                    "technician": m.technician,
                    "cost": m.cost,
                    "description": m.description,
                }
                for m in self.maintenance_history
            ],
            "tags": list(self.tags),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HardwareAsset:
        """Reconstruct fully typed HardwareAsset instance from dictionary."""
        user_data = data.get("assigned_user")
        user = User(**user_data) if user_data else None

        maintenance_list = [
            MaintenanceLog(
                log_id=item["log_id"],
                service_date=date.fromisoformat(item["service_date"]),
                technician=item["technician"],
                cost=float(item["cost"]),
                description=item["description"],
            )
            for item in data.get("maintenance_history", [])
        ]

        return cls(
            asset_id=data["asset_id"],
            model_name=data["model_name"],
            category=AssetCategory(data["category"]),
            purchase_price=float(data["purchase_price"]),
            purchase_date=date.fromisoformat(data["purchase_date"]),
            serial_number=data["serial_number"],
            status=AssetStatus(data.get("status", "IN_STOCK")),
            assigned_user=user,
            maintenance_history=maintenance_list,
            tags=list(data.get("tags", [])),
        )

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent)

    @classmethod
    def from_json(cls, json_str: str) -> HardwareAsset:
        return cls.from_dict(json.loads(json_str))


def main():
    print("=" * 70)
    print("  EXERCISE 05: DATACLASSES & DOMAIN MODELING")
    print("=" * 70)

    # 1. Instantiate domain models
    print("\n[1] Creating Domain Entities:")
    engineer = User(
        user_id="USR-401",
        name="Elena Rostova",
        email="elena.r@deltaiot.com",
        department="Robotics",
    )
    print(f"  User Created (frozen dataclass): {engineer}")

    laptop = HardwareAsset(
        asset_id="AST-1008",
        model_name="ThinkPad P1 Gen 6",
        category=AssetCategory.LAPTOP,
        purchase_price=2450.00,
        purchase_date=date(2023, 6, 15),
        serial_number="PF-3XYZ99",
        tags=["high-compute", "cad-approved"],
    )
    print(f"  Asset Created: {laptop.model_name} [{laptop.status.value}]")

    # 2. State transitions & assignment
    print("\n[2] Asset Lifecycle Transitions:")
    laptop.assign_to(engineer)
    print(f"  Assigned to {laptop.assigned_user.name}: Status is now '{laptop.status.value}'")

    # 3. Add maintenance log
    print("\n[3] Logging Maintenance Event:")
    service_log = MaintenanceLog(
        log_id="MNT-2024-01",
        service_date=date(2024, 2, 10),
        technician="TechSupport Lab",
        cost=180.00,
        description="Replaced thermal paste and cooling fan",
    )
    laptop.log_maintenance(service_log)
    print(f"  Logged Service: ${service_log.cost:.2f} ({service_log.description})")
    print(f"  Total Lifetime Maintenance Cost: ${laptop.total_maintenance_cost:.2f}")
    laptop.complete_maintenance()
    print(f"  Completed Service: Status returned to '{laptop.status.value}'")

    # 4. Depreciation calculation
    print("\n[4] Straight-Line Depreciation:")
    simulated_date = date(2025, 6, 15)  # 2 years later
    dep_val = laptop.calculate_depreciated_value(simulated_date, lifespan_years=4)
    print(f"  Original Purchase Price: ${laptop.purchase_price:,.2f}")
    print(f"  Depreciated Value at {simulated_date}: ${dep_val:,.2f}")

    # 5. Serialization & Deserialization
    print("\n[5] JSON Serialization & Round-Trip Deserialization:")
    json_export = laptop.to_json()
    print("  Serialized JSON Output (Truncated preview):")
    for line in json_export.splitlines()[:12]:
        print(f"    {line}")
    print("    ...")

    # Deserializing back to a live Python object
    reconstructed = HardwareAsset.from_json(json_export)
    print(f"\n  Successfully Reconstructed Asset: {reconstructed.asset_id} - {reconstructed.model_name}")
    print(f"  Reconstructed Custodian: {reconstructed.assigned_user.name} ({reconstructed.assigned_user.email})")
    print(f"  Reconstructed Maintenance Records: {len(reconstructed.maintenance_history)}")
    print(f"  Equality check on fields: {reconstructed.serial_number == laptop.serial_number}")

    print("\nDataclasses and domain modeling demonstration complete!\n")


if __name__ == "__main__":
    main()
