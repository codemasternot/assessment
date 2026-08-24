from __future__ import annotations

from random import Random
from time import perf_counter

from avl_index import AVLIndex


def build_index(n: int, seed: int = 2026) -> AVLIndex:
    rng = Random(seed)
    keys = list(range(n))
    rng.shuffle(keys)
    index = AVLIndex()
    for key in keys:
        index.set(key, key)
    return index


def benchmark_range_queries(n: int, queries: int = 500, width: int = 8) -> float:
    index = build_index(n)
    rng = Random(99)
    starts = [rng.randrange(0, max(1, n - width)) for _ in range(queries)]

    start = perf_counter()
    checksum = 0
    for low in starts:
        rows = index.range_items(low, low + width)
        checksum += len(rows)
    elapsed = perf_counter() - start

    assert checksum > 0
    return elapsed


if __name__ == "__main__":
    print("AVL range-query benchmark")
    print("n\tseconds")
    for n in [2_000, 10_000, 40_000]:
        elapsed = benchmark_range_queries(n)
        print(f"{n}\t{elapsed:.6f}")
