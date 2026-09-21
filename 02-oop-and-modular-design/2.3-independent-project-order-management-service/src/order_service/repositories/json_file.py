"""
json_file.py
File-backed JSON repository implementation with atomic write replacement.
"""

from __future__ import annotations
import json
import os
from typing import Generic, TypeVar, Optional, List, Dict, Callable, Any
from .base import BaseRepository

T = TypeVar("T")


class JsonFileRepository(BaseRepository[T]):
    """Atomic JSON-backed storage for persistence across restarts."""

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

        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
        self._load()

    def _load(self) -> None:
        if not os.path.exists(self._file_path):
            self._storage = {}
            return
        try:
            with open(self._file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._storage = {
                    self._id_getter(obj).strip().upper(): obj
                    for raw in data
                    if (obj := self._from_dict(raw)) is not None
                }
        except (json.JSONDecodeError, OSError):
            self._storage = {}

    def _save(self) -> None:
        temp_file = f"{self._file_path}.tmp"
        serialized = [self._to_dict(obj) for obj in self._storage.values()]
        with open(temp_file, "w", encoding="utf-8") as f:
            json.dump(serialized, f, indent=2)
        os.replace(temp_file, self._file_path)

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
            raise KeyError(f"Entity with ID {key!r} not found for update.")
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
        return [item for item in self._storage.values() if predicate(item)]

    def count(self) -> int:
        return len(self._storage)
