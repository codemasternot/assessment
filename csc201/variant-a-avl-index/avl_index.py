from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class _Node:
    key: int
    value: Any
    left: "_Node | None" = None
    right: "_Node | None" = None
    height: int = 1


def _height(node: _Node | None) -> int:
    return node.height if node else 0


def _update(node: _Node) -> None:
    node.height = 1 + max(_height(node.left), _height(node.right))


def _balance_factor(node: _Node) -> int:
    return _height(node.left) - _height(node.right)


def _rotate_right(y: _Node) -> _Node:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    _update(y)
    _update(x)
    return x


def _rotate_left(x: _Node) -> _Node:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    _update(x)
    _update(y)
    return y


def _rebalance(node: _Node) -> _Node:
    _update(node)
    bf = _balance_factor(node)

    if bf > 1:
        assert node.left is not None
        if _balance_factor(node.left) < 0:
            node.left = _rotate_left(node.left)
        return _rotate_right(node)

    if bf < -1:
        assert node.right is not None
        if _balance_factor(node.right) > 0:
            node.right = _rotate_right(node.right)
        return _rotate_left(node)

    return node


class AVLIndex:
    """Mutable integer-key index implemented as an AVL tree."""

    def __init__(self) -> None:
        self._root: _Node | None = None
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def height(self) -> int:
        return _height(self._root)

    def set(self, key: int, value: Any) -> None:
        inserted = False

        def insert(node: _Node | None) -> _Node:
            nonlocal inserted
            if node is None:
                inserted = True
                return _Node(key, value)
            if key < node.key:
                node.left = insert(node.left)
            elif key > node.key:
                node.right = insert(node.right)
            else:
                node.value = value
                return node
            return _rebalance(node)

        self._root = insert(self._root)
        if inserted:
            self._size += 1

    def get(self, key: int, default: Any = None) -> Any:
        node = self._root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return default

    def delete(self, key: int) -> bool:
        deleted = False

        def delete_node(node: _Node | None, target: int) -> _Node | None:
            nonlocal deleted
            if node is None:
                return None

            if target < node.key:
                node.left = delete_node(node.left, target)
            elif target > node.key:
                node.right = delete_node(node.right, target)
            else:
                deleted = True
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left

                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key = successor.key
                node.value = successor.value

                # Delete the copied successor from the right subtree.  We do not
                # want this internal deletion to affect the public deleted flag.
                prior = deleted
                node.right = _delete_without_flag(node.right, successor.key)
                deleted = prior
                _update(node)
                return node

            return _rebalance(node)

        def _delete_without_flag(node: _Node | None, target: int) -> _Node | None:
            if node is None:
                return None
            if target < node.key:
                node.left = _delete_without_flag(node.left, target)
            elif target > node.key:
                node.right = _delete_without_flag(node.right, target)
            else:
                if node.left is None:
                    return node.right
                if node.right is None:
                    return node.left
                successor = node.right
                while successor.left is not None:
                    successor = successor.left
                node.key = successor.key
                node.value = successor.value
                node.right = _delete_without_flag(node.right, successor.key)
            return _rebalance(node)

        self._root = delete_node(self._root, key)
        if deleted:
            self._size -= 1
        return deleted

    def items(self) -> list[tuple[int, Any]]:
        result: list[tuple[int, Any]] = []
        stack: list[_Node] = []
        node = self._root
        while stack or node is not None:
            while node is not None:
                stack.append(node)
                node = node.left
            node = stack.pop()
            result.append((node.key, node.value))
            node = node.right
        return result

    def range_items(self, low: int, high: int) -> list[tuple[int, Any]]:
        if low > high:
            return []
        return [(key, value) for key, value in self.items() if low <= key <= high]

    def validate(self) -> tuple[bool, str]:
        """Check BST ordering, stored heights, AVL balance, and node count."""

        count = 0

        def walk(node: _Node | None, lo: int | None, hi: int | None) -> tuple[bool, str, int]:
            nonlocal count
            if node is None:
                return True, "", 0

            if lo is not None and node.key <= lo:
                return False, f"BST ordering violated at key {node.key}: expected > {lo}", 0
            if hi is not None and node.key >= hi:
                return False, f"BST ordering violated at key {node.key}: expected < {hi}", 0

            ok, msg, left_h = walk(node.left, lo, node.key)
            if not ok:
                return ok, msg, 0
            ok, msg, right_h = walk(node.right, node.key, hi)
            if not ok:
                return ok, msg, 0

            expected_h = 1 + max(left_h, right_h)
            if node.height != expected_h:
                return False, f"stored height wrong at key {node.key}: {node.height} != {expected_h}", 0
            if abs(left_h - right_h) > 1:
                return False, f"AVL balance violated at key {node.key}: left={left_h}, right={right_h}", 0

            count += 1
            return True, "", expected_h

        ok, msg, _ = walk(self._root, None, None)
        if not ok:
            return False, msg
        if count != self._size:
            return False, f"size mismatch: counted {count}, stored {self._size}"
        return True, "ok"

    def __iter__(self) -> Iterator[tuple[int, Any]]:
        yield from self.items()
