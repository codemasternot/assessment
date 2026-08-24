from __future__ import annotations

from random import Random
from time import perf_counter

from graph_router import GraphRouter


def build_graph(nodes: int = 2_000, extra_edges: int = 8_000, seed: int = 2026) -> GraphRouter:
    rng = Random(seed)
    graph = GraphRouter()

    # Backbone keeps the graph connected.
    for node in range(nodes - 1):
        graph.add_edge(node, node + 1, 1 + (node % 7))

    for _ in range(extra_edges):
        a = rng.randrange(nodes)
        b = rng.randrange(nodes)
        if a != b:
            graph.add_edge(a, b, rng.randint(1, 30))

    return graph


def benchmark_repeated_source_queries(nodes: int = 2_000, queries: int = 400) -> float:
    graph = build_graph(nodes=nodes)
    rng = Random(99)
    targets = [rng.randrange(1, nodes) for _ in range(queries)]

    start = perf_counter()
    checksum = 0.0
    for target in targets:
        cost, path = graph.shortest_path(0, target)
        if path:
            checksum += cost
    elapsed = perf_counter() - start

    assert checksum >= 0
    return elapsed


if __name__ == "__main__":
    print("Graph repeated-source routing benchmark")
    print("nodes\tqueries\tseconds")
    for nodes in [500, 1_000, 2_000]:
        elapsed = benchmark_repeated_source_queries(nodes=nodes)
        print(f"{nodes}\t400\t{elapsed:.6f}")
