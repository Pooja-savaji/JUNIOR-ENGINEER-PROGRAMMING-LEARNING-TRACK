"""
exceptions.py
Domain-specific exceptions for Order Management System.
"""

class OrderManagementError(Exception):
    """Base exception for all domain errors."""
    pass


class OrderNotFoundError(OrderManagementError):
    """Raised when an order ID does not exist."""
    pass


class CustomerNotFoundError(OrderManagementError):
    """Raised when a customer ID does not exist."""
    pass


class InvalidOrderStateError(OrderManagementError):
    """Raised when an illegal order lifecycle transition is attempted."""
    pass


class EmptyOrderError(OrderManagementError):
    """Raised when attempting to confirm or checkout an order with no items."""
    pass


class ValidationError(OrderManagementError):
    """Raised when input validation or domain invariants fail."""
    pass
