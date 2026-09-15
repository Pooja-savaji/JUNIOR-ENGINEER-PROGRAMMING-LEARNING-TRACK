"""
base.py
Generic Repository Interface.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Optional, List, Callable

T = TypeVar("T")


class BaseRepository(ABC, Generic[T]):
    """Formal generic contract for storage operations."""

    @abstractmethod
    def get_by_id(self, entity_id: str) -> Optional[T]:
        pass

    @abstractmethod
    def list_all(self) -> List[T]:
        pass

    @abstractmethod
    def add(self, entity: T) -> None:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def delete(self, entity_id: str) -> bool:
        pass

    @abstractmethod
    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
