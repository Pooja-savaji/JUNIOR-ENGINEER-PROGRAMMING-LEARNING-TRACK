"""
in_memory.py
Mock repository implementation for hermetic, fast unit testing.
"""

from __future__ import annotations
from typing import Generic, TypeVar, Optional, List, Dict, Callable
from .base import BaseRepository

T = TypeVar("T")


class MockRepository(BaseRepository[T]):
    """Pure in-memory repository implementation simulating DB behavior."""

    def __init__(self, id_getter: Callable[[T], str]) -> None:
        self._id_getter = id_getter
        self._data: Dict[str, T] = {}

    def get_by_id(self, entity_id: str) -> Optional[T]:
        return self._data.get(entity_id.strip().upper())

    def list_all(self) -> List[T]:
        return list(self._data.values())

    def add(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key in self._data:
            raise ValueError(f"Entity with ID {key!r} already exists.")
        self._data[key] = entity

    def update(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key not in self._data:
            raise KeyError(f"Entity with ID {key!r} not found for update.")
        self._data[key] = entity

    def delete(self, entity_id: str) -> bool:
        key = entity_id.strip().upper()
        if key in self._data:
            del self._data[key]
            return True
        return False

    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        return [item for item in self._data.values() if predicate(item)]

    def count(self) -> int:
        return len(self._data)
