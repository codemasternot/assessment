from __future__ import annotations

from collections import defaultdict
from heapq import heappop, heappush
from math import inf
from typing import Hashable


Node = Hashable


class GraphRouter:
    """Mutable weighted undirected graph with shortest-path queries."""

    def __init__(self) -> None:
        self._adj: dict[Node, dict[Node, float]] = defaultdict(dict)

    def add_edge(self, a: Node, b: Node, weight: float) -> None:
        weight = float(weight)
        if weight < 0:
            raise ValueError("negative weights are not supported")
        self._adj[a][b] = weight
        self._adj[b][a] = weight

    def remove_edge(self, a: Node, b: Node) -> bool:
        existed = b in self._adj.get(a, {}) or a in self._adj.get(b, {})
        self._adj.get(a, {}).pop(b, None)
        self._adj.get(b, {}).pop(a, None)
        return existed

    def neighbors(self, node: Node) -> dict[Node, float]:
        return dict(self._adj.get(node, {}))

    def shortest_path(self, source: Node, target: Node) -> tuple[float, list[Node]]:
        if source == target:
            return 0.0, [source]
        if source not in self._adj or target not in self._adj:
            return inf, []

        distances: dict[Node, float] = {source: 0.0}
        previous: dict[Node, Node] = {}
        queue: list[tuple[float, int, Node]] = []
        serial = 0
        heappush(queue, (0.0, serial, source))
        discovered: set[Node] = {source}

        while queue:
            distance, _, node = heappop(queue)
            if node == target:
                break

            for neighbor, weight in self._adj[node].items():
                candidate = distance + weight
                if candidate < distances.get(neighbor, inf):
                    distances[neighbor] = candidate
                    previous[neighbor] = node
                    if neighbor not in discovered:
                        serial += 1
                        heappush(queue, (candidate, serial, neighbor))
                        discovered.add(neighbor)

        if target not in distances:
            return inf, []

        path = [target]
        cursor = target
        while cursor != source:
            cursor = previous[cursor]
            path.append(cursor)
        path.reverse()
        return distances[target], path

    def validate(self) -> tuple[bool, str]:
        for node, edges in self._adj.items():
            for neighbor, weight in edges.items():
                if weight < 0:
                    return False, f"negative weight on {node!r}->{neighbor!r}"
                reverse = self._adj.get(neighbor, {}).get(node)
                if reverse is None:
                    return False, f"missing reverse edge for {node!r}<->{neighbor!r}"
                if reverse != weight:
                    return False, f"asymmetric weight for {node!r}<->{neighbor!r}"
        return True, "ok"
