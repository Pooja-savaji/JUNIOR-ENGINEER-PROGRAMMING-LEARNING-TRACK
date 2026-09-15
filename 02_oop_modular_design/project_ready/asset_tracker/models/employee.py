"""
employee.py
Employee domain entity representing personnel and asset custodians.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, Any
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class Employee:
    """Enterprise staff member eligible for hardware and software allocations."""
    emp_id: str
    name: str
    email: str
    department: str
    is_active: bool = True

    def __post_init__(self) -> None:
        self.emp_id = self.emp_id.strip().upper()
        if not self.emp_id:
            raise ValueError("Employee emp_id cannot be empty.")
        self.name = self.name.strip()
        if not self.name:
            raise ValueError("Employee name cannot be empty.")
        self.email = self.email.strip().lower()
        if not EMAIL_REGEX.match(self.email):
            raise ValueError(f"Invalid email address: {self.email!r}")
        self.department = self.department.strip()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Employee:
        return cls(
            emp_id=data["emp_id"],
            name=data["name"],
            email=data["email"],
            department=data["department"],
            is_active=bool(data.get("is_active", True)),
        )

    def __repr__(self) -> str:
        status = "Active" if self.is_active else "Inactive"
        return f"Employee({self.emp_id}, {self.name!r}, dept={self.department!r}, {status})"
