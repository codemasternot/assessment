from __future__ import annotations

from random import Random
from time import perf_counter

from hash_cache import HashCache


def churn(max_items: int, operations: int = 50_000, seed: int = 2026) -> float:
    rng = Random(seed)
    cache = HashCache(max_items=max_items)

    for key in range(max_items):
        cache.put(key, key)

    start = perf_counter()
    checksum = 0
    next_key = max_items

    for i in range(operations):
        if i % 4 == 0:
            cache.put(next_key, next_key)
            next_key += 1
        else:
            key = rng.randrange(max(1, next_key - max_items * 2), next_key)
            value = cache.get(key)
            if value is not None:
                checksum ^= int(value)

    elapsed = perf_counter() - start
    ok, message = cache.validate()
    assert ok, message
    assert checksum >= 0
    return elapsed


if __name__ == "__main__":
    print("Hash-cache churn benchmark")
    print("max_items\tseconds")
    for size in [128, 512, 2_048]:
        elapsed = churn(size)
        print(f"{size}\t{elapsed:.6f}")
