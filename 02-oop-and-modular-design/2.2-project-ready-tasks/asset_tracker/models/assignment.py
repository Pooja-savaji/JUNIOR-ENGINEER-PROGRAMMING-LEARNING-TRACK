"""
assignment.py
AssignmentRecord representing checkout/checkin transactions.
"""

from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict, Any


@dataclass
class AssignmentRecord:
    """Historical record of an asset deployed to an employee."""
    assignment_id: str
    asset_id: str
    emp_id: str
    assigned_at: datetime
    returned_at: Optional[datetime] = None
    condition_on_checkout: str = "Good"
    condition_on_return: Optional[str] = None
    notes: str = ""

    @property
    def is_active(self) -> bool:
        """Returns True if asset is currently deployed with employee."""
        return self.returned_at is None

    def close_assignment(self, condition: str = "Good", notes: str = "") -> None:
        self.returned_at = datetime.now()
        self.condition_on_return = condition
        if notes:
            self.notes = f"{self.notes} | Return note: {notes}".strip(" | ")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "assignment_id": self.assignment_id,
            "asset_id": self.asset_id,
            "emp_id": self.emp_id,
            "assigned_at": self.assigned_at.isoformat(),
            "returned_at": self.returned_at.isoformat() if self.returned_at else None,
            "condition_on_checkout": self.condition_on_checkout,
            "condition_on_return": self.condition_on_return,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> AssignmentRecord:
        ret = data.get("returned_at")
        return cls(
            assignment_id=data["assignment_id"],
            asset_id=data["asset_id"],
            emp_id=data["emp_id"],
            assigned_at=datetime.fromisoformat(data["assigned_at"]),
            returned_at=datetime.fromisoformat(ret) if ret else None,
            condition_on_checkout=data.get("condition_on_checkout", "Good"),
            condition_on_return=data.get("condition_on_return"),
            notes=data.get("notes", ""),
        )

    def __repr__(self) -> str:
        status = "ACTIVE" if self.is_active else f"RETURNED ({self.returned_at.strftime('%Y-%m-%d') if self.returned_at else ''})"
        return f"AssignmentRecord({self.assignment_id}: Asset {self.asset_id} -> Emp {self.emp_id} [{status}])"
