"""
base.py
Generic Repository interface enforcing the Collection-Oriented CRUD contract.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Callable

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Abstract generic repository contract."""

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        """Find entity by unique identifier. Returns None if not found."""
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        """Retrieve all managed entities."""
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        """Persist a new entity. Raises ValueError if entity already exists."""
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        """Update existing entity. Raises KeyError if entity does not exist."""
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        """Delete entity by ID. Returns True if deleted, False if not found."""
        pass

    @abstractmethod
    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        """Query entities matching a custom predicate."""
        pass

    @abstractmethod
    def count(self) -> int:
        """Total entities count."""
        pass
