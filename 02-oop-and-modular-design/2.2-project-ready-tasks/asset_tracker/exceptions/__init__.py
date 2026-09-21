"""Exceptions package for asset tracker."""
from .errors import (
    AssetTrackerError,
    AssetNotFoundError,
    AssetAlreadyAssignedError,
    AssetNotAssignedError,
    AssetInMaintenanceError,
    AssetRetiredError,
    EmployeeNotFoundError,
    LicenseSeatsExhaustedError,
    ValidationError,
    RepositoryError,
)

__all__ = [
    "AssetTrackerError",
    "AssetNotFoundError",
    "AssetAlreadyAssignedError",
    "AssetNotAssignedError",
    "AssetInMaintenanceError",
    "AssetRetiredError",
    "EmployeeNotFoundError",
    "LicenseSeatsExhaustedError",
    "ValidationError",
    "RepositoryError",
]
