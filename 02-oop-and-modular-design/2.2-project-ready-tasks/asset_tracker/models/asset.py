"""
asset.py
Asset domain hierarchy: Base Asset, HardwareAsset, and SoftwareLicense.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from enum import Enum
from typing import Optional, Dict, Any


class AssetStatus(str, Enum):
    IN_STOCK = "IN_STOCK"
    ASSIGNED = "ASSIGNED"
    UNDER_MAINTENANCE = "UNDER_MAINTENANCE"
    RETIRED = "RETIRED"


class AssetCategory(str, Enum):
    LAPTOP = "LAPTOP"
    DESKTOP = "DESKTOP"
    SERVER = "SERVER"
    MOBILE = "MOBILE"
    SOFTWARE_LICENSE = "SOFTWARE_LICENSE"
    PERIPHERAL = "PERIPHERAL"


class Asset(ABC):
    """Abstract root entity for all physical and digital corporate assets."""

    def __init__(
        self,
        asset_id: str,
        name: str,
        category: AssetCategory,
        purchase_price: float,
        purchase_date: date,
        status: AssetStatus = AssetStatus.IN_STOCK,
    ) -> None:
        self._asset_id = asset_id.strip().upper()
        if not self._asset_id:
            raise ValueError("Asset ID cannot be empty.")
        self._name = name.strip()
        if not self._name:
            raise ValueError("Asset name cannot be empty.")
        if purchase_price < 0:
            raise ValueError("Purchase price cannot be negative.")
        self._purchase_price = round(float(purchase_price), 2)
        self._purchase_date = purchase_date
        self._status = AssetStatus(status) if isinstance(status, str) else status

    @property
    def asset_id(self) -> str:
        return self._asset_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def category(self) -> AssetCategory:
        return self._category

    @property
    def purchase_price(self) -> float:
        return self._purchase_price

    @property
    def purchase_date(self) -> date:
        return self._purchase_date

    @property
    def status(self) -> AssetStatus:
        return self._status

    @status.setter
    def status(self, value: AssetStatus) -> None:
        self._status = AssetStatus(value) if isinstance(value, str) else value

    @abstractmethod
    def calculate_current_value(self, as_of_date: Optional[date] = None) -> float:
        """Calculate current financial/depreciated value."""
        pass

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Serialize asset to dictionary."""
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data: Dict[str, Any]) -> Asset:
        """Deserialize dictionary into concrete Asset subtype."""
        pass


class HardwareAsset(Asset):
    """Physical hardware device with serial numbers, warranty, and straight-line depreciation."""

    def __init__(
        self,
        asset_id: str,
        name: str,
        category: AssetCategory,
        purchase_price: float,
        purchase_date: date,
        serial_number: str,
        warranty_expiry: Optional[date] = None,
        lifespan_years: int = 4,
        status: AssetStatus = AssetStatus.IN_STOCK,
        specs: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(asset_id, name, category, purchase_price, purchase_date, status)
        self._category = AssetCategory(category) if isinstance(category, str) else category
        if not serial_number.strip():
            raise ValueError("Serial number cannot be empty.")
        self._serial_number = serial_number.strip()
        self._warranty_expiry = warranty_expiry
        self._lifespan_years = max(1, int(lifespan_years))
        self._specs = dict(specs) if specs else {}

    @property
    def serial_number(self) -> str:
        return self._serial_number

    @property
    def warranty_expiry(self) -> Optional[date]:
        return self._warranty_expiry

    @property
    def lifespan_years(self) -> int:
        return self._lifespan_years

    @property
    def specs(self) -> Dict[str, Any]:
        return dict(self._specs)

    def is_under_warranty(self, as_of_date: Optional[date] = None) -> bool:
        if not self._warranty_expiry:
            return False
        cur = as_of_date or date.today()
        return cur <= self._warranty_expiry

    def calculate_current_value(self, as_of_date: Optional[date] = None) -> float:
        """Straight-line depreciation over useful lifespan."""
        if self._status == AssetStatus.RETIRED:
            return 0.0
        cur = as_of_date or date.today()
        days_held = (cur - self._purchase_date).days
        years_held = max(0.0, days_held / 365.25)

        if years_held >= self._lifespan_years:
            return 0.0

        depreciation_rate = self._purchase_price / self._lifespan_years
        remaining = self._purchase_price - (depreciation_rate * years_held)
        return round(max(0.0, remaining), 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "HardwareAsset",
            "asset_id": self._asset_id,
            "name": self._name,
            "category": self._category.value,
            "purchase_price": self._purchase_price,
            "purchase_date": self._purchase_date.isoformat(),
            "serial_number": self._serial_number,
            "warranty_expiry": self._warranty_expiry.isoformat() if self._warranty_expiry else None,
            "lifespan_years": self._lifespan_years,
            "status": self._status.value,
            "specs": self._specs,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> HardwareAsset:
        w_exp = data.get("warranty_expiry")
        return cls(
            asset_id=data["asset_id"],
            name=data["name"],
            category=AssetCategory(data["category"]),
            purchase_price=float(data["purchase_price"]),
            purchase_date=date.fromisoformat(data["purchase_date"]),
            serial_number=data["serial_number"],
            warranty_expiry=date.fromisoformat(w_exp) if w_exp else None,
            lifespan_years=int(data.get("lifespan_years", 4)),
            status=AssetStatus(data.get("status", "IN_STOCK")),
            specs=data.get("specs", {}),
        )

    def __repr__(self) -> str:
        return (
            f"HardwareAsset({self._asset_id}, {self._name!r}, "
            f"SN={self._serial_number!r}, status={self._status.value})"
        )


class SoftwareLicense(Asset):
    """Digital software license with seat counts, keys, and expiration timelines."""

    def __init__(
        self,
        asset_id: str,
        name: str,
        purchase_price: float,
        purchase_date: date,
        license_key: str,
        total_seats: int = 1,
        allocated_seats: int = 0,
        expiration_date: Optional[date] = None,
        status: AssetStatus = AssetStatus.IN_STOCK,
    ) -> None:
        super().__init__(asset_id, name, AssetCategory.SOFTWARE_LICENSE, purchase_price, purchase_date, status)
        self._category = AssetCategory.SOFTWARE_LICENSE
        if not license_key.strip():
            raise ValueError("License key cannot be empty.")
        self._license_key = license_key.strip()
        if total_seats < 1:
            raise ValueError("Total license seats must be at least 1.")
        self._total_seats = int(total_seats)
        if allocated_seats < 0 or allocated_seats > total_seats:
            raise ValueError(f"Allocated seats must be between 0 and {total_seats}.")
        self._allocated_seats = int(allocated_seats)
        self._expiration_date = expiration_date

    @property
    def license_key(self) -> str:
        return self._license_key

    @property
    def total_seats(self) -> int:
        return self._total_seats

    @property
    def allocated_seats(self) -> int:
        return self._allocated_seats

    @property
    def available_seats(self) -> int:
        return max(0, self._total_seats - self._allocated_seats)

    @property
    def expiration_date(self) -> Optional[date]:
        return self._expiration_date

    def is_expired(self, as_of_date: Optional[date] = None) -> bool:
        if not self._expiration_date:
            return False  # Perpetual license
        cur = as_of_date or date.today()
        return cur > self._expiration_date

    def allocate_seat(self) -> None:
        """Reserve a license seat for an employee."""
        if self.is_expired():
            raise ValueError(f"Software license {self._asset_id} has expired.")
        if self._allocated_seats >= self._total_seats:
            raise ValueError(f"No seats remaining on license {self._asset_id} ({self._total_seats}/{self._total_seats} used).")
        self._allocated_seats += 1
        if self._allocated_seats == self._total_seats:
            self._status = AssetStatus.ASSIGNED
        else:
            self._status = AssetStatus.IN_STOCK

    def release_seat(self) -> None:
        """Release a previously allocated seat."""
        if self._allocated_seats <= 0:
            raise ValueError(f"No allocated seats to release on license {self._asset_id}.")
        self._allocated_seats -= 1
        if self._allocated_seats < self._total_seats and self._status == AssetStatus.ASSIGNED:
            self._status = AssetStatus.IN_STOCK

    def calculate_current_value(self, as_of_date: Optional[date] = None) -> float:
        """Amortized value over subscription period or book value."""
        if self._status == AssetStatus.RETIRED or self.is_expired(as_of_date):
            return 0.0
        if not self._expiration_date:
            # Perpetual: flat value
            return self._purchase_price

        cur = as_of_date or date.today()
        total_days = (self._expiration_date - self._purchase_date).days
        remaining_days = (self._expiration_date - cur).days

        if total_days <= 0 or remaining_days <= 0:
            return 0.0

        fraction = remaining_days / total_days
        return round(self._purchase_price * fraction, 2)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": "SoftwareLicense",
            "asset_id": self._asset_id,
            "name": self._name,
            "category": self._category.value,
            "purchase_price": self._purchase_price,
            "purchase_date": self._purchase_date.isoformat(),
            "license_key": self._license_key,
            "total_seats": self._total_seats,
            "allocated_seats": self._allocated_seats,
            "expiration_date": self._expiration_date.isoformat() if self._expiration_date else None,
            "status": self._status.value,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SoftwareLicense:
        exp = data.get("expiration_date")
        return cls(
            asset_id=data["asset_id"],
            name=data["name"],
            purchase_price=float(data["purchase_price"]),
            purchase_date=date.fromisoformat(data["purchase_date"]),
            license_key=data["license_key"],
            total_seats=int(data.get("total_seats", 1)),
            allocated_seats=int(data.get("allocated_seats", 0)),
            expiration_date=date.fromisoformat(exp) if exp else None,
            status=AssetStatus(data.get("status", "IN_STOCK")),
        )

    def __repr__(self) -> str:
        return (
            f"SoftwareLicense({self._asset_id}, {self._name!r}, "
            f"seats={self._allocated_seats}/{self._total_seats}, status={self._status.value})"
        )
