"""
errors.py
Domain-specific custom exceptions hierarchy for Asset Tracker.
"""

class AssetTrackerError(Exception):
    """Base exception for all domain errors in Asset Tracker."""
    pass


class AssetNotFoundError(AssetTrackerError):
    """Raised when an asset identifier cannot be resolved."""
    pass


class AssetAlreadyAssignedError(AssetTrackerError):
    """Raised when attempting to check out an asset that is already deployed."""
    pass


class AssetNotAssignedError(AssetTrackerError):
    """Raised when attempting to check in an asset that is not currently checked out."""
    pass


class AssetInMaintenanceError(AssetTrackerError):
    """Raised when attempting operations on an asset currently undergoing repair."""
    pass


class AssetRetiredError(AssetTrackerError):
    """Raised when attempting operations on a decommissioned asset."""
    pass


class EmployeeNotFoundError(AssetTrackerError):
    """Raised when an employee identifier cannot be resolved."""
    pass


class LicenseSeatsExhaustedError(AssetTrackerError):
    """Raised when all seats for a software license have been allocated."""
    pass


class ValidationError(AssetTrackerError):
    """Raised when domain invariant or field validation fails."""
    pass


class RepositoryError(AssetTrackerError):
    """Raised when persistence or storage I/O operations fail."""
    pass
