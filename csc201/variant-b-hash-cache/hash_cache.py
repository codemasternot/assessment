from __future__ import annotations

from dataclasses import dataclass
from typing import Any


_TOMBSTONE = object()


@dataclass
class _Entry:
    key: Any
    value: Any
    last_access: int


class HashCache:
    """Bounded LRU cache backed by a custom open-addressed hash table."""

    def __init__(self, max_items: int = 32) -> None:
        if max_items < 1:
            raise ValueError("max_items must be >= 1")
        capacity = 8
        while capacity < max_items * 4:
            capacity *= 2
        self._slots: list[_Entry | object | None] = [None] * capacity
        self._mask = capacity - 1
        self._max_items = max_items
        self._size = 0
        self._clock = 0

    def __len__(self) -> int:
        return self._size

    def _tick(self) -> int:
        self._clock += 1
        return self._clock

    def _start(self, key: Any) -> int:
        return hash(key) & self._mask

    def _find_existing(self, key: Any) -> int | None:
        index = self._start(key)
        for _ in range(len(self._slots)):
            slot = self._slots[index]
            if slot is None:
                return None
            if slot is _TOMBSTONE:
                return None
            assert isinstance(slot, _Entry)
            if slot.key == key:
                return index
            index = (index + 1) & self._mask
        return None

    def _find_for_insert(self, key: Any) -> tuple[int, bool]:
        index = self._start(key)
        first_tombstone: int | None = None

        for _ in range(len(self._slots)):
            slot = self._slots[index]
            if slot is None:
                return (first_tombstone if first_tombstone is not None else index), False
            if slot is _TOMBSTONE:
                if first_tombstone is None:
                    first_tombstone = index
            else:
                assert isinstance(slot, _Entry)
                if slot.key == key:
                    return index, True
            index = (index + 1) & self._mask

        if first_tombstone is not None:
            return first_tombstone, False
        raise RuntimeError("hash table unexpectedly full")

    def put(self, key: Any, value: Any) -> None:
        existing = self._find_existing(key)
        if existing is not None:
            entry = self._slots[existing]
            assert isinstance(entry, _Entry)
            entry.value = value
            entry.last_access = self._tick()
            return

        if self._size >= self._max_items:
            self._evict_lru()

        index, found = self._find_for_insert(key)
        if found:
            entry = self._slots[index]
            assert isinstance(entry, _Entry)
            entry.value = value
            entry.last_access = self._tick()
            return

        self._slots[index] = _Entry(key, value, self._tick())
        self._size += 1

    def get(self, key: Any, default: Any = None) -> Any:
        index = self._find_existing(key)
        if index is None:
            return default
        entry = self._slots[index]
        assert isinstance(entry, _Entry)
        entry.last_access = self._tick()
        return entry.value

    def contains(self, key: Any) -> bool:
        return self._find_existing(key) is not None

    def delete(self, key: Any) -> bool:
        index = self._find_existing(key)
        if index is None:
            return False
        self._slots[index] = _TOMBSTONE
        self._size -= 1
        return True

    def _evict_lru(self) -> None:
        candidate_index: int | None = None
        candidate_access: int | None = None

        for i, slot in enumerate(self._slots):
            if isinstance(slot, _Entry):
                if candidate_access is None or slot.last_access < candidate_access:
                    candidate_index = i
                    candidate_access = slot.last_access

        if candidate_index is None:
            raise RuntimeError("cannot evict from empty cache")

        self._slots[candidate_index] = _TOMBSTONE
        self._size -= 1

    def items(self) -> list[tuple[Any, Any]]:
        return [(slot.key, slot.value) for slot in self._slots if isinstance(slot, _Entry)]

    def validate(self) -> tuple[bool, str]:
        live = [slot for slot in self._slots if isinstance(slot, _Entry)]
        if len(live) != self._size:
            return False, f"size mismatch: stored={self._size}, live={len(live)}"
        if self._size > self._max_items:
            return False, f"capacity exceeded: {self._size} > {self._max_items}"

        seen = set()
        for entry in live:
            if entry.key in seen:
                return False, f"duplicate live key: {entry.key!r}"
            seen.add(entry.key)

        return True, "ok"
