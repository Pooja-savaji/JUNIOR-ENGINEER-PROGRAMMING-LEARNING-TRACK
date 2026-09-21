"""Persistence abstractions and repository implementations."""
from .base import BaseRepository
from .json_repo import JsonRepository, InMemoryRepository

__all__ = [
    "BaseRepository",
    "JsonRepository",
    "InMemoryRepository",
]
