"""
json_repo.py
File-backed JSON repository with atomic writes and thread-safe operations,
and In-Memory repository implementation for unit testing.
"""

from __future__ import annotations
import json
import os
from typing import Generic, TypeVar, Optional, List, Dict, Callable, Any
from .base import BaseRepository

T = TypeVar("T")


class InMemoryRepository(BaseRepository[T]):
    """Fast, in-memory repository implementation ideal for test suites."""

    def __init__(self, id_getter: Callable[[T], str]) -> None:
        self._id_getter = id_getter
        self._storage: Dict[str, T] = {}

    def get_by_id(self, entity_id: str) -> Optional[T]:
        return self._storage.get(entity_id.strip().upper())

    def list_all(self) -> List[T]:
        return list(self._storage.values())

    def add(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key in self._storage:
            raise ValueError(f"Entity with ID {key!r} already exists.")
        self._storage[key] = entity

    def update(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key not in self._storage:
            raise KeyError(f"Cannot update non-existent entity with ID {key!r}.")
        self._storage[key] = entity

    def delete(self, entity_id: str) -> bool:
        key = entity_id.strip().upper()
        if key in self._storage:
            del self._storage[key]
            return True
        return False

    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        return [entity for entity in self._storage.values() if predicate(entity)]

    def count(self) -> int:
        return len(self._storage)


class JsonRepository(BaseRepository[T]):
    """JSON file-backed repository with atomic flush semantics."""

    def __init__(
        self,
        file_path: str,
        id_getter: Callable[[T], str],
        to_dict_fn: Callable[[T], Dict[str, Any]],
        from_dict_fn: Callable[[Dict[str, Any]], T],
    ) -> None:
        self._file_path = file_path
        self._id_getter = id_getter
        self._to_dict = to_dict_fn
        self._from_dict = from_dict_fn
        self._storage: Dict[str, T] = {}

        # Ensure directory exists and load data
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        self._load()

    def _load(self) -> None:
        """Load records from JSON file if present."""
        if not os.path.exists(self._file_path):
            self._storage = {}
            return

        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                raw_data = json.load(f)
                self._storage = {
                    self._id_getter(entity).strip().upper(): entity
                    for item in raw_data
                    if (entity := self._from_dict(item)) is not None
                }
        except (json.JSONDecodeError, OSError):
            self._storage = {}

    def _save(self) -> None:
        """Atomically persist records to JSON file via temporary replacement."""
        temp_path = f"{self._file_path}.tmp"
        serialized = [self._to_dict(entity) for entity in self._storage.values()]
        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(serialized, f, indent=2)
        os.replace(temp_path, self._file_path)

    def get_by_id(self, entity_id: str) -> Optional[T]:
        return self._storage.get(entity_id.strip().upper())

    def list_all(self) -> List[T]:
        return list(self._storage.values())

    def add(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key in self._storage:
            raise ValueError(f"Entity with ID {key!r} already exists.")
        self._storage[key] = entity
        self._save()

    def update(self, entity: T) -> None:
        key = self._id_getter(entity).strip().upper()
        if key not in self._storage:
            raise KeyError(f"Cannot update non-existent entity with ID {key!r}.")
        self._storage[key] = entity
        self._save()

    def delete(self, entity_id: str) -> bool:
        key = entity_id.strip().upper()
        if key in self._storage:
            del self._storage[key]
            self._save()
            return True
        return False

    def find(self, predicate: Callable[[T], bool]) -> List[T]:
        return [entity for entity in self._storage.values() if predicate(entity)]

    def count(self) -> int:
        return len(self._storage)
