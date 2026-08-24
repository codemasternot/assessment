# Variant B — Open-Addressed Hash Cache

You are maintaining a bounded in-memory cache built on a custom open-addressed hash table. The cache supports lookup, insertion/update, explicit deletion, and least-recently-used eviction when full.

The data structure must preserve probe-chain correctness under insertion and deletion, maintain one live entry per key, and evict the least-recently-used live entry when capacity is reached.

## Your task

1. Identify the core representation/probing invariants.
2. Discover a small operation sequence that demonstrates a correctness defect.
3. Repair the root cause and add regression tests.
4. Identify an avoidable complexity problem under a high-churn cache workload and improve it while preserving public behaviour.
5. Produce before/after benchmark evidence.
6. Complete the AI review only after the human-only phases.
7. Submit a GitHub Pull Request meeting `../ASSESSMENT_4_RULES.md`.

## Public API

`HashCache(max_items)` supports:

- `put(key, value)`
- `get(key, default=None)`
- `delete(key)`
- `contains(key)`
- `items()`
- `validate()`

Do not replace the cache with `dict`, `OrderedDict`, or a third-party cache implementation. Standard-library helper structures may be introduced only if you can explain why they preserve the assessment's intended data-structure reasoning.

## Required evidence

Your PR must include a minimal failing sequence, exact invariant/correctness condition, regression tests, repair rationale, complexity before/after, and benchmark evidence from `benchmark.py` or an assessor-approved equivalent.

```bash
python -m pytest -q
python benchmark.py
```

Visible tests are intentionally incomplete.
